"""
EOAP CWLWrap (c) 2025

EOAP CWLWrap is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from . import wrap
from .loader import ( load_workflow,
                      dump_workflow )
from .pumler import to_puml
from datetime import datetime
import click
import time

@click.command()
@click.option("--stage-in", required=True, help="The CWL stage-in file")
@click.option("--workflow", required=True, help="The CWL workflow file")
@click.option("--workflow-id", required=True, help="ID of the workflow")
@click.option("--stage-out", required=True, help="The CWL stage-out file")
@click.option("--output", type=click.Path(), required=True, help="Output file path")
@click.option('--puml', is_flag=True, help="Serializes the workflow as PlantUML diagram.")
def main(stage_in: str,
         workflow: str,
         workflow_id: str,
         stage_out: str,
         output: str,
         puml: bool):
    start_time = time.time()

    stage_in_cwl = load_workflow(path=stage_in)

    print('------------------------------------------------------------------------')

    workflows_cwl = load_workflow(path=workflow)

    print('------------------------------------------------------------------------')

    stage_out_cwl = load_workflow(path=stage_out)

    print('------------------------------------------------------------------------')

    main_workflow = wrap(
        stage_in=stage_in_cwl,
        workflows=workflows_cwl,
        workflow_id=workflow_id,
        stage_out=stage_out_cwl
    )

    print('------------------------------------------------------------------------')
    print('BUILD SUCCESS')
    print('------------------------------------------------------------------------')

    dump_workflow(main_workflow, output)

    print('------------------------------------------------------------------------')

    if puml:
        to_puml(
            workflows=main_workflow,
            output=output
        )

        print('------------------------------------------------------------------------')

    end_time = time.time()

    print(f"Total time: {end_time - start_time:.4f} seconds")
    print(f"Finished at: {datetime.fromtimestamp(end_time).isoformat(timespec='milliseconds')}")

if __name__ == "__main__":
    main()
