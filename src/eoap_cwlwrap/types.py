"""
EOAP CWLWrap (c) 2025

EOAP CWLWrap is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from cwl_utils.parser.cwl_v1_2 import ( Directory,
                                        CommandInputArraySchema,
                                        CommandOutputArraySchema,
                                        InputArraySchema,
                                        OutputArraySchema,
                                        SchemaDefRequirement,
                                        Workflow )
from typing import Any, Union
import sys

Workflows = Union[Workflow, list[Workflow]]

URL_SCHEMA = 'https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml'
URL_TYPE = f"{URL_SCHEMA}#URI"

def is_nullable(typ: Any) -> bool:
    return isinstance(typ, list) and 'null' in typ

def is_directory_compatible_type(typ: Any) -> bool:
    """
    Recursively check if a CWL v1.2 type is or contains a Directory,
    including unions and multi-dimensional arrays.
    
    :param typ: A CWLType (or nested list of types) from cwl_utils.parser
    :return: True if the type (even deeply nested) is a Directory, else False
    """

    # Case 0: Direct string reference
    if isinstance(typ, str) and typ == Directory.__name__:
        return True

    # Case 1: Direct match with Directory class
    if typ == Directory or isinstance(typ, Directory):
        return True

    # Case 2: Union type (list of types)
    if isinstance(typ, list):
        return any(is_directory_compatible_type(t) for t in typ)

    # Case 3: Array type (recursive item type check)
    if hasattr(typ, "items"):
        return is_directory_compatible_type(typ.items)

    # Case 4: Possibly a CWLType or raw class — extract and test
    if isinstance(typ, type):
        return issubclass(typ, Directory)

    return False

def is_uri_compatible_type(typ: Any) -> bool:
    """
    Recursively check if a CWL v1.2 type is or contains a https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI,
    including unions and multi-dimensional arrays.
    
    :param typ: A CWLType (or nested list of types) from cwl_utils.parser
    :return: True if the type (even deeply nested) is a https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI, else False
    """

    # Case 1: Direct string reference
    if isinstance(typ, str) and typ == URL_TYPE:
        return True

    # Case 2: Union type (list of types)
    if isinstance(typ, list):
        return any(is_uri_compatible_type(t) for t in typ)

    # Case 3: Array type (recursive item type check)
    if hasattr(typ, "items"):
        return is_uri_compatible_type(typ.items)

    return False

def is_array_type(typ: Any) -> bool:
    if isinstance(typ, list):
        return any(is_array_type(type_item) for type_item in list(typ))

    return hasattr(typ, "items")

def replace_directory_with_url(typ: Any) -> Any:
    """
    Recursively traverses the CWL type (from cwl_utils.parser.cwl_v1_2) and replaces
    every occurrence of `Directory` with the external schema reference:
    
        "https://raw.githubusercontent.com/eoap/schemas/main/string_format.yaml#URI"

    :param typ: CWL type (can be primitive, list, or schema object)
    :return: Modified type with Directory replaced
    """

    # Base case: direct Directory type

    # case 0: Direct match with Directory class name
    if isinstance(typ, str) and typ == Directory.__name__:
        return URL_TYPE

    # Case 1: Direct match with Directory class
    if typ == Directory or isinstance(typ, Directory):
        return URL_TYPE

    # Union: list of types
    if isinstance(typ, list):
        return [replace_directory_with_url(t) for t in typ]

    # Array types
    if isinstance(typ, InputArraySchema) or isinstance(typ, CommandInputArraySchema):
        return InputArraySchema(
            extension_fields=typ.extension_fields,
            items=replace_directory_with_url(typ.items),
            type_=typ.type_,
            label=typ.label,
            doc=typ.doc
        )

    if isinstance(typ, OutputArraySchema) or isinstance(typ, CommandOutputArraySchema):
        return OutputArraySchema(
            extension_fields=typ.extension_fields,
            items=replace_directory_with_url(typ.items),
            type_=typ.type_,
            label=typ.label,
            doc=typ.doc
        )

    # Return original type if no match
    return typ

def type_to_string(typ: Any) -> str:
    if isinstance(typ, list):
        return f"[ {', '.join([type_to_string(t) for t in typ])} ]"

    if hasattr(typ, "items"):
        return f"{type_to_string(typ.items)}[]"

    if isinstance(typ, str):
        return typ

    return typ.__name__

def _create_error_message(parameters: list[Any]) -> str:
    return 'no' if 0 == len(parameters) else str(list(map(lambda parameter: parameter.id, parameters)))

def validate_stage_in(stage_in: Workflow):
    print(f"Validating stage-in '{stage_in.id}'...")

    url_inputs = list(
        filter(
            lambda input: is_uri_compatible_type(input.type_),
            stage_in.inputs
        )
    )

    if len(url_inputs) != 1:
        sys.exit(f"stage-in '{stage_in.id}' not valid, {_create_error_message(url_inputs)} URL-compatible input found, please specify one.")

    directory_outputs = list(
        filter(
            lambda output: is_directory_compatible_type(output.type_),
            stage_in.outputs
        )
    )

    if len(directory_outputs) != 1:
        sys.exit(f"stage-in '{stage_in.id}' not valid, {_create_error_message(directory_outputs)} Directory-compatible output found, please specify one.")

    print(f"stage-in '{stage_in.id}' is valid")

def validate_stage_out(stage_out: Workflow):
    print(f"Validating stage-out '{stage_out.id}'...")

    directory_inputs = list(
        filter(
            lambda input: is_directory_compatible_type(input.type_),
            stage_out.inputs
        )
    )

    if len(directory_inputs) != 1:
        sys.exit(f"stage-out '{stage_out.id}' not valid, {_create_error_message(directory_inputs)} Directory-compatible input found, please specify one.")

    url_outputs = list(
        filter(
            lambda output: is_uri_compatible_type(output.type_),
            stage_out.outputs
        )
    )

    if len(url_outputs) != 1:
        sys.exit(f"stage-out '{stage_out.id}' not valid, {_create_error_message(url_outputs)} URL-compatible output found, please specify one.")

    print(f"stage-out '{stage_out.id}' is valid")
