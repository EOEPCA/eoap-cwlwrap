# Install EOAP CWL Wrap

Install the released package from PyPI:

```bash
pip install eoap-cwlwrap
```

To test the current `main` branch before a release:

```bash
pip install --no-cache-dir git+https://github.com/EOEPCA/eoap-cwlwrap@main
```

To run from the published container image:

```bash
docker run -it --rm ghcr.io/eoepca/eoap-cwlwrap/eoap-cwlwrap:latest eoap-cwlwrap --help
```

The package declares Python `>=3.8`; the project test matrix covers Python 3.9 through 3.13.
