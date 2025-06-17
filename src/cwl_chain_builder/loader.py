"""
CWL Chain Builder (c) 2025

CWL Chain Builder is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

TARGET_CWL_VERSION = 'v1.2'

from cwl_utils.parser import load_document_by_yaml
from cwltool.load_tool import default_loader
from cwltool.update import update
from ruamel.yaml import YAML
from typing import Any

def clean_workflow(workflow: Any):
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

def load_workflow(path: str, yaml: YAML) -> Any:
    print(f"Loading CWL document from {path}...")

    with open(path, 'r') as workflow_stream:
        raw_workflow = yaml.load(workflow_stream)

    print(f"Raw CWL document successfully loaded from {path}! Now updating the model to v1.2...")

    updated_workflow = update(
        doc=raw_workflow,
        loader=default_loader(),
        baseuri=path,
        enable_dev=False,
        metadata={'cwlVersion': TARGET_CWL_VERSION},
        update_to=TARGET_CWL_VERSION
    )

    print('Raw CWL document successfully updated! Now converting to the CWL model...')

    workflow = load_document_by_yaml(
        yaml=updated_workflow,
        uri=path,
        load_all=True
    )

    print('aw CWL document successfully updated! Now dereferencing the FQNs...')

    if isinstance(workflow, list):
        for wf in workflow:
            clean_workflow(wf)
    else:
        clean_workflow(workflow)

    print(f"CWL document successfully dereferenced!")
    print('------------------------------------------------------------------------')

    return workflow
