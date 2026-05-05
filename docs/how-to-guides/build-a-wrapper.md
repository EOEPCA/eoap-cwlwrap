# Build a Wrapped Workflow With the CLI

Use the `eoap-cwlwrap` command when your stage-in, application workflow, and stage-out CWL documents are available as files or URLs.

```bash
eoap-cwlwrap \
  --directory-stage-in ./stage-in.cwl \
  --file-stage-in ./stage-in-file.cwl \
  --workflow ./workflow.cwl#water-bodies-detection \
  --directory-stage-out ./stage-out.cwl \
  --file-stage-out ./stage-out-file.cwl \
  --output ./wrapped.cwl
```

Append `#<process-id>` to `--workflow` when the CWL document contains a `$graph` or when the workflow id must be selected explicitly:

```bash
eoap-cwlwrap \
  --directory-stage-in https://example.test/stage-in.cwl \
  --workflow https://example.test/workflows.cwl#water-bodies-detection \
  --directory-stage-out https://example.test/stage-out.cwl \
  --output ./wrapped.cwl
```

You only need `--file-stage-in` when the application workflow has `File`-compatible inputs. You only need `--file-stage-out` when it has `File`-compatible outputs.

Validate the generated CWL with `cwltool`:

```bash
cwltool --enable-ext --validate ./wrapped.cwl
```
