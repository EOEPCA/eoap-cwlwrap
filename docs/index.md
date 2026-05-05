# EOAP CWL Wrap

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
pip install eoap-cwlwrap
```

Build a wrapped workflow:

```bash
eoap-cwlwrap \
  --directory-stage-in ./stage-in.cwl \
  --workflow ./workflow.cwl#water-bodies-detection \
  --directory-stage-out ./stage-out.cwl \
  --output ./wrapped.cwl
```

For the full command surface, see the [CLI reference](reference/cli.md).
