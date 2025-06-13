"""
CWL Chain Builder (c) 2025

CWL Chain Builder is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from cwl_utils.parser import load_document_by_uri, save, Directory
from cwl_utils.parser.cwl_v1_2 import CommandInputRecordSchema, LoadingOptions, SchemaDefRequirement, Workflow, WorkflowInputParameter, WorkflowOutputParameter, WorkflowStep
from loguru import logger
from pathlib import Path
from ruamel.yaml import YAML
from typing import Any
import click
import sys
import uuid

def extract_id_name(id : Any) -> str:
    return id.split('#')[-1].split('/')[-1]

def build_workflow(stage_in_cwl, workflow_cwl, stage_out_cwl) -> Workflow:
    inputs = []
    outputs = []
    steps = []

    steps_labels = ['stage_in', 'app', 'stage_out']

    # inputs
    for i, cwl in enumerate([stage_in_cwl, workflow_cwl, stage_out_cwl]):
        for input in cwl.inputs:
            inputs.append(WorkflowInputParameter(id = input.id,
                                                 type_ = input.type_,
                                                 label = input.label,
                                                 secondaryFiles = input.secondaryFiles,
                                                 streamable = input.streamable,
                                                 doc = input.doc,
                                                 format = input.format,
                                                 loadContents = getattr(input, 'loadContents', None),
                                                 loadListing = getattr(input, 'loadListing', None),
                                                 default = input.default,
                                                 inputBinding = input.inputBinding,
                                                 extension_fields = input.extension_fields,
                                                 loadingOptions = input.loadingOptions))

        # steps
        steps.append(WorkflowStep(id = steps_labels[i],
                                  in_= [],
                                  out = list(map(lambda out: out.id, cwl.outputs)),
                                  run = cwl.id))

    # outputs
    for output in stage_out_cwl.outputs:
        outputs.append(WorkflowOutputParameter(id = output.id,
                                               outputSource = f"stage_out/{output.id}",
                                               type_ = output.type_,
                                               label = output.label,
                                               secondaryFiles = output.secondaryFiles,
                                               streamable = output.streamable,
                                               doc = output.doc,
                                               format = output.format,
                                               extension_fields = output.extension_fields,
                                               loadingOptions = output.loadingOptions))

    return Workflow(id = 'main',
                    requirements = [ SchemaDefRequirement(types=[ { '$import': 'https://raw.githubusercontent.com/eoap/schemas/main/url.yaml' } ]) ],
                    inputs = inputs,
                    outputs = outputs,
                    steps = steps)

def clean_workflow(workflow):
    workflow.id = workflow.id.split('#')[-1]

    for parameters in [ workflow.inputs, workflow.outputs ]:
        for parameter in parameters:
            parameter.id = parameter.id.split('/')[-1]

            if hasattr(parameter, 'outputSource'):
                for i, output_source in enumerate(parameter.outputSource):
                    parameter.outputSource[i] = output_source.split(f"{workflow.id}/")[-1]

    if hasattr(workflow, 'steps'):
        for step in workflow.steps:
            step.id = step.id.split(f"{workflow.id}/")[-1]

            for step_in in getattr(step, 'in_', []):
                step_in.id = step_in.id.split('/')[-1]
                step_in.source = step_in.source.split('/')[-1]

            step_outs = getattr(step, 'out', [])
            for i, step_out in enumerate(step_outs):
                step_outs[i] = step_out.split('/')[-1]

            if hasattr(step, 'run'):
                step.run = step.run.split('#')[-1]

def load_workflow(path: str) -> Any:
    with open(path, 'r') as f:
        content = f.read()
    workflow = load_document_by_uri(path = path,
                                    loadingOptions = LoadingOptions(),
                                    load_all = True)
    if isinstance(workflow, list):
        for wf in workflow:
            clean_workflow(wf)
    else:
        clean_workflow(workflow)

    return workflow

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
@click.option("--output", "-o", type=click.Path(), required=True, help="Output file path")
def main(stage_in,
         workflow,
         workflow_id,
         stage_out,
         output):
    stage_in_cwl = load_workflow(path = stage_in)

    workflows_cwl = load_workflow(path = workflow)
    workflow_cwl = search_workflow(workflow_id = workflow_id, workflow = workflows_cwl)

    stage_out_cwl = load_workflow(path = stage_out)

    orchestrator = build_workflow(stage_in_cwl, workflow_cwl, stage_out_cwl)

    main_workflow = [ orchestrator, stage_in_cwl ]

    if isinstance(workflows_cwl, list):
        for wf in workflows_cwl:
            main_workflow.append(wf)
    else:
        main_workflow.append(workflows_cwl)

    main_workflow.append(stage_out_cwl)

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    yaml = YAML()

    with output_path.open("w") as f:
        yaml.dump(save(main_workflow), f)

    logger.info(f"Raw workflow written to: {output_path}")

if __name__ == "__main__":
    main()
