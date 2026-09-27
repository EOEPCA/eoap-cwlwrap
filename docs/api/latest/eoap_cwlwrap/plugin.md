# `eoap_cwlwrap.plugin`

Transpiler Mate registers `cwlwrap` through the `transpiler_mate.plugins` entry
point. The plugin resolves optional staging locations using the supplied context,
wraps its selected process, adjusts command-line tool resource requirements, and
writes the wrapper and resolved processes to a packed CWL document.

`CwlWrapOptions` accepts `directory_stage_in`, `file_stage_in`,
`directory_stage_out`, and `file_stage_out` as optional CWL URLs or file paths.
Each defaults to `None`. Use a `#<process-id>` fragment to select a staging
process from a multi-process graph. The `output` path defaults to `wrapped.cwl`;
the plugin creates parent directories as needed and overwrites the output file.
Unknown option fields are rejected.

::: eoap_cwlwrap.plugin
    options:
      members:
        - CwlWrapOptions
        - cwlwrap
      members_order: source
      show_root_full_path: false
      show_root_heading: false
      show_root_toc_entry: false
      show_source: false
