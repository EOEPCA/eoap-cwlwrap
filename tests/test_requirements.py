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

import unittest

from cwl_utils.parser.cwl_v1_2 import CommandLineTool, ResourceRequirement

from eoap_cwlwrap.requirements import (
    DEFAULT_CORES_MAX,
    DEFAULT_RAM_MAX,
    adjust_resource_requirements,
    get_feature_requirement,
)


class TestRequirements(unittest.TestCase):
    def _command_line_tool(
        self, resource_requirement: ResourceRequirement | None = None
    ) -> CommandLineTool:
        return CommandLineTool(
            id="tool",
            inputs=[],
            outputs=[],
            requirements=[resource_requirement] if resource_requirement else None,
        )

    def _resource_requirement(self, tool: CommandLineTool) -> ResourceRequirement:
        resource_requirement = get_feature_requirement(ResourceRequirement, tool)
        self.assertIsNotNone(resource_requirement)
        assert resource_requirement is not None
        return resource_requirement

    def test_adjust_resource_requirements_adds_default_resource_requirement(
        self,
    ) -> None:
        tool = self._command_line_tool()

        adjust_resource_requirements(tool)

        resource_requirement = self._resource_requirement(tool)
        self.assertEqual(resource_requirement.ramMax, DEFAULT_RAM_MAX)
        self.assertEqual(resource_requirement.ramMin, resource_requirement.ramMax)
        self.assertEqual(resource_requirement.coresMax, DEFAULT_CORES_MAX)
        self.assertEqual(resource_requirement.coresMin, resource_requirement.coresMax)

    def test_adjust_resource_requirements_caps_minimums_to_defaults(
        self,
    ) -> None:
        ram_max = DEFAULT_RAM_MAX + 1024
        cores_max = DEFAULT_CORES_MAX + 2
        tool = self._command_line_tool(
            ResourceRequirement(ramMax=ram_max, coresMax=cores_max)
        )

        adjust_resource_requirements(tool)

        resource_requirement = self._resource_requirement(tool)
        self.assertEqual(resource_requirement.ramMax, ram_max)
        self.assertEqual(resource_requirement.ramMin, DEFAULT_RAM_MAX)
        self.assertEqual(resource_requirement.coresMax, cores_max)
        self.assertEqual(resource_requirement.coresMin, DEFAULT_CORES_MAX)

    def test_adjust_resource_requirements_uses_maximums_below_defaults(
        self,
    ) -> None:
        ram_max = DEFAULT_RAM_MAX - 512
        cores_max = DEFAULT_CORES_MAX - 1
        tool = self._command_line_tool(
            ResourceRequirement(ramMax=ram_max, coresMax=cores_max)
        )

        adjust_resource_requirements(tool)

        resource_requirement = self._resource_requirement(tool)
        self.assertEqual(resource_requirement.ramMax, ram_max)
        self.assertEqual(resource_requirement.ramMin, ram_max)
        self.assertEqual(resource_requirement.coresMax, cores_max)
        self.assertEqual(resource_requirement.coresMin, cores_max)

    def test_adjust_resource_requirements_uses_maximums_equal_to_defaults(
        self,
    ) -> None:
        tool = self._command_line_tool(
            ResourceRequirement(
                ramMax=DEFAULT_RAM_MAX,
                coresMax=DEFAULT_CORES_MAX,
            )
        )

        adjust_resource_requirements(tool)

        resource_requirement = self._resource_requirement(tool)
        self.assertEqual(resource_requirement.ramMax, DEFAULT_RAM_MAX)
        self.assertEqual(resource_requirement.ramMin, DEFAULT_RAM_MAX)
        self.assertEqual(resource_requirement.coresMax, DEFAULT_CORES_MAX)
        self.assertEqual(resource_requirement.coresMin, DEFAULT_CORES_MAX)
