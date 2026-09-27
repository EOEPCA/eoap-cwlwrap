# `eoap_cwlwrap`

The top-level `wrap` function accepts loaded CWL processes, validates any supplied
staging processes, and returns an orchestrating workflow. Staging arguments default to `None`, but matching components are required for
any `Directory`- or `File`-compatible inputs and outputs.

Use the [`cwlwrap` plugin](plugin.md) to resolve CWL locations and write a packed
CWL document. `wrap` itself does not write a file.

::: eoap_cwlwrap
    options:
      members:
        - wrap
      members_order: source
      show_root_full_path: false
      show_root_heading: false
      show_root_toc_entry: false
      show_source: false
