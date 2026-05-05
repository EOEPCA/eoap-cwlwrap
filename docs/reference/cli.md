# CLI Reference

`eoap-cwlwrap` builds and writes a packed orchestrator workflow.

```bash
eoap-cwlwrap [OPTIONS]
```

## Options

| Option | Required | Description |
| --- | --- | --- |
| `--workflow` | Yes | CWL workflow file or URL. Use `<location>#<process-id>` to select a process from a `$graph`. |
| `--directory-stage-out` | Yes | CWL stage-out file or URL for `Directory`-compatible outputs. |
| `--output` | Yes | Output file path for the packed CWL document. Parent directories are created automatically. |
| `--directory-stage-in` | No | CWL stage-in file or URL for `Directory`-compatible inputs. |
| `--file-stage-in` | No | CWL stage-in file or URL for `File`-compatible inputs. |
| `--file-stage-out` | No | CWL stage-out file or URL for `File`-compatible outputs. |
| `--workflow-id` | No | Deprecated. Use `--workflow <location>#<process-id>` instead. |

## Process Selection

If `--workflow` points to a single CWL `Process`, the process id can be omitted:

```bash
eoap-cwlwrap \
  --workflow ./workflow.cwl \
  --directory-stage-out ./stage-out.cwl \
  --output ./wrapped.cwl
```

If the document contains a `$graph`, include the id:

```bash
eoap-cwlwrap \
  --workflow ./workflow.cwl#water-bodies-detection \
  --directory-stage-out ./stage-out.cwl \
  --output ./wrapped.cwl
```
