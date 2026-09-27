# CLI Reference

!!! warning "CLI migration since version 0.32.0"

    Since version **0.32.0**, EOAP CWL Wrap is a **Transpiler Mate plugin**.
    Install `transpiler-mate-runtime` alongside `eoap-cwlwrap` and invoke
    `transpiler-mate cwlwrap` instead of `eoap-cwlwrap`. Pass the application
    workflow as the positional `SOURCE` argument instead of `--workflow`.
    The legacy `--workflow-id` and `--stage-out` options are no longer supported;
    use a `#<process-id>` fragment and `--directory-stage-out`, respectively.

The installed plugin builds and writes a packed orchestrator workflow:

```bash
transpiler-mate cwlwrap [OPTIONS] SOURCE
```

`SOURCE` is the required application CWL file or URL. Append `#<process-id>` to
select a process from a packed graph.

## Plugin Options

| Option | Default | Description |
| --- | --- | --- |
| `--directory-stage-in` | None | CWL stage-in file or URL for `Directory`-compatible inputs. |
| `--file-stage-in` | None | CWL stage-in file or URL for `File`-compatible inputs. |
| `--directory-stage-out` | None | CWL stage-out file or URL for `Directory`-compatible outputs. |
| `--file-stage-out` | None | CWL stage-out file or URL for `File`-compatible outputs. |
| `--output` | `wrapped.cwl` | Output path for the packed CWL document. Parent directories are created automatically; an existing file is overwritten. |
| `--help` | — | Show the command help and exit. |

Staging options are conditionally required: supply the matching stage-in for
each `Directory`- or `File`-compatible input and the matching stage-out for each
compatible output. A missing required component causes wrapping to fail. Other
parameter types are forwarded unchanged. Supplied staging processes must satisfy
the [component contracts](component-contracts.md).

## Runtime Authentication Options

Transpiler Mate supplies these options for resolving CWL locations:

| Option | Environment variable | Description |
| --- | --- | --- |
| `--oci-hostname` | `OCI_HOSTNAME` | OCI registry hostname. |
| `--oci-username` | `OCI_USERNAME` | OCI registry username. |
| `--oci-password` | `OCI_PASSWORD` | OCI registry password. |
| `--oauth2-bearer` | `OAUTH2_BEARER` | OAuth2 bearer token. |

Location loading and authentication are managed by the host runtime. Available
schemes depend on its configured resolver and loaders.

## Process Selection

For a single-process document, use its path directly:

```bash
transpiler-mate cwlwrap ./workflow.cwl \
  --directory-stage-out ./stage-out.cwl \
  --output ./wrapped.cwl
```

Use fragments to select the application process and staging processes from
multi-process documents:

```bash
transpiler-mate cwlwrap './workflow.cwl#water-bodies-detection' \
  --directory-stage-in './components.cwl#directory-stage-in' \
  --directory-stage-out './components.cwl#directory-stage-out' \
  --output ./wrapped.cwl
```

Process fragments work for `SOURCE` and all four staging options. A staging
document containing multiple processes requires an explicit fragment.

Check the options exposed by your installed runtime and plugin with:

```bash
transpiler-mate cwlwrap --help
```
