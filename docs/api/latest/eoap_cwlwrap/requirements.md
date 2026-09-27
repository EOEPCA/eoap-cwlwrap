# `eoap_cwlwrap.requirements`

Utilities for inspecting and updating CWL feature, schema, and resource
requirements. Feature requirement lookup checks `requirements`, not `hints`.
`add_feature_requirement` mutates the process only when that requirement class
is absent and returns whether it added the requirement.

Schema utilities identify import locations, make shallow copies of schema
requirements, and merge missing imports in sorted order.
`merge_schema_def_imports` updates the supplied requirement in place.

`adjust_resource_requirements` updates `CommandLineTool` processes in place.
When no `ResourceRequirement` exists, it adds one with defaults of 2 cores and
2000 MiB RAM. Missing minima are derived from the corresponding maxima, capped
at these defaults for numeric values; expressions are preserved. Missing maxima
are copied from existing minima. Existing pairs are preserved, and workflow
processes are skipped.

::: eoap_cwlwrap.requirements
    options:
      members:
        - DEFAULT_CORES_MAX
        - DEFAULT_RAM_MAX
        - get_feature_requirement
        - contains_feature_requirement
        - add_feature_requirement
        - get_schema_def_import
        - copy_schema_def_requirement
        - merge_schema_def_imports
        - adjust_resource_requirements
      members_order: source
      show_root_full_path: false
      show_root_heading: false
      show_root_toc_entry: false
      show_source: false
