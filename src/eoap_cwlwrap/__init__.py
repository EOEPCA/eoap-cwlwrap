# Copyright 2025 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Compose application workflows with EOAP staging steps."""

import time
from collections.abc import Callable, Mapping
from typing import Any

from cwl_utils.parser import Process
from cwl_utils.parser.cwl_v1_2 import (
    InlineJavascriptRequirement,
    ScatterFeatureRequirement,
    SchemaDefRequirement,
    SubworkflowFeatureRequirement,
    Workflow,
    WorkflowInputParameter,
    WorkflowOutputParameter,
    WorkflowStep,
    WorkflowStepInput,
)
from loguru import logger
from transpiler_mate.api import PluginFailureError

from .requirements import (
    add_feature_requirement,
    copy_schema_def_requirement,
    get_feature_requirement,
    merge_schema_def_imports,
)
from .types import (
    URL_SCHEMA,
    Directory_or_File,
    get_assignable_type,
    is_array_type,
    is_directory_compatible_type,
    is_nullable,
    is_type_assignable_to,
    is_uri_compatible_type,
    replace_type_with_url,
    type_to_string,
    validate_directory_stage_in,
    validate_directory_stage_out,
    validate_file_stage_in,
    validate_file_stage_out,
)
from .types import (
    is_file_compatible_type as is_file_compatible_type,
)
from .types import (
    replace_directory_with_url as replace_directory_with_url,
)


def _to_workflow_input_parameter(
    source: str, parameter: Any, target_type: Any | None = None
) -> WorkflowInputParameter:
    return WorkflowInputParameter(
        type_=target_type if target_type else parameter.type_,
        label=f"{parameter.label} - {source}/{parameter.id}"
        if parameter.label
        else f"{source}/{parameter.id}",
        secondaryFiles=parameter.secondaryFiles,
        streamable=parameter.streamable,
        doc=f"{parameter.doc} - This parameter is derived from {source}/{parameter.id}"
        if parameter.label
        else f"This parameter is derived from: {source}/{parameter.id}",
        id=parameter.id,
        format=parameter.format,
        loadContents=parameter.loadContents,
        loadListing=parameter.loadListing,
        default=parameter.default,
        inputBinding=parameter.inputBinding,
        extension_fields=parameter.extension_fields,
        loadingOptions=parameter.loadingOptions,
    )


def _configure_staging_step(
    orchestrator: Workflow, workflow_step: WorkflowStep, parameter_id: str, parameter_type: object
) -> None:
    """Add scattering and null guards required by a staged parameter."""
    if is_array_type(parameter_type):
        workflow_step.scatter = parameter_id
        workflow_step.scatterMethod = "dotproduct"
        add_feature_requirement(ScatterFeatureRequirement(), orchestrator)
    if is_nullable(parameter_type):
        workflow_step.when = f"$(inputs.{parameter_id} !== null)"
        add_feature_requirement(InlineJavascriptRequirement(), orchestrator)


def _add_type_imports(parameter_type: object, imports: set[str]) -> None:
    """Collect schema imports referenced by a parameter type."""
    if isinstance(parameter_type, list):
        for member_type in parameter_type:
            _add_type_imports(member_type, imports)
    else:
        type_string = type_to_string(parameter_type)
        if "#" in type_string:
            imports.add(type_string.split("#")[0])


def _connect_staging_inputs(
    orchestrator: Workflow,
    workflow_step: WorkflowStep,
    stage: Process,
    source: str,
    parameter_type: object,
    accepts_data: Callable[[object], bool],
) -> None:
    """Wire staging inputs and apply array and null handling to data inputs."""
    for parameter in stage.inputs:
        is_data = accepts_data(parameter.type_)
        workflow_step.in_.append(
            WorkflowStepInput(id=parameter.id, source=source if is_data else parameter.id)
        )
        if is_data:
            _configure_staging_step(orchestrator, workflow_step, parameter.id, parameter_type)


