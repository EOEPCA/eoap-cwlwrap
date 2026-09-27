# Install EOAP CWL Wrap

Since version 0.32.0, EOAP CWL Wrap runs as a Transpiler Mate plugin. Install the
host runtime and plugin in the same Python environment:

```bash
pip install transpiler-mate-runtime eoap-cwlwrap
transpiler-mate cwlwrap --help
```

The runtime discovers the plugin through its `transpiler_mate.plugins` entry
point. Installing the plugin alone does not provide the host CLI.

To test the current `main` branch before a release:

```bash
pip install transpiler-mate-runtime
pip install --no-cache-dir git+https://github.com/EOEPCA/eoap-cwlwrap@main
```

The package requires Python `>=3.10`; the project test matrix covers Python 3.10
through 3.14. See the [CLI reference](../reference/cli.md) for migration details.
