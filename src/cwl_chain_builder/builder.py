"""
CWL Chain Builder (c) 2025

CWL Chain Builder is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from cwl_utils.parser import load_document_by_yaml
from pathlib import Path
from ruamel.yaml import YAML
from typing import List
import click
import sys
import uuid

def build_workflow(step_paths: List[str], workflow_id: str):
    yaml_loader = YAML()
    tools = []

    for path in step_paths:
        with open(path) as f:
            cwl_doc = yaml_loader.load(f)
            tool = load_document_by_yaml(cwl_doc, str(path))
            tools.append(tool)

    for i in range(1, len(tools)):
        prev_outputs = {o.id for o in tools[i - 1].outputs}
        curr_inputs = {i.id for i in tools[i].inputs}
        if not curr_inputs.issubset(prev_outputs):
            raise ValueError(f"Step {i}: input(s) {curr_inputs - prev_outputs} not satisfied by previous outputs.")

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
            "type": o.type
        } for o in final_outputs
    ]

    inputs = [{"id": i.id, "type": i.type} for i in tools[0].inputs]

    workflow = {
        "cwlVersion": "v1.2",
        "class": "Workflow",
        "id": workflow_id,
        "inputs": inputs,
        "outputs": outputs,
        "steps": steps,
    }

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
        yaml_dumper.dump(workflow, f)

    print(f"Raw workflow written to: {output_path}")

if __name__ == "__main__":
    main()
