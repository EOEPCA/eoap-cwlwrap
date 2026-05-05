# EOAP CWL Wrap

[![PyPI - Version](https://img.shields.io/pypi/v/eoap-cwlwrap.svg)](https://pypi.org/project/eoap-cwlwrap)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/eoap-cwlwrap.svg)](https://pypi.org/project/eoap-cwlwrap)

`eoap-cwlwrap` is a command-line utility that composes a CWL `Workflow` from a series of `Workflow`/`CommandLineTool` steps, defined according to [Application package patterns based on data stage-in and stage-out behaviors commonly used in EO workflows](https://eoap.github.io/application-package-patterns), and **packs** it into a single self-contained CWL document.

It ensures:
- **Type-safe chaining** of step outputs to the next step's inputs.
- **Reusable, modular design** by keeping each step in its own file.
- **Packed output** ready for execution or distribution.

## Contribute

Submit a [Github issue](https://github.com/EOEPCA/eoap-cwlwrap/issues) if you have comments or suggestions.

## Documentation

See the documentation at https://eoepca.github.io/eoap-cwlwrap/

## License

[![Apache License, Version 2.0](https://img.shields.io/badge/license-Apache%20License%202.0-blue)](https://www.apache.org/licenses/LICENSE-2.0)

