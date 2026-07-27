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

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from cwl_utils.parser import Process
from cwl_utils.parser.cwl_v1_2 import (
    CommandLineTool,
    ProcessRequirement,
    ResourceRequirement,
    SchemaDefRequirement,
)
from loguru import logger

DEFAULT_CORES_MAX: int = 2

DEFAULT_RAM_MAX: int = 2000

_ProcessRequirementType = TypeVar("_ProcessRequirementType", bound=ProcessRequirement)


def get_feature_requirement(
    requirement_type: type[_ProcessRequirementType], workflow: Process
) -> _ProcessRequirementType | None:
    if workflow.requirements:
        for current_requirement in workflow.requirements:
            if requirement_type.__name__ == current_requirement.class_:
                return cast("_ProcessRequirementType", current_requirement)
    return None


def contains_feature_requirement(
    requirement_type: type[ProcessRequirement], workflow: Process
) -> bool:
    return get_feature_requirement(requirement_type, workflow) is not None


def add_feature_requirement(requirement: ProcessRequirement, workflow: Process) -> bool:
    if not workflow.requirements:
        workflow.requirements = [requirement]
        return True
    if not contains_feature_requirement(type(requirement), workflow):
        workflow.requirements.append(requirement)
        return True

    return False


def get_schema_def_import(type_: Any) -> str | None:
    name = None
    if isinstance(type_, Mapping):
        import_ = type_.get("$import")
        if isinstance(import_, str):
            return import_

        name = type_.get("name")
    else:
        name = getattr(type_, "name", None)

    if isinstance(name, str) and "#" in name:
        return name.split("#")[0]

    return None


def copy_schema_def_requirement(
    requirement: SchemaDefRequirement,
) -> SchemaDefRequirement:
    return SchemaDefRequirement(
        types=list(requirement.types)
        if isinstance(requirement.types, list)
        else requirement.types,
        extension_fields=requirement.extension_fields,
        loadingOptions=requirement.loadingOptions,
    )


def merge_schema_def_imports(
    requirement: SchemaDefRequirement, imports: set[str]
) -> None:
    if isinstance(requirement.types, list):
        types = list(requirement.types)
    elif requirement.types:
        types = [requirement.types]
    else:
        types = []

    existing_imports = set()
    for type_ in types:
        import_ = get_schema_def_import(type_)
        if import_:
            existing_imports.add(import_)

    for import_ in sorted(imports):
        if import_ not in existing_imports:
            types.append({"$import": import_})

    requirement.types = types


def _get_minimum_requirement(default_min: int, current_max: Any) -> Any:
    if isinstance(current_max, (int, float)):
        return min(default_min, current_max)

    return current_max


def adjust_resource_requirements(workflow: list[Process]) -> None:
    for process in workflow:
        logger.debug(f"- Checking ResourceRequirement in {process.id}...")

        if isinstance(process, CommandLineTool):
            resource_requirement = get_feature_requirement(ResourceRequirement, process)

            if resource_requirement is None:
                resource_requirement = ResourceRequirement(
                    coresMax=DEFAULT_CORES_MAX,
                    ramMax=DEFAULT_RAM_MAX,
                )
                add_feature_requirement(
                    resource_requirement,
                    process,
                )

            for min_requirement, max_requirement, default_min in (
                ("ramMin", "ramMax", DEFAULT_RAM_MAX),
                ("coresMin", "coresMax", DEFAULT_CORES_MAX),
            ):
                current_min = getattr(resource_requirement, min_requirement)
                current_max = getattr(resource_requirement, max_requirement)

                if current_min is None and current_max is not None:
                    setattr(
                        resource_requirement,
                        min_requirement,
                        _get_minimum_requirement(default_min, current_max),
                    )
                elif current_max is None and current_min is not None:
                    setattr(resource_requirement, max_requirement, current_min)

            logger.debug(
                f"  ResourceRequirement in {process.id} adjusted to {resource_requirement.__dict__}"
            )
        else:
            logger.debug(f"  {process.id} is not a CommandLineTool instance, skipping.")
