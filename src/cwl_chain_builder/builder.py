"""
CWL Chain Builder (c) 2025

CWL Chain Builder is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

import sys
import uuid
import click
from pathlib import Path
from typing import List

from ruamel.yaml import YAML
from cwl_utils.parser import load_document_by_uri, save

def build_workflow(step_paths: List[str], workflow_id: str):
    workflow = {
        "cwlVersion": "v1.2",
        "class": "Workflow",
        "id": workflow_id,
        "inputs": []
    }

    print(f"initial inputs: {workflow['inputs']}")

    for path in step_paths:
        current = load_document_by_uri(path=path)

        print(f"current inputs: {current.inputs}")

        workflow["inputs"] += current.inputs
    '''
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

    final_outputs = tools[-1].outputs
    outputs = [
        {
            "id": o.id,
            "outputSource": f"step{len(tools) - 1}/{o.id}",
            "type": getattr(o, "type", getattr(o, "type_", None))
        } for o in final_outputs
    ]

    inputs = [{"id": i.id, "type": getattr(i, "type", getattr(i, "type_", None))} for i in tools[0].inputs]

    workflow = {
        "cwlVersion": "v1.2",
        "class": "Workflow",
        "id": workflow_id,
        "inputs": inputs,
        "outputs": outputs,
        "steps": steps,
    }
    '''
    return workflow

@click.command()
@click.argument("steps", nargs=-1, type=click.Path(exists=True))
@click.option("--workflow-id", default=lambda: f"workflow_{uuid.uuid4().hex[:8]}", help="ID of the workflow")
@click.option("--output", "-o", type=click.Path(), required=True, help="Output file path")
def main(steps, workflow_id, output):
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    workflow = build_workflow(list(steps), workflow_id=workflow_id)

    yaml_dumper = YAML()
    with output_path.open("w") as f:
        yaml_dumper.dump(save(workflow), f)

    print(f"Raw workflow written to: {output_path}")

if __name__ == "__main__":
    main()
