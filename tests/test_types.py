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

import pytest
from cwl_utils.parser.cwl_v1_2 import (
    CommandInputArraySchema,
    CommandOutputArraySchema,
    Directory,
    InputArraySchema,
    OutputArraySchema,
)

from eoap_cwlwrap.types import (
    URL_TYPE,
    Directory_or_File,
    is_type_assignable_to,
    replace_type_with_url,
)


@pytest.mark.parametrize("target", [Directory, "Directory"])
def test_replaces_nullable_directory_and_preserves_other_strings(
    target: type[Directory] | str,
) -> None:
    assert replace_type_with_url(["null", "Directory", "string"], target) == [
        "null",
        URL_TYPE,
        "string",
    ]


@pytest.mark.parametrize(
    ("schema", "expected_schema"),
    [
        (InputArraySchema, InputArraySchema),
        (CommandInputArraySchema, InputArraySchema),
        (OutputArraySchema, OutputArraySchema),
        (CommandOutputArraySchema, OutputArraySchema),
    ],
)
def test_replaces_array_items_without_mutating_source(
    schema: type[InputArraySchema]
    | type[CommandInputArraySchema]
    | type[OutputArraySchema]
    | type[CommandOutputArraySchema],
    expected_schema: type[InputArraySchema] | type[OutputArraySchema],
) -> None:
    source = schema(items=["null", "Directory"], type_="array", label="Data", doc="Staged data")
    result = replace_type_with_url(source, Directory)
    assert isinstance(result, expected_schema)
    assert result.items == ["null", URL_TYPE]
    assert result.label == source.label
    assert result.doc == source.doc
    assert source.items == ["null", "Directory"]


def test_union_target_preserves_first_matching_type_behavior() -> None:
    assert replace_type_with_url("File", Directory_or_File) == URL_TYPE
    assert replace_type_with_url("string", Directory_or_File) is None


def test_assignability_recurses_through_nullable_arrays() -> None:
    source = InputArraySchema(items=["null", "Directory"], type_="array")
    assert is_type_assignable_to(source, Directory)
    assert not is_type_assignable_to("string", Directory)
