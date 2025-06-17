"""
CWL Chain Builder (c) 2025

CWL Chain Builder is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from .loader import load_workflow
from .types import are_cwl_types_identical, is_directory_type
from cwl_utils.parser import save
from cwl_utils.parser.cwl_v1_2 import ( LoadingOptions,
                                        SchemaDefRequirement,
                                        SubworkflowFeatureRequirement,
                                        Workflow,
                                        WorkflowInputParameter,
                                        WorkflowOutputParameter,
                                        WorkflowStep,
                                        WorkflowStepInput )

from pathlib import Path
from ruamel.yaml import YAML
from typing import Any
import click
import sys

def build_orchestrator_workflow(
        stage_in_cwl: Any,
        workflow_cwl: Any,
        stage_out_cwl: Any) -> Any:
    print(f"Building the CWL Orchestrator Workflow...")

    loadingOptions = LoadingOptions()

    orchestrator = Workflow(
        id='main',
        requirements=[
            SubworkflowFeatureRequirement(),
            SchemaDefRequirement(types=[ { '$import': 'https://raw.githubusercontent.com/eoap/schemas/main/url.yaml' } ])
        ],
        inputs=[],
        outputs=[],
        steps=[]
    )

    # steps
    prev_step_label, prev_cwl = None, None
    for step_label, cwl in { 'stage_in': stage_in_cwl, 'app': workflow_cwl, 'stage_out': stage_out_cwl }.items():
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
                    for workflow_input in workflow_cwl.inputs:
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
    for app_output in workflow_cwl.outputs:
        if is_directory_type(app_output.type_):
            for stage_out_output in stage_out_cwl.outputs:
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
    yaml = YAML()

    stage_in_cwl = load_workflow(path=stage_in, yaml=yaml)

    workflows_cwl = load_workflow(path=workflow, yaml=yaml)
    workflow_cwl = search_workflow(workflow_id=workflow_id, workflow=workflows_cwl)

    stage_out_cwl = load_workflow(path=stage_out, yaml=yaml)

    orchestrator = build_orchestrator_workflow(stage_in_cwl, workflow_cwl, stage_out_cwl)

    main_workflow = [ orchestrator, stage_in_cwl ]

    if isinstance(workflows_cwl, list):
        for wf in workflows_cwl:
            main_workflow.append(wf)
    else:
        main_workflow.append(workflows_cwl)

    main_workflow.append(stage_out_cwl)

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w") as f:
        yaml.dump(
            save(
                val=main_workflow,
                relative_uris=False
            ),
        f)

    print('BUILD SUCCESS')
    print(f"Workflow written to: {output_path}")
    print('------------------------------------------------------------------------')

if __name__ == "__main__":
    main()
