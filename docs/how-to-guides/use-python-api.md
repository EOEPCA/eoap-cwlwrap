# Build a Wrapped Workflow With Python

Use `wrap_locations` when the source CWL documents are available as local paths or URLs:

```python
from pathlib import Path

from cwl_loader import dump_cwl
from eoap_cwlwrap import wrap_locations

base_url = "https://raw.githubusercontent.com/eoap/application-package-patterns/refs/heads/main"
workflow_id = "pattern-1"

wrapped = wrap_locations(
    directory_stage_in=f"{base_url}/templates/stage-in.cwl",
    workflows=f"{base_url}/cwl-workflow/{workflow_id}.cwl#{workflow_id}",
    directory_stage_out=f"{base_url}/templates/stage-out.cwl",
)

with Path("wrapped.cwl").open("w") as stream:
    dump_cwl(wrapped, stream)
```

Use `wrap_raw` when you already have CWL documents loaded as mappings, or `wrap` when you already have parsed `cwl_utils.parser.Process` objects.
