# Runtime Dependencies

The plugin's direct runtime dependencies are declared in `pyproject.toml`:

| Package | Role |
| --- | --- |
| `transpiler-mate-api` | Plugin interfaces, context, errors, and supporting CWL dependencies. |
| `loguru` | Build and validation logging. |

Install `transpiler-mate-runtime` alongside the plugin to provide the
`transpiler-mate` CLI, plugin discovery, and CWL location resolution.

The documentation environment also uses `mkdocs-material`, `mkdocs-jupyter`, and
`mkdocstrings`. The test environment uses `cwltool` to validate generated CWL
documents.
