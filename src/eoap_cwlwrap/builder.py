"""
EOAP CWLWrap (c) 2025

EOAP CWLWrap is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from .loader import ( load_workflow,
                      dump_workflow )
from .pumler import to_puml
from .types import ( are_cwl_types_identical,
                     is_directory_compatible_type,
                     is_url_compatible_type,
                     replace_directory_with_url,
                     URL_SCHEMA,
                     validate_stage_in,
                     validate_stage_out,
                     Workflows )
from cwl_utils.parser.cwl_v1_2 import ( LoadingOptions,
                                        SchemaDefRequirement,
                                        SubworkflowFeatureRequirement,
                                        Workflow,
                                        WorkflowInputParameter,
                                        WorkflowOutputParameter,
                                        WorkflowStep,
                                        WorkflowStepInput,
                                        WorkflowStepOutput )
from datetime import datetime
from typing import ( Any, Optional )
import click
import sys
import time

def to_workflow_input_parameter(source: str,
                                parameter: Any,
                                target_type: Optional[Any] = None) -> WorkflowInputParameter:
    return WorkflowInputParameter(
        type_=target_type if target_type else parameter.type_,
        label=f"{parameter.label} - {source}/{parameter.id}" if parameter.label else f"{source}/{parameter.id}",
        secondaryFiles=parameter.secondaryFiles,
        streamable=parameter.streamable,
        doc=f"{parameter.doc} - This parameter is derived from {source}/{parameter.id}" if parameter.label else f"This parameter is derived from: {source}/{parameter.id}",
        id=parameter.id,
        format=parameter.format,
        loadContents=parameter.loadContents,
        loadListing=parameter.loadListing,
        default=parameter.default,
        inputBinding=parameter.inputBinding,
        extension_fields=parameter.extension_fields,
        loadingOptions=parameter.loadingOptions,
    )

def build_orchestrator_workflow(
        stage_in: Workflow,
        workflow: Workflow,
        stage_out: Workflow) -> Workflow:
    print(f"Building the CWL Orchestrator Workflow...")

    orchestrator = Workflow(
        id='main',
        requirements=[
            SubworkflowFeatureRequirement(),
            SchemaDefRequirement(types=[ { '$import': URL_SCHEMA } ])
        ],
        inputs=list(
            map(
                lambda parameter: to_workflow_input_parameter(stage_in.id, parameter),
                list(
                    filter(
                        lambda workflow_input: not is_url_compatible_type(workflow_input.type_),
                        stage_in.inputs
                    )
                )
            )
        ),
        outputs=[],
        steps=[]
    )

    app = WorkflowStep(
        id='app',
        in_=[],
        out=[],
        run=f"#{workflow.id}"
    )

    # inputs

    print(f"Analyzing {workflow.id} inputs:")

    directories = 0
    for input in workflow.inputs:
        print(f"* {workflow.id}/{input.id}: {input.type_}")

        target_type = input.type_

        if is_directory_compatible_type(target_type):
            print(f"  Directory type detected, creating a related 'stage_in_{directories}'...")

            target_type = replace_directory_with_url(target_type)

            orchestrator.steps.append(
                WorkflowStep(
                    id=f"stage_in_{directories}",
                    in_=list(
                            map(
                                lambda in_: WorkflowStepInput(
                                    id=in_.id,
                                    source=input.id if are_cwl_types_identical(target_type, in_.type_) else in_.id
                                ),
                                stage_in.inputs
                            )
                        ),
                    out=list(map(lambda out: out.id, stage_in.outputs)),
                    run=f"#{stage_in.id}"
                )
            )

            print(f"  Connecting 'app/{input.id}' to 'stage_in_{directories}' output...")

            app.in_.append(
                WorkflowStepInput(
                    id=input.id,
                    source=f"stage_in_{directories}/{next(filter(lambda out: is_directory_compatible_type(out.type_), stage_in.outputs), None).id}"
                )
            )

            directories += 1
        else:
            app.in_.append(
                WorkflowStepInput(
                    id=input.id,
                    source=input.id
                )
            )

        orchestrator.inputs.append(
            to_workflow_input_parameter(
                source=workflow.id,
                parameter=input,
                target_type=target_type
            )
        )

    orchestrator.inputs += list(
                                map(
                                    lambda parameter: to_workflow_input_parameter(stage_out.id, parameter),
                                    list(
                                        filter(
                                            lambda workflow_input: not is_directory_compatible_type(workflow_input.type_),
                                            stage_out.inputs
                                        )
                                    )
                                )
                            )

    # once all 'stage_in_{index}' are defined, we can now append the 'app' step
    orchestrator.steps.append(app)

    # outputs

    print(f"Analyzing {workflow.id} outputs:")

    directories = 0
    for output in workflow.outputs:
        print(f"* {workflow.id}/{output.id}: {output.type_}")

        app.out.append(output.id)

        if is_directory_compatible_type(output.type_):
            print(f"  Directory type detected, creating a related 'stage_out_{directories}'...")

            orchestrator.steps.append(
                WorkflowStep(
                    id=f"stage_out_{directories}",
                    in_=list(
                            map(
                                lambda in_: WorkflowStepInput(
                                    id=in_.id,
                                    source=f"app/{output.id}" if are_cwl_types_identical(output.type_, in_.type_) else in_.id
                                ),
                                stage_out.inputs
                            )
                        ),
                    out=list(map(lambda out: out.id, stage_out.outputs)),
                    run=f"#{stage_out.id}"
                )
            )

            print(f"  Connecting 'app/{output.id}' to 'stage_out_{directories}' output...")

            url_type = replace_directory_with_url(output.type_)

            orchestrator.outputs.append(
                next(
                    map(
                        lambda mapping_output: WorkflowOutputParameter(
                            id=output.id,
                            type_=url_type,
                            outputSource=[f"stage_out_{directories}/{mapping_output.id}"],
                            label=output.label,
                            secondaryFiles=output.secondaryFiles,
                            streamable=output.streamable,
                            doc=output.doc,
                            format=output.format,
                            extension_fields=output.extension_fields,
                            loadingOptions=output.loadingOptions
                        ),
                        filter(
                            lambda stage_out_cwl_output: are_cwl_types_identical(url_type, stage_out_cwl_output.type_),
                            stage_out.outputs
                        )
                    ),
                    None
                )
            )

            directories += 1

    return orchestrator

def search_workflow(workflow_id: str, workflow: Workflows) -> Workflows:
    if isinstance(workflow, list):
        for wf in workflow:
            if workflow_id in wf.id:
                return wf
    elif workflow_id in workflow.id:
        return wf

    sys.exit(f"Sorry, '{workflow_id}' not found in the workflow input file, only {list(map(lambda wf: wf.id, workflow)) if isinstance(workflow, list) else [workflow.id]} available.")

@click.command()
@click.option("--stage-in", type=click.Path(exists=True), help="The CWL stage-in file")
@click.option("--workflow", type=click.Path(exists=True), help="The CWL workflow file")
@click.option("--workflow-id", help="ID of the workflow")
@click.option("--stage-out", type=click.Path(exists=True), help="The CWL stage-out file")
@click.option("--output", type=click.Path(), required=True, help="Output file path")
@click.option('--puml', is_flag=True, help="Serializes the workflow as PlantUML diagram.")
def main(stage_in: str,
         workflow: str,
         workflow_id: str,
         stage_out: str,
         output: str,
         puml: bool):
    start_time = time.time()

    stage_in_cwl = load_workflow(path=stage_in)
    validate_stage_in(stage_in=stage_in_cwl)

    print('------------------------------------------------------------------------')

    workflows_cwl = load_workflow(path=workflow)
    workflow_cwl = search_workflow(workflow_id=workflow_id, workflow=workflows_cwl)

    print('------------------------------------------------------------------------')

    stage_out_cwl = load_workflow(path=stage_out)
    validate_stage_out(stage_out=stage_out_cwl)

    print('------------------------------------------------------------------------')

    orchestrator = build_orchestrator_workflow(stage_in_cwl, workflow_cwl, stage_out_cwl)

    main_workflow = [ orchestrator, stage_in_cwl ]

    if isinstance(workflows_cwl, list):
        for wf in workflows_cwl:
            main_workflow.append(wf)
    else:
        main_workflow.append(workflows_cwl)

    main_workflow.append(stage_out_cwl)

    print('------------------------------------------------------------------------')
    print('BUILD SUCCESS')
    print('------------------------------------------------------------------------')

    dump_workflow(main_workflow, output)

    print('------------------------------------------------------------------------')

    if puml:
        to_puml(
            workflows=main_workflow,
            output=f"{output}.puml"
        )

        print('------------------------------------------------------------------------')

    end_time = time.time()

    print(f"Total time: {end_time - start_time:.4f} seconds")
    print(f"Finished at: {datetime.fromtimestamp(end_time).isoformat(timespec='milliseconds')}")

if __name__ == "__main__":
    main()
