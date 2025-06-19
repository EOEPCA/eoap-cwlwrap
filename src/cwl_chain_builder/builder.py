"""
CWL Chain Builder (c) 2025

CWL Chain Builder is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from .loader import load_workflow, dump_workflow
from .types import ( append_url_schema_def_requirement,
                     are_cwl_types_identical,
                     is_url_type )
from cwl_utils.parser.cwl_v1_2 import ( LoadingOptions,
                                        SubworkflowFeatureRequirement,
                                        Workflow,
                                        WorkflowInputParameter,
                                        WorkflowOutputParameter,
                                        WorkflowStep,
                                        WorkflowStepInput,
                                        WorkflowStepOutput )
from typing import Any
import click

def to_workflow_input_parameter(source: str, parameter: Any) -> WorkflowInputParameter:
    return WorkflowInputParameter(
        type_=parameter.type_,
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

def filter_workflow_input(workflow: Workflow) -> list:
    return list(
        map(
            lambda parameter: to_workflow_input_parameter(workflow.id, parameter),
            list(
                filter(
                    lambda workflow_input: not is_url_type(workflow_input.type_),
                    workflow.inputs
                )
            )
        )
    )

def build_orchestrator_workflow(
        stage_in: Workflow,
        workflow: Workflow,
        stage_out: Workflow) -> Workflow:
    print(f"Building the CWL Orchestrator Workflow...")

    orchestrator = Workflow(
        id='main',
        requirements=[
            SubworkflowFeatureRequirement()
        ],
        inputs=filter_workflow_input(stage_in),
        outputs=[],
        steps=[]
    )

    append_url_schema_def_requirement(orchestrator)

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

        if is_url_type(input.type_):
            print(f"  URL type detected, creating a related 'stage_in_{directories}'...")

            orchestrator.steps.append(
                WorkflowStep(
                    id=f"stage_in_{directories}",
                    in_=list(
                            map(
                                lambda in_: WorkflowStepInput(
                                    id=in_.id,
                                    valueFrom=input.id if are_cwl_types_identical(input.type_, in_.type_) else in_.id
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
                    valueFrom=f"stage_in_{directories}/{next(filter(lambda out: is_url_type(out.type_), stage_in.outputs), None).id}"
                )
            )

            directories += 1
        else:
            app.in_.append(
                WorkflowStepInput(
                    id=input.id,
                    valueFrom=input.id
                )
            )

        orchestrator.inputs.append(to_workflow_input_parameter(workflow.id, input))

    orchestrator.inputs += filter_workflow_input(stage_out)

    # once all 'stage_in_{index}' are defined, we can now append the 'app' step
    orchestrator.steps.append(app)

    # outputs

    print(f"Analyzing {workflow.id} outputs:")

    directories = 0
    for output in workflow.outputs:
        print(f"* {workflow.id}/{output.id}: {output.type_}")

        app.out.append(output.id)

        if is_url_type(output.type_):
            print(f"  URL type detected, creating a related 'stage_out_{directories}'...")

            orchestrator.steps.append(
                WorkflowStep(
                    id=f"stage_out_{directories}",
                    in_=list(
                            map(
                                lambda in_: WorkflowStepInput(
                                    id=in_.id,
                                    valueFrom=f"app/{output.id}" if are_cwl_types_identical(output.type_, in_.type_) else in_.id
                                ),
                                stage_out.inputs
                            )
                        ),
                    out=list(map(lambda out: out.id, stage_out.outputs)),
                    run=f"#{stage_out.id}"
                )
            )

            print(f"  Connecting 'app/{output.id}' to 'stage_out_{directories}' output...")

            orchestrator.outputs.append(
                next(
                    map(
                        lambda mapping_output: WorkflowOutputParameter(
                            id=output.id,
                            type_=output.type_,
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
                            lambda stage_out_cwl_output: are_cwl_types_identical(output.type_, stage_out_cwl_output.type_),
                            stage_out.outputs
                        )
                    ),
                    None
                )
            )

            directories += 1

    return orchestrator

def search_workflow(workflow_id: str, workflow: Any):
    if isinstance(workflow, list):
        for wf in workflow:
            if workflow_id in wf.id:
                return wf
    elif workflow_id in workflow.id:
        return wf

    raise Exception("Sorry, {workflow_id} not found, please check the input file.")

@click.command()
@click.option("--stage-in", type=click.Path(exists=True), help="The CWL stage-in file")
@click.option("--workflow", type=click.Path(exists=True), help="The CWL workflow file")
@click.option("--workflow-id", help="ID of the workflow")
@click.option("--stage-out", type=click.Path(exists=True), help="The CWL stage-out file")
@click.option("--output", type=click.Path(), required=True, help="Output file path")
def main(stage_in,
         workflow,
         workflow_id,
         stage_out,
         output):
    stage_in_cwl = load_workflow(path=stage_in)

    workflows_cwl = load_workflow(path=workflow)
    workflow_cwl = search_workflow(workflow_id=workflow_id, workflow=workflows_cwl)

    stage_out_cwl = load_workflow(path=stage_out)

    orchestrator = build_orchestrator_workflow(stage_in_cwl, workflow_cwl, stage_out_cwl)

    main_workflow = [ orchestrator, stage_in_cwl ]

    if isinstance(workflows_cwl, list):
        for wf in workflows_cwl:
            main_workflow.append(wf)
    else:
        main_workflow.append(workflows_cwl)

    main_workflow.append(stage_out_cwl)

    print('------------------------------------------------------------------------')

    dump_workflow(main_workflow, output)

    print('BUILD SUCCESS')
    print('------------------------------------------------------------------------')

if __name__ == "__main__":
    main()
