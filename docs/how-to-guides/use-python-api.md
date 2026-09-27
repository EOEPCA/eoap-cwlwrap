# Build a Wrapped Workflow With Python

Use the plugin with a Transpiler Mate context when the source CWL documents are
available as local paths or URLs. Install `transpiler-mate-runtime` alongside
`eoap-cwlwrap` for the default resolver.

```python
from pathlib import Path

from transpiler_mate.runtime.context_resolver import DefaultTranspilerContextResolver

from eoap_cwlwrap.plugin import CwlWrapOptions, cwlwrap

base_url = "https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/develop"
workflow_id = "pattern-1"
context = DefaultTranspilerContextResolver().resolve(
    f"{base_url}/cwl-workflow/{workflow_id}.cwl#{workflow_id}"
)
options = CwlWrapOptions(
    directory_stage_in=f"{base_url}/templates/stage-in.cwl",
    directory_stage_out=f"{base_url}/templates/stage-out.cwl",
    output=Path("wrapped.cwl"),
)
cwlwrap.execute(context, options)
```

The plugin writes the packed CWL document to `options.output`.

For already parsed `cwl_utils.parser.Process` objects, use
[`eoap_cwlwrap.wrap`](../api/latest/eoap_cwlwrap/index.md) to construct an
orchestrating workflow in memory. Packing and file serialization are handled by
the plugin. The former `wrap_locations` and `wrap_raw` helpers are no longer
available.
