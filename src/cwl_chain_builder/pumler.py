"""
CWL Chain Builder (c) 2025

CWL Chain Builder is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from cwl_utils.parser.cwl_v1_2 import Workflow
from jinja2 import Template
from pathlib import Path

def to_puml(workflows: list[Workflow], output: str):
    print(f"Saving the new PlantUML Workflow diagram to {output}...")

    template = Template("""{% macro to_puml_name(identifier) %}{{ identifier | replace('-', '_') }}{% endmacro %}
/'
CWL Chain Builder (c) 2025

CWL Chain Builder is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
'/
@startuml

{% for workflow in workflows %}
component "{{ workflow.id }}" as {{ to_puml_name(workflow.id) }} {
    {% for input in workflow.inputs %}portin "{{ input.id }}" as {{ to_puml_name(workflow.id) }}_{{ to_puml_name(input.id) }}
    {% endfor %}
    {% for output in workflow.outputs %}portout "{{ output.id }}" as {{ to_puml_name(workflow.id) }}_{{ to_puml_name(output.id) }}
    {% endfor %}

    {% if workflow.steps is defined %}
    {% for step in workflow.steps %}component "{{ step.id }}" as {{ to_puml_name(workflow.id) }}_{{ to_puml_name(step.id) }} {
        {% for input in step.in_ %}portin "{{ input.id }}" as {{ to_puml_name(workflow.id) }}_{{ to_puml_name(step.id) }}_{{ to_puml_name(input.id) }}
        {% endfor %}
        {% for output in step.out %}portout "{{ output }}" as {{ to_puml_name(workflow.id) }}_{{ to_puml_name(step.id) }}_{{ to_puml_name(output) }}
        {% endfor %}
    }
    {% endfor %}
    {% endif %}
}
{% endfor %}

{% for workflow in workflows %}
    {% if workflow.steps is defined %}
        {% for step in workflow.steps %}
            {% for input in step.in_ %}
{{ to_puml_name(workflow.id) }}_{{ input.source | replace('/', '_') | replace('-', '_') }} --> {{ to_puml_name(workflow.id) }}_{{ to_puml_name(step.id) }}_{{ to_puml_name(input.id) }}
            {% endfor %}

{{ to_puml_name(workflow.id) }}_{{ to_puml_name(step.id) }} -> {{ step.run[1:] | replace('-', '_') }}
        {% endfor %}
    {% endif %}

    {% for output in workflow.outputs %}
        {% for outputSource in output.outputSource %}
{{ to_puml_name(workflow.id) }}_{{ outputSource | replace('/', '_') | replace('-', '_') }} --> {{ to_puml_name(workflow.id) }}_{{ to_puml_name(output.id) }}
        {% endfor %}
    {% endfor %}
{% endfor %}
@enduml

""")

    output_path = Path(output)

    with output_path.open("w") as f:
        f.write(template.render(workflows=workflows))

    print(f"PlantUML Workflow diagram successfully saved to {output}!")
