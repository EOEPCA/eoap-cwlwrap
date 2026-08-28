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

import time
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


def _build_orchestrator_workflow(  # noqa: C901
    directory_stage_in: Process | None,
    file_stage_in: Process | None,
    workflow: Process,
    directory_stage_out: Process | None,
    file_stage_out: Process | None,
) -> Process:
    start_time = time.time()
    logger.info("Building the CWL Orchestrator Workflow...")

    imports = {URL_SCHEMA}

    def _add_import(type_: Any) -> None:
        if isinstance(type_, list):
            for typ in type_:
                _add_import(typ)
        else:
            type_string: str = type_to_string(type_)
            if "#" in type_string:
                imports.add(type_string.split("#")[0])

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
            add_feature_requirement(
                copy_schema_def_requirement(schema_requirement), orchestrator
            )

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

    stage_in_counters = {"Directory": 0, "File": 0}

    stage_in_cwl = {"Directory": directory_stage_in, "File": file_stage_in}

    stage_out_counters = {"Directory": 0, "File": 0}

    stage_out_cwl = {"Directory": directory_stage_out, "File": file_stage_out}

    for input in workflow.inputs:
        type_string = type_to_string(input.type_)
        _add_import(input.type_)

        logger.info(f"* {workflow.id}/{input.id}: {type_to_string(input.type_)}")

        assignable_type = get_assignable_type(
            actual=input.type_, expected=Directory_or_File
        )

        target_type = input.type_

        if assignable_type:
            stage_in = stage_in_cwl[type_to_string(assignable_type)]
            if not stage_in:
                raise PluginFailureError(
                    f"  input requires a {type_to_string(assignable_type)} stage-in, that was not specified"
                )

            stage_in_id = f"{type_to_string(assignable_type).lower()}_stage_in_{stage_in_counters[type_to_string(assignable_type)]}"

            logger.info(
                f"  {type_to_string(assignable_type)} type detected, creating a related '{stage_in_id}'..."
            )

            logger.info(
                f"  Converting {type_to_string(input.type_)} to URL-compatible type..."
            )

            target_type = replace_type_with_url(
                source=input.type_, to_be_replaced=Directory_or_File
            )

            logger.info(
                f"  {type_to_string(input.type_)} converted to {type_to_string(target_type)}"
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

            for stage_in_input in stage_in.inputs:
                workflow_step.in_.append(
                    WorkflowStepInput(
                        id=stage_in_input.id,
                        source=input.id
                        if is_uri_compatible_type(stage_in_input.type_)
                        else stage_in_input.id,
                    )
                )

                if is_uri_compatible_type(stage_in_input.type_):
                    if is_array_type(input.type_):
                        logger.info(
                            f"  Array detected, 'scatter' required for {stage_in_input.id}:{input.id}"
                        )

                        workflow_step.scatter = stage_in_input.id
                        workflow_step.scatterMethod = "dotproduct"

                        add_feature_requirement(
                            requirement=ScatterFeatureRequirement(),
                            workflow=orchestrator,
                        )

                    if is_nullable(input.type_):
                        logger.info(
                            f"  Nullable detected, 'when' required for {stage_in_input.id}:{input.id}"
                        )

                        workflow_step.when = f"$(inputs.{stage_in_input.id} !== null)"

                        add_feature_requirement(
                            requirement=InlineJavascriptRequirement(),
                            workflow=orchestrator,
                        )

            logger.info(f"  Connecting 'app/{input.id}' to '{stage_in_id}' output...")

            stage_in_output = next(
                filter(
                    lambda output: is_type_assignable_to(
                        output.type_, Directory_or_File
                    ),
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
                    id=input.id,
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
            app.in_.append(WorkflowStepInput(id=input.id, source=input.id))

        orchestrator.inputs.append(
            _to_workflow_input_parameter(
                source=workflow.id, parameter=input, target_type=target_type
            )
        )

    # once all '{type}_stage_in_{index}' are defined, we can now append the 'app' step

    orchestrator.steps.append(app)

    # outputs

    logger.info(f"Analyzing {workflow.id} outputs...")

    for output in workflow.outputs:
        type_string = type_to_string(output.type_)
        _add_import(output.type_)
        logger.info(f"* {workflow.id}/{output.id}: {type_string}")

        assignable_type = get_assignable_type(
            actual=output.type_, expected=Directory_or_File
        )

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

            url_type = replace_type_with_url(
                source=output.type_, to_be_replaced=assignable_type
            )

            logger.info(
                f"  {type_to_string(output.type_)} converted to {type_to_string(url_type)}"
            )

            workflow_step = WorkflowStep(
                id=f"stage_out_{stage_out_counters[type_to_string(assignable_type)]}",
                in_=[],
                out=[output.id for output in stage_out.outputs],
                run=f"#{stage_out.id}",
                label=f"Stage-out {stage_out_counters[type_to_string(assignable_type)]}",
                doc=f"Stage-out {type_to_string(output.type_)} {stage_out_counters[type_to_string(assignable_type)]}",
            )

            orchestrator.steps.append(workflow_step)

            for stage_out_input in stage_out.inputs:
                workflow_step.in_.append(
                    WorkflowStepInput(
                        id=stage_out_input.id,
                        source=f"app/{output.id}"
                        if is_directory_compatible_type(stage_out_input.type_)
                        else stage_out_input.id,
                    )
                )

                if is_directory_compatible_type(stage_out_input.type_):
                    if is_array_type(url_type):
                        logger.info(
                            f"  Array detected, scatter required for {stage_out_input.id}:app/{output.id}"
                        )

                        workflow_step.scatter = stage_out_input.id
                        workflow_step.scatterMethod = "dotproduct"

                        add_feature_requirement(
                            requirement=ScatterFeatureRequirement(),
                            workflow=orchestrator,
                        )

                    if is_nullable(url_type):
                        logger.info(
                            f"  Nullable detected, 'when' required for {stage_out_input.id}:app/{output.id}"
                        )

                        workflow_step.when = f"$(inputs.{stage_out_input.id} !== null)"

                        add_feature_requirement(
                            requirement=InlineJavascriptRequirement(),
                            workflow=orchestrator,
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

    if not add_feature_requirement(
        requirement=SchemaDefRequirement(
            types=[{"$import": import_} for import_ in set(imports)]
        ),
        workflow=orchestrator,
    ):
        logger.debug("Merging existing feature requirements")
        schema_requirement = get_feature_requirement(SchemaDefRequirement, orchestrator)
        if schema_requirement:
            merge_schema_def_imports(schema_requirement, imports)

    end_time = time.time()
    logger.success(
        f"Orchestrator Workflow built in {end_time - start_time:.4f} seconds"
    )

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
