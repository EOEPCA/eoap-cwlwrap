# `eoap_cwlwrap.types`

Type utilities and validators used by the workflow wrapper.

Compatibility helpers inspect CWL type names, unions, and array item types.
Conversion helpers replace matching types with the EOAP URI type identified by
`URL_TYPE`, preserving union members and array structure.

Stage-in validators require exactly one URI-compatible input and exactly one
output compatible with the requested `Directory` or `File` type. Stage-out
validators require exactly one compatible `Directory` or `File` input and
exactly one URI-compatible output. Invalid staging contracts raise
`transpiler_mate.api.PluginFailureError`.

::: eoap_cwlwrap.types
    options:
      members:
        - Directory_or_File
        - URL_SCHEMA
        - URL_TYPE
        - is_nullable
        - is_type_assignable_to
        - get_assignable_type
        - is_directory_compatible_type
        - is_file_compatible_type
        - is_directory_or_file_compatible_type
        - is_uri_compatible_type
        - is_array_type
        - replace_type_with_url
        - replace_directory_with_url
        - type_to_string
        - validate_directory_stage_in
        - validate_file_stage_in
        - validate_directory_stage_out
        - validate_file_stage_out
      members_order: source
      show_root_full_path: false
      show_root_heading: false
      show_root_toc_entry: false
      show_source: false
