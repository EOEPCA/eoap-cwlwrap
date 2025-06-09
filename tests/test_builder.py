'''
CWL Chain Builder (c) 2025

CWL Chain Builder is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
'''

import pytest
from cwl_chain_builder.builder import build_workflow

def test_fails_on_type_mismatch(tmp_path):
    step1 = tmp_path / "step1.cwl"
    step2 = tmp_path / "step2.cwl"

    step1.write_text("""cwlVersion: v1.2
class: CommandLineTool
inputs:
  input_text:
    type: string
outputs:
  output_number:
    type: int
baseCommand: [echo]
stdout: step1.txt
outputBinding:
  glob: step1.txt
""")

    step2.write_text("""cwlVersion: v1.2
class: CommandLineTool
inputs:
  input_number:
    type: string
outputs:
  output_text:
    type: string
baseCommand: [echo]
stdout: step2.txt
outputBinding:
  glob: step2.txt
""")

    with pytest.raises(ValueError, match="Type mismatch"):
        build_workflow([str(step1), str(step2)])
