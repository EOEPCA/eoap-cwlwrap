# Copyright 2026 Terradue
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


from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any

from cwl_utils.parser import Process, save
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field
from ruamel.yaml import YAML
from transpiler_mate.api import (
    PluginExecutionError,
    transpiler_plugin,
)

from . import wrap
from .requirements import adjust_resource_requirements

if TYPE_CHECKING:
    from collections.abc import MutableSequence

    from schema_salad.runtime import Saveable
    from transpiler_mate.api import TranspilerContext


class CwlWrapOptions(BaseModel):
    """Options accepted by the {{ project_name }} plugin."""

    model_config = ConfigDict(extra="forbid")

    directory_stage_in: Annotated[
        str | None,
        Field(
            default=None,
            description="The CWL stage-in URL or file for Directory derived types",
        ),
    ] = None

    file_stage_in: Annotated[
        str | None,
        Field(
            default=None,
            description="The CWL stage-in URL or file for File derived types",
        ),
    ] = None

    directory_stage_out: Annotated[
        str | None,
        Field(
            default=None,
            description="The CWL stage-out URL or file for Directory derived types",
        ),
    ] = None

    file_stage_out: Annotated[
        str | None,
        Field(
            default=None,
            description="The CWL stage-out URL or file for File derived types",
        ),
    ] = None

    output: Annotated[
        Path,
        Field(default=Path("wrapped.cwl"), description="The output file path"),
    ]


def _resolve_stage_context(
    parent: TranspilerContext, location: str | None
) -> TranspilerContext | None:
    return parent.resolver.resolve(location) if location else None


def _get_stage_process(context: TranspilerContext | None) -> Process | None:
    if context:
        if context.process_id:
            return context.resolved_process

        if len(context.document) != 1:
            raise PluginExecutionError(
                f"Process $graph found from {context.source}, but no #<process-id> specified in input CWL document"
            )

        return next(iter(context.processes))

    return None


@transpiler_plugin(
    name="cwlwrap",
    description="Composes a CWL `Workflow` from a series of `Workflow`/`CommandLineTool` steps, defined according to [Application package patterns based on data stage-in and stage-out behaviors commonly used in EO workflows](https://github.com/eoap/application-package-patterns), and **packs** it into a single self-contained CWL document.",
    options_model=CwlWrapOptions,
)
def cwlwrap(context: TranspilerContext, options: CwlWrapOptions) -> None:
    """Composes a CWL `Workflow` from a series of `Workflow`/`CommandLineTool` steps, defined according to [Application package patterns based on data stage-in and stage-out behaviors commonly used in EO workflows](https://github.com/eoap/application-package-patterns), and **packs** it into a single self-contained CWL document."""
    directory_stage_in: TranspilerContext | None = _resolve_stage_context(
        context, options.directory_stage_in
    )
    file_stage_in: TranspilerContext | None = _resolve_stage_context(
        context, options.file_stage_in
    )
    directory_stage_out: TranspilerContext | None = _resolve_stage_context(
        context, options.directory_stage_out
    )
    file_stage_out: TranspilerContext | None = _resolve_stage_context(
        context, options.file_stage_out
    )

    main_wf: Process = wrap(
        workflow=context.resolved_process,
        directory_stage_in=_get_stage_process(directory_stage_in),
        file_stage_in=_get_stage_process(file_stage_in),
        directory_stage_out=_get_stage_process(directory_stage_out),
        file_stage_out=_get_stage_process(file_stage_out),
    )

    wrapper_cwl: MutableSequence[Saveable] = []

    def _append_process(p: Process) -> None:
        adjust_resource_requirements(p)
        wrapper_cwl.append(p)

    _append_process(main_wf)

    for current_context in (
        directory_stage_in,
        file_stage_in,
        context,
        directory_stage_out,
        file_stage_out,
    ):
        if current_context:
            for wf in current_context.processes:
                _append_process(wf)

    try:
        options.output.parent.mkdir(parents=True, exist_ok=True)

        data: Any = save(
            val=wrapper_cwl,
            relative_uris=False,
        )

        with options.output.open("w") as output_stream:
            YAML().dump(data=data, stream=output_stream)

        logger.info(f"New Workflow successfully saved to {options.output.absolute()}!")
    except Exception as e:
        raise PluginExecutionError(
            f"An error occurred when serializing to {options.output.absolute()}, see nested exception"
        ) from e
