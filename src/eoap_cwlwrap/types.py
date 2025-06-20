"""
CWL Chain Builder (c) 2025

CWL Chain Builder is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from cwl_utils.parser.cwl_v1_2 import ( Directory,
                                        CommandInputArraySchema,
                                        CommandOutputArraySchema,
                                        SchemaDefRequirement,
                                        Workflow )
from typing import Any
from builtins import isinstance

URL_SCHEMA = 'https://raw.githubusercontent.com/eoap/schemas/main/url.yaml'
__URL_TYPE__ = f"{URL_SCHEMA}#URL"

def are_cwl_types_identical(expected: Any, actual: Any) -> bool:
    """
    Recursively checks if two CWL types from cwl_utils.parser are identical in structure.
    
    Handles:
    - Named types (e.g., Directory, File)
    - Array schemas (multi-dimensional)
    - Unions (lists of types)

    :param expected: First CWL type
    :param actual: Second CWL type
    :return: True if structurally and semantically identical, else False
    """

    # Direct object identity
    if expected is actual:
        return True

    # Both are lists (i.e., union types)
    if isinstance(expected, list) and isinstance(actual, list):
        # Must match in length and all types
        return (
            len(expected) == len(actual)
            and all(any(are_cwl_types_identical(a, b) for b in actual) for a in expected)
        )

    # One is list, one is not: can't be identical
    if isinstance(expected, list) != isinstance(actual, list):
        return False

    # Array types (CommandInputArraySchema or CommandOutputArraySchema)
    array_types = (CommandInputArraySchema, CommandOutputArraySchema)
    if isinstance(expected, array_types) and isinstance(actual, array_types):
        return are_cwl_types_identical(expected.items, actual.items)

    # Class or base types (e.g., Directory, File)
    if isinstance(actual, type(expected)):
        return expected == actual

    # If one is class, the other is instance of that class
    if isinstance(expected, actual.__class__) and isinstance(actual, expected.__class__):
        return type(expected) == type(actual)

    return False

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

def is_url_compatible_type(typ: Any) -> bool:
    """
    Recursively check if a CWL v1.2 type is or contains a https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL,
    including unions and multi-dimensional arrays.
    
    :param typ: A CWLType (or nested list of types) from cwl_utils.parser
    :return: True if the type (even deeply nested) is a https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL, else False
    """

    # Case 1: Direct string reference
    if isinstance(typ, str) and typ == __URL_TYPE__:
        return True

    # Case 2: Union type (list of types)
    if isinstance(typ, list):
        return any(is_url_compatible_type(t) for t in typ)

    # Case 3: Array type (recursive item type check)
    if hasattr(typ, "items"):
        return is_url_compatible_type(typ.items)

    return False

def replace_directory_with_url(typ: Any) -> Any:
    """
    Recursively traverses the CWL type (from cwl_utils.parser.cwl_v1_2) and replaces
    every occurrence of `Directory` with the external schema reference:
    
        "https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL"

    :param typ: CWL type (can be primitive, list, or schema object)
    :return: Modified type with Directory replaced
    """

    # Base case: direct Directory type

    # case 0: Direct match with Directory class name
    if isinstance(typ, str) and typ == Directory.__name__:
        return __URL_TYPE__

    # Case 1: Direct match with Directory class
    if typ == Directory or isinstance(typ, Directory):
        return __URL_TYPE__

    # Union: list of types
    if isinstance(typ, list):
        return [replace_directory_with_url(t) for t in typ]

    # Array types
    if isinstance(typ, CommandInputArraySchema):
        return CommandInputArraySchema(
            extension_fields=typ.extension_fields,
            items=replace_directory_with_url(typ.items),
            type_=typ.type_,
            label=typ.label
        )

    if isinstance(typ, CommandOutputArraySchema):
        return CommandOutputArraySchema(
            extension_fields=typ.extension_fields,
            items=replace_directory_with_url(typ.items),
            type_=typ.type_,
            label=typ.label
        )

    # Return original type if no match
    return typ
