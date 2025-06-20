"""
EOAP CWLWrap (c) 2025

EOAP CWLWrap is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from .types import Workflows
from cwl_utils.parser import load_document_by_yaml, save
from cwl_utils.parser.cwl_v1_2 import Workflow
from cwltool.load_tool import default_loader
from cwltool.update import update
from ruamel.yaml import YAML
from pathlib import Path
from typing import Any

__TARGET_CWL_VERSION__ = 'v1.2'

yaml = YAML()

def _clean_workflow(workflow: Workflow):
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
                step.run = f"#{step.run.split('#')[-1]}"

def load_workflow(path: str) -> Workflows:
    print(f"Loading CWL document from {path}...")

    with open(path, 'r') as workflow_stream:
        raw_workflow = yaml.load(workflow_stream)

    print(f"Raw CWL document successfully loaded from {path}! Now updating the model to v1.2...")

    updated_workflow = update(
        doc=raw_workflow,
        loader=default_loader(),
        baseuri=path,
        enable_dev=False,
        metadata={'cwlVersion': __TARGET_CWL_VERSION__},
        update_to=__TARGET_CWL_VERSION__
    )

    print('Raw CWL document successfully updated! Now converting to the CWL model...')

    workflow = load_document_by_yaml(
        yaml=updated_workflow,
        uri=path,
        load_all=True
    )

    print('Raw CWL document successfully updated! Now dereferencing the FQNs...')

    if isinstance(workflow, list):
        for wf in workflow:
            _clean_workflow(wf)
    else:
        _clean_workflow(workflow)

    print(f"CWL document successfully dereferenced!")

    return workflow

def dump_workflow(workflow: Workflows, output: str):
    print(f"Saving the new Workflow to {output}...")

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w") as f:
        yaml.dump(
            save(
                val=workflow,
                relative_uris=False
            ),
        f)

    print(f"New Workflow successfully saved to {output}!")
