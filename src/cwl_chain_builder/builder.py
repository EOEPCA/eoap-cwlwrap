"""
CWL Chain Builder (c) 2025

CWL Chain Builder is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from cwl_utils.parser import load_document_by_yaml, load_document_by_uri, save, Directory
from cwl_utils.parser.cwl_v1_2 import CommandInputRecordSchema, LoadingOptions, SchemaDefRequirement, Workflow, WorkflowInputParameter, WorkflowOutputParameter, WorkflowStep
from loguru import logger
from pathlib import Path
from ruamel.yaml import YAML
from typing import Any
import click
import sys
import uuid

def extract_id_name(var : Any) -> str:
    return var.id.split('#')[-1].split('/')[-1]

def build_workflow(cwls: dict) -> Workflow:
    requirements = [ SchemaDefRequirement(types=[ { '$import': 'https://raw.githubusercontent.com/eoap/schemas/main/url.yaml' } ]) ]

    inputs = []
    outputs = []
    steps = []

    for cwl_id in ['stage-in', 'workflow', 'stage-out']:
        cwl = cwls[cwl_id]

        # inputs
        for input in cwl.inputs:
            inputs.append(WorkflowInputParameter(id = extract_id_name(input),
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
        steps.append(WorkflowStep(id = cwl.id.split('#')[-1],
                                  in_= [],
                                  out = list(map(lambda out: extract_id_name(out), cwl.outputs)),
                                  run = cwl.id.split('#')[0]))

    # outputs
    if 1 != len(cwls['stage-out'].outputs):
        raise ValueError(f"Unexpected 'stage-out' outputs, found {len(cwls['stage-out'].outputs)} items (expected 1) .")

    output = cwls['stage-out'].outputs[0]
    outputs.append(WorkflowOutputParameter(id = extract_id_name(output),
                                           outputSource = [ output.id.split('#')[-1] ],
                                           type_ = output.type_,
                                           label = output.label,
                                           secondaryFiles = output.secondaryFiles,
                                           streamable = output.streamable,
                                           doc = output.doc,
                                           format = output.format,
                                           extension_fields = output.extension_fields,
                                           loadingOptions = output.loadingOptions))

    return Workflow(id = 'main',
                    requirements = requirements,
                    inputs = inputs,
                    outputs = outputs,
                    steps = steps)

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
    yaml = YAML()

    with open(workflow, "r") as f:
        workflow_dict = yaml.load(f)

    loading_options = LoadingOptions()
    cwls = {
        'stage-in': load_document_by_uri(path = stage_in, loadingOptions = loading_options),
        'workflow': load_document_by_yaml(yaml = workflow_dict, uri = Path(workflow).resolve().as_uri(), loadingOptions = loading_options, id_ = workflow_id, load_all = False),
        'stage-out': load_document_by_uri(path = stage_out, loadingOptions = loading_options),
    }

    workflow = build_workflow(cwls = cwls)

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        yaml.dump(save(workflow), f)

    logger.info(f"Raw workflow written to: {output_path}")

if __name__ == "__main__":
    main()