def _connect_inputs(
    workflow: Process,
    orchestrator: Workflow,
    app: WorkflowStep,
    stage_in_cwl: Mapping[str, Process | None],
    imports: set[str],
) -> None:
    """Connect application inputs through staging steps when needed.

    Raises:
        PluginFailureError: If a required staging process or output is missing.
    """
    stage_in_counters = {"Directory": 0, "File": 0}
    for parameter in workflow.inputs:
        _add_type_imports(parameter.type_, imports)

        logger.info(f"* {workflow.id}/{parameter.id}: {type_to_string(parameter.type_)}")

        assignable_type = get_assignable_type(actual=parameter.type_, expected=Directory_or_File)

        target_type = parameter.type_

        if assignable_type:
            stage_in = stage_in_cwl[type_to_string(assignable_type)]
            if not stage_in:
                raise PluginFailureError(
                    f"  parameter requires a {type_to_string(assignable_type)} stage-in, that was not specified"
                )

            stage_in_id = f"{type_to_string(assignable_type).lower()}_stage_in_{stage_in_counters[type_to_string(assignable_type)]}"

            logger.info(
                f"  {type_to_string(assignable_type)} type detected, creating a related '{stage_in_id}'..."
            )

            logger.info(f"  Converting {type_to_string(parameter.type_)} to URL-compatible type...")

            target_type = replace_type_with_url(
                source=parameter.type_, to_be_replaced=Directory_or_File
            )

            logger.info(
                f"  {type_to_string(parameter.type_)} converted to {type_to_string(target_type)}"
            )

            workflow_step = WorkflowStep(
                id=stage_in_id,
                in_=[],
                out=[output.id for output in stage_in.outputs],
                run=f"#{stage_in.id}",
                label=f"Stage-in {stage_in_counters[type_to_string(assignable_type)]}",
                doc=f"Stage-in {type_to_string(assignable_type)} {stage_in_counters[type_to_string(assignable_type)]}",
            )

            orchestrator.steps.append(workflow_step)

            _connect_staging_inputs(
                orchestrator,
                workflow_step,
                stage_in,
                parameter.id,
                parameter.type_,
                is_uri_compatible_type,
            )

            logger.info(f"  Connecting 'app/{parameter.id}' to '{stage_in_id}' output...")

            stage_in_output = next(
                filter(
                    lambda output: is_type_assignable_to(output.type_, Directory_or_File),
                    stage_in.outputs,
                ),
                None,
            )
            if stage_in_output is None:
                raise PluginFailureError(
                    f"  {stage_in.id} does not define a File or Directory output"
                )

            app.in_.append(
                WorkflowStepInput(
                    id=parameter.id,
                    source=f"{stage_in_id}/{stage_in_output.id}",
                )
            )

            if stage_in_counters[type_to_string(assignable_type)] == 0:
                orchestrator.inputs.extend(
                    [
                        _to_workflow_input_parameter(stage_in.id, parameter)
                        for parameter in stage_in.inputs
                        if not is_uri_compatible_type(parameter.type_)
                    ]
                )

            stage_in_counters[type_to_string(assignable_type)] += 1
        else:
            app.in_.append(WorkflowStepInput(id=parameter.id, source=parameter.id))

        orchestrator.inputs.append(
            _to_workflow_input_parameter(
                source=workflow.id, parameter=parameter, target_type=target_type
            )
        )


def _connect_outputs(
    workflow: Process,
    orchestrator: Workflow,
    app: WorkflowStep,
    stage_out_cwl: Mapping[str, Process | None],
    imports: set[str],
) -> None:
    """Connect application outputs through staging steps when configured."""
    stage_out_counters = {"Directory": 0, "File": 0}
    for output in workflow.outputs:
        type_string = type_to_string(output.type_)
        _add_type_imports(output.type_, imports)
        logger.info(f"* {workflow.id}/{output.id}: {type_string}")

        assignable_type = get_assignable_type(actual=output.type_, expected=Directory_or_File)

        app.out.append(output.id)

        if assignable_type:
            stage_out = stage_out_cwl[type_to_string(assignable_type)]
            if not stage_out:
                raise PluginFailureError(
                    f"  output requires a {type_to_string(assignable_type)} stage-out, that was not specified"
                )

            stage_out_id = f"{type_to_string(assignable_type).lower()}_stage_out_{stage_out_counters[type_to_string(assignable_type)]}"

            logger.info(
                f"  {type_to_string(assignable_type)} type detected, creating a related '{stage_out_id}'..."
            )

            url_type = replace_type_with_url(source=output.type_, to_be_replaced=assignable_type)

            logger.info(f"  {type_to_string(output.type_)} converted to {type_to_string(url_type)}")

            workflow_step = WorkflowStep(
                id=f"stage_out_{stage_out_counters[type_to_string(assignable_type)]}",
                in_=[],
                out=[output.id for output in stage_out.outputs],
                run=f"#{stage_out.id}",
                label=f"Stage-out {stage_out_counters[type_to_string(assignable_type)]}",
                doc=f"Stage-out {type_to_string(output.type_)} {stage_out_counters[type_to_string(assignable_type)]}",
            )

            orchestrator.steps.append(workflow_step)

            _connect_staging_inputs(
                orchestrator,
                workflow_step,
                stage_out,
                f"app/{output.id}",
                url_type,
                is_directory_compatible_type,
            )

            logger.info(
                f"  Connecting 'app/{output.id}' to 'stage_out_{stage_out_counters[type_to_string(assignable_type)]}' output..."
            )

            orchestrator.outputs.append(
                next(
                    (
                        WorkflowOutputParameter(
                            id=output.id,
                            type_=url_type,
                            outputSource=f"stage_out_{stage_out_counters[type_to_string(assignable_type)]}/{mapping_output.id}",
                            label=output.label,
                            secondaryFiles=output.secondaryFiles,
                            streamable=output.streamable,
                            doc=output.doc,
                            format=output.format,
                            extension_fields=output.extension_fields,
                            loadingOptions=output.loadingOptions,
                        )
                        for mapping_output in stage_out.outputs
                        if is_uri_compatible_type(mapping_output.type_)
                    ),
                    None,
                )
            )

            stage_out_counters[type_to_string(assignable_type)] += 1
        else:
            orchestrator.outputs.append(
                WorkflowOutputParameter(
                    type_=output.type_,
                    label=f"{output.label} - app/{output.id}"
                    if output.label
                    else f"app/{output.id}",
                    secondaryFiles=output.secondaryFiles,
                    streamable=output.streamable,
                    doc=f"{output.doc} - This output is derived from app/{output.id}"
                    if output.label
                    else f"This output is derived from: app/{output.id}",
                    id=output.id,
                    format=output.format,
                    outputSource=f"app/{output.id}",
                    linkMerge=output.linkMerge,
                    pickValue=output.pickValue,
                    extension_fields=output.extension_fields,
                    loadingOptions=output.loadingOptions,
                )
            )

        if assignable_type and stage_out_counters[type_to_string(assignable_type)] > 0:
            stage_out = stage_out_cwl[type_to_string(assignable_type)]
            if stage_out is None:
                raise ValueError(
                    f"  output requires a {type_to_string(assignable_type)} stage-out, that was not specified"
                )

            orchestrator.inputs.extend(
                [
                    _to_workflow_input_parameter(stage_out.id, parameter)
                    for parameter in stage_out.inputs
                    if not is_directory_compatible_type(parameter.type_)
                ]
            )


