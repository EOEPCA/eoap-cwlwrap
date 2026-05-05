# Runtime Dependencies

The runtime dependencies are declared in `pyproject.toml`:

| Package | Role |
| --- | --- |
| `click` | Command-line interface. |
| `cwl-loader` | CWL loading, dumping, process lookup, and graph ordering. |
| `cwl-utils` | CWL parser model classes used to build workflows. |
| `loguru` | Build and validation logging. |

The documentation environment also uses `mkdocs-material`, `mkdocs-jupyter`, and `mkdocstrings`.

The test environment uses `cwltool` to validate generated CWL documents.
