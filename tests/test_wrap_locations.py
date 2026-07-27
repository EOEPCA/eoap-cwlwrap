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

import re
import unittest
from collections.abc import Callable
from unittest.mock import patch

from cwl_utils.parser.cwl_v1_2 import Workflow
from requests import Session

from eoap_cwlwrap import _load_process_from_location, wrap_locations


class TestLoadProcessFromLocation(unittest.TestCase):
    def test_selects_process_from_graph(self) -> None:
        first = Workflow(id="first", inputs=[], outputs=[], steps=[])
        selected = Workflow(id="selected", inputs=[], outputs=[], steps=[])
        graph = [first, selected]

        with patch("eoap_cwlwrap.load_cwl_from_location", return_value=graph):
            parsed, process = _load_process_from_location(
                path="workflow.cwl#selected", kind="main", session=Session()
            )

        self.assertIs(parsed, graph)
        self.assertIs(process, selected)

    def test_rejects_graph_without_process_id(self) -> None:
        graph = [Workflow(id="available", inputs=[], outputs=[], steps=[])]

        with (
            patch("eoap_cwlwrap.load_cwl_from_location", return_value=graph),
            self.assertRaisesRegex(
                ValueError,
                r"no process id was provided.*available",
            ),
        ):
            _load_process_from_location(
                path="workflow.cwl", kind="main", session=Session()
            )

    def test_rejects_unknown_process_id(self) -> None:
        graph = [Workflow(id="available", inputs=[], outputs=[], steps=[])]

        with (
            patch("eoap_cwlwrap.load_cwl_from_location", return_value=graph),
            self.assertRaisesRegex(
                ValueError,
                r"Process missing does not exist.*available",
            ),
        ):
            _load_process_from_location(
                path="workflow.cwl#missing", kind="main", session=Session()
            )

    def test_selects_matching_id_from_single_process_document(self) -> None:
        workflow = Workflow(id="selected", inputs=[], outputs=[], steps=[])

        with patch("eoap_cwlwrap.load_cwl_from_location", return_value=workflow):
            parsed, process = _load_process_from_location(
                path="workflow.cwl#selected", kind="main", session=Session()
            )

        self.assertIs(parsed, workflow)
        self.assertIs(process, workflow)

    def test_rejects_unknown_id_for_single_process_document(self) -> None:
        workflow = Workflow(id="available", inputs=[], outputs=[], steps=[])

        with (
            patch("eoap_cwlwrap.load_cwl_from_location", return_value=workflow),
            self.assertRaisesRegex(
                ValueError,
                r"Process missing does not exist.*available",
            ),
        ):
            _load_process_from_location(
                path="workflow.cwl#missing", kind="main", session=Session()
            )

    def test_rejects_empty_process_id_without_loading_document(self) -> None:
        with (
            patch("eoap_cwlwrap.load_cwl_from_location") as load_cwl,
            self.assertRaisesRegex(ValueError, r"Empty process id"),
        ):
            _load_process_from_location(
                path="workflow.cwl#", kind="main", session=Session()
            )

        load_cwl.assert_not_called()


class TestWrapLocations(unittest.TestCase):
    def _assert_duplicate_stage_id_rejected(
        self,
        invoke_wrap_locations: Callable[[], object],
        kind: str,
        stage_name: str,
    ) -> None:
        duplicate_id = "already-defined"
        workflow = Workflow(id=duplicate_id, inputs=[], outputs=[], steps=[])
        stage = Workflow(id=duplicate_id, inputs=[], outputs=[], steps=[])
        stage_location = "stage.cwl"
        expected_message = (
            f"Cannot import Workflow {duplicate_id} {stage_name} declared in "
            f"{stage_location}, 'id' already present in wrapped CWL document"
        )

        with (
            patch(
                "eoap_cwlwrap._load_process_from_location",
                side_effect=[([workflow], workflow), (stage, stage)],
            ) as load_process,
            self.assertRaisesRegex(ValueError, re.escape(expected_message)),
        ):
            invoke_wrap_locations()

        self.assertEqual(load_process.call_count, 2)
        self.assertEqual(load_process.call_args_list[0].kwargs["kind"], "main")
        self.assertEqual(load_process.call_args_list[1].kwargs["kind"], kind)

    def test_rejects_directory_stage_in_with_duplicate_id(self) -> None:
        self._assert_duplicate_stage_id_rejected(
            lambda: wrap_locations(
                workflows="workflow.cwl", directory_stage_in="stage.cwl"
            ),
            "directory-stage-in",
            "Directory Stage-In",
        )

    def test_rejects_directory_stage_out_with_duplicate_id(self) -> None:
        self._assert_duplicate_stage_id_rejected(
            lambda: wrap_locations(
                workflows="workflow.cwl", directory_stage_out="stage.cwl"
            ),
            "directory-stage-out",
            "Directory Stage-Out",
        )

    def test_rejects_file_stage_in_with_duplicate_id(self) -> None:
        self._assert_duplicate_stage_id_rejected(
            lambda: wrap_locations(workflows="workflow.cwl", file_stage_in="stage.cwl"),
            "file-stage-in",
            "File Stage-In",
        )

    def test_rejects_file_stage_out_with_duplicate_id(self) -> None:
        self._assert_duplicate_stage_id_rejected(
            lambda: wrap_locations(
                workflows="workflow.cwl", file_stage_out="stage.cwl"
            ),
            "file-stage-out",
            "File Stage-Out",
        )
