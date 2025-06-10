"""
CWL Chain Builder (c) 2025

CWL Chain Builder is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from cwl_utils.parser import load_document_by_uri, save
from cwl_utils.parser.cwl_v1_2 import CommandInputRecordSchema, LoadingOptions, SchemaDefRequirement, Workflow, WorkflowInputParameter, WorkflowOutputParameter
from pathlib import Path
from ruamel.yaml import YAML
import click
import sys
import uuid
from loguru import logger

def build_workflow(workflow_id: str, workflows: []) -> Workflow:
    requirements = [ SchemaDefRequirement(types=[ { '$import': 'https://raw.githubusercontent.com/eoap/schemas/main/url.yaml' } ]) ]

    inputs = []
    outputs = []
    steps = []

    # inputs
    for workflow in workflows:
        for input in workflow.inputs:
            inputs.append(WorkflowInputParameter(id = input.id.split('#')[-1].split('/')[-1],
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

    # outputs
    for output in workflows[-1].outputs:
        outputs.append(WorkflowOutputParameter(id = output.id.split('#')[-1].split('/')[-1],
                                               outputSource = [ output.id.split('#')[-1] ],
                                               type_ = output.type_,
                                               label = output.label,
                                               secondaryFiles = output.secondaryFiles,
                                               streamable = output.streamable,
                                               doc = output.doc,
                                               format = output.format,
                                               extension_fields = output.extension_fields,
                                               loadingOptions = output.loadingOptions))

    return Workflow(id=workflow_id,
                    requirements=requirements,
                    inputs=inputs,
                    outputs=outputs,
                    steps=steps)

'''
def build_workflow(yaml: YAML,
                   loader: Loader,
                   step_paths: List[str],
                   workflow_id: str):

    for i in range(1, len(tools)):
        prev_outputs = {o.id.split('#')[-1]: getattr(o, 'type', getattr(o, 'type_', None)) for o in tools[i - 1].outputs}
        curr_inputs = {i.id.split('#')[-1]: getattr(i, 'type', getattr(i, 'type_', None)) for i in tools[i].inputs}

        missing = set(curr_inputs) - set(prev_outputs)
        if missing:
            expected = {i.id: getattr(i, "type", getattr(i, "type_", None)) for i in tools[i].inputs if i.id.split('#')[-1] in missing}
            found = set(prev_outputs)
            raise ValueError(
                f"Step {i}: input(s) {missing} not satisfied by previous outputs. "
                f"Expected types: {expected} but found {found}"
            )

    steps = []
    for i, tool in enumerate(tools):
        tool_id = f"step{i}"
        steps.append({
            "id": tool_id,
            "run": tool.id,
            "in": [{"id": i.id} for i in tool.inputs],
            "out": [o.id for o in tool.outputs],
        })
'''

@click.command()
@click.argument("cwl_paths", nargs=-1, type=click.Path(exists=True))
@click.option("--workflow-id", default=lambda: f"workflow_{uuid.uuid4().hex[:8]}", help="ID of the workflow")
@click.option("--output", "-o", type=click.Path(), required=True, help="Output file path")
def main(cwl_paths, workflow_id, output):
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    workflows = []

    loading_options = LoadingOptions()

    for cwl_path in list(cwl_paths):
        logger.info(f"Parsing {cwl_path} CWL document...")

        current = load_document_by_uri(path = cwl_path, loadingOptions = loading_options)

        logger.info(f"Parsed current CWL: {type(current)}")

        workflows.append(current)

    workflow = build_workflow(workflow_id = workflow_id, workflows = workflows)

    yaml = YAML()
    with output_path.open("w") as f:
        yaml.dump(save(workflow), f)

    logger.info(f"Raw workflow written to: {output_path}")

if __name__ == "__main__":
    main()