def _build_orchestrator_workflow(
    directory_stage_in: Process | None,
    file_stage_in: Process | None,
    workflow: Process,
    directory_stage_out: Process | None,
    file_stage_out: Process | None,
) -> Process:
    """Build a workflow connecting the application and its staging processes."""
    start_time = time.time()
    logger.info("Building the CWL Orchestrator Workflow...")

    imports = {URL_SCHEMA}

    orchestrator = Workflow(
        id="main",
        label=f"{workflow.class_} {workflow.id} orchestrator",
        doc=f"This Workflow is used to orchestrate the {workflow.class_} {workflow.id}",
        requirements=[SubworkflowFeatureRequirement()],
        inputs=[],
        outputs=[],
        steps=[],
    )

    # copy all the SchemaDefRequirement required types from the original workflow
    if isinstance(workflow, Workflow) and workflow.requirements:
        schema_requirement = get_feature_requirement(SchemaDefRequirement, workflow)
        if schema_requirement:
            add_feature_requirement(copy_schema_def_requirement(schema_requirement), orchestrator)

    app = WorkflowStep(
        id="app",
        in_=[],
        out=[],
        run=f"#{workflow.id}",
        label=workflow.label,
        doc=workflow.doc,
    )

    # inputs

    logger.info(f"Analyzing {workflow.id} inputs...")

    stage_in_cwl = {"Directory": directory_stage_in, "File": file_stage_in}

    stage_out_cwl = {"Directory": directory_stage_out, "File": file_stage_out}

    _connect_inputs(workflow, orchestrator, app, stage_in_cwl, imports)

    # once all '{type}_stage_in_{index}' are defined, we can now append the 'app' step

    orchestrator.steps.append(app)

    # outputs

    logger.info(f"Analyzing {workflow.id} outputs...")

    _connect_outputs(workflow, orchestrator, app, stage_out_cwl, imports)

    if not add_feature_requirement(
        requirement=SchemaDefRequirement(types=[{"$import": import_} for import_ in set(imports)]),
        workflow=orchestrator,
    ):
        logger.debug("Merging existing feature requirements")
        schema_requirement = get_feature_requirement(SchemaDefRequirement, orchestrator)
        if schema_requirement:
            merge_schema_def_imports(schema_requirement, imports)

    end_time = time.time()
    logger.success(f"Orchestrator Workflow built in {end_time - start_time:.4f} seconds")

    return orchestrator


def wrap(
    workflow: Process,
    directory_stage_in: Process | None = None,
    directory_stage_out: Process | None = None,
    file_stage_in: Process | None = None,
    file_stage_out: Process | None = None,
) -> Process:
    """
    Composes a CWL `Workflow` from a series of `Workflow`/`CommandLineTool` steps, defined according to [Application package patterns based on data stage-in and stage-out behaviors commonly used in EO workflows](https://github.com/eoap/application-package-patterns), and **packs** it into a single self-contained CWL document.

    Args:
        workflow: The application workflow process to wrap.
        directory_stage_in: The CWL stage-in process for `Directory` derived types.
        directory_stage_out: The CWL stage-out process for `Directory` derived types.
        file_stage_in: The CWL stage-in process for `File` derived types.
        file_stage_out: The CWL stage-out process for `File` derived types.

    Returns:
        The orchestrating CWL `Workflow`.
    """
    if directory_stage_in:
        validate_directory_stage_in(directory_stage_in=directory_stage_in)

    if directory_stage_out:
        validate_directory_stage_out(directory_stage_out=directory_stage_out)

    if file_stage_in:
        validate_file_stage_in(file_stage_in=file_stage_in)

    if file_stage_out:
        validate_file_stage_out(file_stage_out=file_stage_out)

    return _build_orchestrator_workflow(
        directory_stage_in=directory_stage_in,
        file_stage_in=file_stage_in,
        workflow=workflow,
        directory_stage_out=directory_stage_out,
        file_stage_out=file_stage_out,
    )
