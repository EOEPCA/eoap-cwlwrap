# CLI Reference

`eoap-cwlwrap` builds and writes a packed orchestrator workflow.

```bash
eoap-cwlwrap [OPTIONS]
```

## Options

| Option | Required | Description |
| --- | --- | --- |
| `--workflow` | Yes | CWL workflow file or URL. Use `<location>#<process-id>` to select a process from a `$graph`. |
| `--output` | Yes | Output file path for the packed CWL document. Parent directories are created automatically. |
| `--directory-stage-in` | When needed | CWL stage-in file or URL for `Directory`-compatible inputs. Required when the application workflow has `Directory` inputs. |
| `--file-stage-in` | When needed | CWL stage-in file or URL for `File`-compatible inputs. Required when the application workflow has `File` inputs. |
| `--directory-stage-out` | When needed | CWL stage-out file or URL for `Directory`-compatible outputs. Required when the application workflow has `Directory` outputs. |
| `--stage-out` | When needed | Deprecated alias for `--directory-stage-out`. |
| `--file-stage-out` | When needed | CWL stage-out file or URL for `File`-compatible outputs. Required when the application workflow has `File` outputs. |
| `--workflow-id` | No | Deprecated. Use `--workflow <location>#<process-id>` instead. |
| `--oci-hostname` | For `oci://` | OCI registry hostname. Can also be set with `OCI_HOSTNAME`. |
| `--oci-username` | For `oci://` | OCI registry username. Can also be set with `OCI_USERNAME`. |
| `--oci-password` | For `oci://` | OCI registry password. Can also be set with `OCI_PASSWORD`. |

Stage-in and stage-out options are conditional. The command inspects the selected workflow and requires only the component types needed to adapt its `Directory` and `File` inputs and outputs.

## Process Selection

If `--workflow` points to a single CWL `Process`, the process id can be omitted:

```bash
eoap-cwlwrap \
  --workflow ./workflow.cwl \
  --directory-stage-out ./stage-out.cwl \
  --output ./wrapped.cwl
```

If the workflow document contains a `$graph`, include the id:

```bash
eoap-cwlwrap \
  --workflow ./workflow.cwl#water-bodies-detection \
  --directory-stage-out ./stage-out.cwl \
  --output ./wrapped.cwl
```

Process selection works for every CWL location option, not only `--workflow`. Append `#<process-id>` to `--directory-stage-in`, `--file-stage-in`, `--directory-stage-out`, `--stage-out`, or `--file-stage-out` when the corresponding document contains a `$graph`:

```bash
eoap-cwlwrap \
  --directory-stage-in ./components.cwl#directory-stage-in \
  --workflow ./workflow.cwl#water-bodies-detection \
  --directory-stage-out ./components.cwl#directory-stage-out \
  --output ./wrapped.cwl
```

## Location Schemes

Locations can be local paths or URLs. The CLI configures loaders for:

| Scheme | Use |
| --- | --- |
| local path | Read a CWL document from the local filesystem. |
| `file://` | Read a CWL document through a file URL. |
| `http://` or `https://` | Read a CWL document from the web. |
| `s3://` | Read a CWL document from S3-compatible storage. |
| `oci://` | Read a CWL document from an OCI registry, using the OCI options or environment variables above when credentials are needed. |
