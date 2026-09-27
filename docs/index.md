# EOAP CWL Wrap

!!! warning "CLI migration since version 0.32.0"

    Since version **0.32.0**, EOAP CWL Wrap is a **Transpiler Mate plugin**.
    Install `transpiler-mate-runtime` alongside `eoap-cwlwrap` and invoke
    `transpiler-mate cwlwrap` instead of `eoap-cwlwrap`. Pass the application
    workflow as the positional `SOURCE` argument instead of `--workflow`.
    The legacy `--workflow-id` and `--stage-out` options are no longer supported;
    use a `#<process-id>` fragment and `--directory-stage-out`, respectively.

`eoap-cwlwrap` composes an EO Application Package CWL `Workflow` with stage-in and stage-out processes, then packs the result into a single self-contained CWL document.

Use these docs by intent:

- [Tutorials](tutorials/index.md): learn the wrapping flow by working through a complete example.
- [How-to guides](how-to-guides/index.md): complete common tasks such as installation, CLI usage, and Python API usage.
- [Reference](reference/index.md): look up CLI options, CWL component contracts, dependencies, and API details.
- [Explanation](explanation/index.md): understand why the wrapper exists and how it builds the orchestrator workflow.

The documentation is organized with the [Diataxis](https://diataxis.fr/) approach: tutorials, how-to guides, reference, and explanation each answer a different reader need.

## What It Does

`eoap-cwlwrap` inspects a CWL workflow, adds stage-in steps for `Directory` and `File` inputs, adds stage-out steps for `Directory` and `File` outputs, converts the outer workflow interface to URI-compatible values where needed, and emits a packed CWL graph ready to validate, run, or distribute.

## Quick Start

Install the package:

```bash
pip install transpiler-mate-runtime eoap-cwlwrap
```

Build a wrapped workflow:

```bash
transpiler-mate cwlwrap \
  --directory-stage-in ./stage-in.cwl \
  ./workflow.cwl#water-bodies-detection \
  --directory-stage-out ./stage-out.cwl \
  --output ./wrapped.cwl
```

For the full command surface, see the [CLI reference](reference/cli.md).
