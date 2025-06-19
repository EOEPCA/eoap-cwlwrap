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
                     is_directory_type,
                     is_url_type,
                     URL_TYPE )
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

    loadingOptions = LoadingOptions()

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
    append_url_schema_def_requirement(workflow)

    app = WorkflowStep(
        id='app',
        in_=[],
        out=[],
        run=f"#{workflow.id}"
    )

    # inputs
    directories = 0
    for input in workflow.inputs:
        print(f"Analyzing {workflow.id}/{input.id} input")

        if is_directory_type(input.type_):
            print(f"  URL type detected, creating a related 'stage_in_{directories}'...")

            orchestrator.steps.append(
                WorkflowStep(
                    id=f"stage_in_{directories}",
                    in_=list(
                            map(
                                lambda in_: WorkflowStepInput(
                                    id=in_.id,
                                    valueFrom=input.id if is_url_type(in_.type_) else in_.id
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

            # Transform the original input Directory type to URL
            input.type_ = URL_TYPE
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
    directories = 0
    for output in workflow.outputs:
        print(f"Analyzing {workflow.id}/{output.id} output")

        if is_directory_type(output.type_):
            orchestrator.steps.append(
                WorkflowStep(
                    id=f"stage_out_{directories}",
                    in_=[],
                    out=[],
                    run=f"#{stage_out.id}"
                )
            )

            # Transform the original input Directory type to URL
            output.type_ = URL_TYPE

            for stage_out_cwl_output in stage_out.outputs:
                if are_cwl_types_identical(output.type_, stage_out_cwl_output.type_):
                    orchestrator.outputs.append(
                        WorkflowOutputParameter(
                            id=output.id,
                            type_=output.type_,
                            outputSource=[f"stage_out_{directories}/{stage_out_cwl_output.id}"],
                            label=output.label,
                            secondaryFiles=output.secondaryFiles,
                            streamable=output.streamable,
                            doc=output.doc,
                            format=output.format,
                            extension_fields=output.extension_fields,
                            loadingOptions=loadingOptions
                        )
                    )

            directories += 1

    '''
    # steps
    prev_step_label, prev_cwl = None, None
    for step_label, cwl in { 'stage_in': stage_in, 'app': workflow, 'stage_out': stage_out }.items():
        print(f"New step '{cwl.id}' as '{step_label}' identified")

        orchestrator.steps.append(
            WorkflowStep(
                id = step_label,
                in_ = [],
                out = list(map(lambda out: out.id, cwl.outputs)),
                run = f"#{cwl.id}"
            )
        )

        print('Analyzing related inputs:')

        # inputs
        for input in cwl.inputs:
            print(f"* {cwl.id}/{input.id}: {input.type_}")

            # linking step inputs from previous step outputs
            if is_directory_type(actual_instance = input.type_):
                if 'app' == step_label:
                    print('  Recognized as part of the main Workflow inputs list')
                    orchestrator.inputs.append(input)

                if prev_cwl:
                    for previous_output in prev_cwl.outputs:
                        if is_directory_type(actual_instance = previous_output.type_):
                            orchestrator.steps[-1].in_.append(
                                WorkflowStepInput(
                                    id=input.id,
                                    valueFrom=f"{prev_step_label}/{previous_output.id}"
                                )
                            )

                            print(f"  Linked to the output of the previous step: {prev_step_label}/{previous_output.id}")
                else:
                    for workflow_input in workflow.inputs:
                        if is_directory_type(actual_instance = workflow_input.type_):
                            orchestrator.steps[-1].in_.append(
                                WorkflowStepInput(
                                    id=input.id,
                                    valueFrom=workflow_input.id
                                )
                            )

                            print(f"  Linked to the {orchestrator.steps[-1].id}/{workflow_input.id} input")
            else:
                orchestrator.inputs.append(input)

                orchestrator.steps[-1].in_.append(
                    WorkflowStepInput(
                        id=input.id,
                        valueFrom=input.id
                    )
                )

                print(f"  Linked to the {orchestrator.steps[-1].id}/{input.id} input")

        prev_step_label, prev_cwl = step_label, cwl

    print('------------------------------------------------------------------------')

    print('Building main Wokflow outputs:')

    # outputs
    for app_output in workflow.outputs:
        if is_directory_type(app_output.type_):
            for stage_out_output in stage_out.outputs:
                if are_cwl_types_identical(app_output.type_, stage_out_output.type_):
                    orchestrator.outputs.append(
                        WorkflowOutputParameter(
                            id=app_output.id,
                            type_=app_output.type_,
                            outputSource=[f"stage_out/{stage_out_output.id}"],
                            label=app_output.label,
                            secondaryFiles=app_output.secondaryFiles,
                            streamable=app_output.streamable,
                            doc=app_output.doc,
                            format=app_output.format,
                            extension_fields=app_output.extension_fields,
                            loadingOptions=loadingOptions
                        )
                    )

                    print(f"* Output '{app_output.id}' linked to 'stage_out/{stage_out_output.id}'")

    print('------------------------------------------------------------------------')
    '''
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

    dump_workflow(main_workflow, output)

    print('BUILD SUCCESS')
    print('------------------------------------------------------------------------')

if __name__ == "__main__":
    main()
