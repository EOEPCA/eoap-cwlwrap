# Copyright 2025 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from . import wrap_locations
from cwl_loader import dump_cwl
from datetime import datetime
from loguru import logger
from pathlib import Path
from requests import Session
from session_adapters.file_adapter import FileAdapter
from session_adapters.s3_adapter import S3Adapter
from session_adapters.oci_adapter import OCIAdapter

import click
import time

@click.command()
@click.option("--directory-stage-in", required=False, help="The CWL stage-in URL or file for Directory derived types")
@click.option("--file-stage-in", required=False, help="The CWL stage-in URL or file for File derived types")
@click.option("--workflow", required=True, help="The CWL workflow URL or file")
@click.option("--workflow-id", required=False, help="ID of the workflow", deprecated="Use --workflow specifying the <CWL_URL#WF_ID> instead.",)
@click.option("--stage-out", required=False, deprecated="Use --directory-stage-out instead", help="The CWL stage-out URL or file")
@click.option("--directory-stage-out", required=False, help="The CWL stage-out URL or file for Directory derived types")
@click.option("--file-stage-out", required=False, help="The CWL stage-out URL or file for File derived types")
@click.option("--output", type=click.Path(path_type=Path), required=True, help="The output file path")
@click.option("--oci-hostname", envvar="OCI_HOSTNAME", show_envvar=True)
@click.option("--oci-username", envvar="OCI_USERNAME", show_envvar=True)
@click.option("--oci-password", envvar="OCI_PASSWORD", show_envvar=True)
def main(
    directory_stage_in: str,
    file_stage_in: str,
    workflow: str,
    workflow_id: str,
    stage_out: str,
    directory_stage_out: str,
    file_stage_out: str,
    output: Path,
    oci_hostname: str | None,
    oci_username: str | None,
    oci_password: str | None,
):
    '''
    Composes a CWL `Workflow` from a series of `Workflow`/`CommandLineTool` steps, defined according to [Application package patterns based on data stage-in and stage-out behaviors commonly used in EO workflows](https://github.com/eoap/application-package-patterns), and **packs** it into a single self-contained CWL document.
    '''
    start_time = time.time()

    session = Session()
    session.mount("file://", FileAdapter())
    session.mount("s3://", S3Adapter())
    session.mount(
        "oci://",
        OCIAdapter(hostname=oci_hostname, username=oci_username, password=oci_password),
    )

    main_workflow = wrap_locations(
        session=session,
        directory_stage_in=directory_stage_in,
        file_stage_in=file_stage_in,
        workflows=f"{workflow}#{workflow_id}" if "#" not in workflow and workflow_id else workflow,
        directory_stage_out=stage_out if stage_out else directory_stage_out,
        file_stage_out=file_stage_out
    )

    logger.info('------------------------------------------------------------------------')
    logger.info('BUILD SUCCESS')
    logger.info('------------------------------------------------------------------------')

    logger.info(f"Saving the new Workflow to {output}...")

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w") as f:
        dump_cwl(main_workflow, f)

    logger.info(f"New Workflow successfully saved to {output.absolute()}!")

    end_time = time.time()

    logger.info(f"Total time: {end_time - start_time:.4f} seconds")
    logger.info(f"Finished at: {datetime.fromtimestamp(end_time).isoformat(timespec='milliseconds')}")

if __name__ == "__main__":
    main()
