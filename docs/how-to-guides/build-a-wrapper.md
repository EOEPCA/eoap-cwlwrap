# Build a Wrapped Workflow With the CLI

Use the `transpiler-mate cwlwrap` command when your stage-in, application workflow, and stage-out CWL documents are available as files or URLs.

```bash
transpiler-mate cwlwrap \
  --directory-stage-in ./stage-in.cwl \
  --file-stage-in ./stage-in-file.cwl \
  ./workflow.cwl#water-bodies-detection \
  --directory-stage-out ./stage-out.cwl \
  --file-stage-out ./stage-out-file.cwl \
  --output ./wrapped.cwl
```

Append `#<process-id>` to the positional `SOURCE` argument when the CWL document contains a `$graph` or when the workflow id must be selected explicitly:

```bash
transpiler-mate cwlwrap \
  --directory-stage-in https://example.test/stage-in.cwl \
  https://example.test/workflows.cwl#water-bodies-detection \
  --directory-stage-out https://example.test/stage-out.cwl \
  --output ./wrapped.cwl
```

Supply a matching stage-in for each `Directory`- or `File`-compatible input and
a matching stage-out for each compatible output. Components for types absent
from the application interface can be omitted.
See the [CLI reference](../reference/cli.md) for migration details and all options.

Validate the generated CWL with `cwltool`:

```bash
cwltool --enable-ext --validate ./wrapped.cwl
```
