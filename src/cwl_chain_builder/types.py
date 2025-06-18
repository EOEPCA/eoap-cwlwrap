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

URL_SCHEMA = 'https://raw.githubusercontent.com/eoap/schemas/main/url.yaml'
URL_TYPE = f"{URL_SCHEMA}#URL"
URL_SCHEMA_REQUIREMENT = SchemaDefRequirement(types=[ { '$import': URL_SCHEMA } ])

def append_url_schema_def_requirement(workflow_cwl: Workflow):
    if workflow_cwl.requirements:
        for requirement in workflow_cwl.requirements:
            if requirement.class_ == SchemaDefRequirement.__name__:
                if requirement.types:
                    requirement.types.append(URL_SCHEMA_REQUIREMENT.types[0])
                else:
                    requirement.types = URL_SCHEMA_REQUIREMENT.types
                return

        workflow_cwl.requirements.append(URL_SCHEMA_REQUIREMENT)
    else:
        workflow_cwl.requirements = [ URL_SCHEMA_REQUIREMENT ]

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
    if isinstance(expected, type) and isinstance(actual, type):
        return expected == actual

    # If one is class, the other is instance of that class
    if isinstance(expected, actual.__class__) and isinstance(actual, expected.__class__):
        return type(expected) == type(actual)

    return False

def is_url_type(actual_instance: Any) -> bool:
    """
    Recursively check if a CWL v1.2 type is or contains a https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL,
    including unions and multi-dimensional arrays.
    
    :param typ: A CWLType (or nested list of types) from cwl_utils.parser
    :return: True if the type (even deeply nested) is a https://raw.githubusercontent.com/eoap/schemas/main/url.yaml#URL, else False
    """

    # Case 1: Union type (list of types)
    if isinstance(actual_instance, str) and actual_instance == URL_TYPE:
        return True

    # Case 2: Union type (list of types)
    if isinstance(actual_instance, list):
        return any(is_url_type(t) for t in actual_instance)

    # Case 3: Array type (recursive item type check)
    if hasattr(actual_instance, "items"):
        return is_url_type(actual_instance.items)

    return False

def is_directory_type(actual_instance: Any) -> bool:
    """
    Recursively check if a CWL v1.2 type is or contains a Directory,
    including unions and multi-dimensional arrays.
    
    :param typ: A CWLType (or nested list of types) from cwl_utils.parser
    :return: True if the type (even deeply nested) is a Directory, else False
    """

    # case 0: Direct match with Directory class name
    if isinstance(actual_instance, str) and actual_instance == Directory.__name__:
        return True

    # Case 1: Direct match with Directory class
    if actual_instance == Directory or isinstance(actual_instance, Directory):
        return True

    # Case 2: Union type (list of types)
    if isinstance(actual_instance, list):
        return any(is_directory_type(t) for t in actual_instance)

    # Case 3: Array type (recursive item type check)
    if hasattr(actual_instance, "items"):
        return is_directory_type(actual_instance.items)

    # Case 4: Possibly a CWLType or raw class — extract and test
    if isinstance(actual_instance, type):
        return issubclass(actual_instance, Directory)

    return False
