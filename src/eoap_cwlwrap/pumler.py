"""
EOAP CWLWrap (c) 2025

EOAP CWLWrap is licensed under
Creative Commons Attribution-ShareAlike 4.0 International.

You should have received a copy of the license along with this work.
If not, see <https://creativecommons.org/licenses/by-sa/4.0/>.
"""

from cwl_utils.parser.cwl_v1_2 import Workflow
from jinja2 import Template
from pathlib import Path

_COMPONENTS_TEMPLATE = """{% macro to_puml_name(identifier) %}{{ identifier | replace('-', '_') }}{% endmacro %}
@startuml
skinparam linetype ortho

{% for workflow in workflows %}
node "{{ workflow.class_ }} '{{ workflow.id }}'" {
    component "{{ workflow.id }}" as {{ to_puml_name(workflow.id) }} {
    {% for input in workflow.inputs %}
        portin "{{ input.id }}" as {{ to_puml_name(workflow.id) }}_{{ to_puml_name(input.id) }}
    {% endfor %}
    {% for output in workflow.outputs %}
        portout "{{ output.id }}" as {{ to_puml_name(workflow.id) }}_{{ to_puml_name(output.id) }}
    {% endfor %}
    }

{% for step in workflow.steps %}
    component "{{ step.id }}" as {{ to_puml_name(workflow.id) }}_{{ to_puml_name(step.id) }} {
    {% for input in step.in_ %}
        portin "{{ input.id }}" as {{ to_puml_name(workflow.id) }}_{{ to_puml_name(step.id) }}_{{ to_puml_name(input.id) }}
        {{ to_puml_name(workflow.id) }}_{{ input.source | replace('/', '_') | replace('-', '_') }} -down-> {{ to_puml_name(workflow.id) }}_{{ to_puml_name(step.id) }}_{{ to_puml_name(input.id) }}
    {% endfor %}

    {% for output in step.out %}
        portout "{{ output }}" as {{ to_puml_name(workflow.id) }}_{{ to_puml_name(step.id) }}_{{ to_puml_name(output) }}
    {% endfor %}
    }
{% endfor %}
}
{% endfor %}

{% for workflow in workflows %}
    {% for output in workflow.outputs %}
        {% for outputSource in output.outputSource %}
{{ to_puml_name(workflow.id) }}_{{ outputSource | replace('/', '_') | replace('-', '_') }} -up-> {{ to_puml_name(workflow.id) }}_{{ to_puml_name(output.id) }}
        {% endfor %}
    {% endfor %}

    {% for step in workflow.steps %}
{{ to_puml_name(workflow.id) }}_{{ to_puml_name(step.id) }} -right-> {{ step.run[1:] | replace('-', '_') }}
    {% endfor %}
{% endfor %}
@enduml
"""

_CLASS_TEMPLATE = '''{% macro to_puml_name(identifier) %}{{ identifier | replace('-', '_') }}{% endmacro %}
@startuml

{% for workflow in workflows %}
class "{{ workflow.id }}" as {{ to_puml_name(workflow.id) }} extends {{ workflow.class_ }} {
    __ Inputs __
    {% for input in workflow.inputs %}
    + {{ input.id }}: {{ input.type_ }}
    {% endfor %}

    __ Outputs __
    {% for output in workflow.outputs %}
    + {{ output.id }}: {{ output.type_ }}
    {% endfor %}

    {% if workflow.steps is defined %}
    __ Steps __
        {% for step in workflow.steps %}
    - {{ step.id }}: {{ to_puml_name(step.run[1:]) }}
        {% endfor %}
    {% endif %}
}

    {% for requirement in workflow.requirements %}
        {% if requirement.class_ %}
{{ to_puml_name(workflow.id) }} --> {{ requirement.class_ }}
        {% endif %}
    {% endfor %}
{% endfor %}

{% for workflow in workflows %}
    {% for step in workflow.steps %}
{{ to_puml_name(workflow.id) }} --> {{ to_puml_name(step.run[1:]) }}
    {% endfor %}

    {% for input in workflow.inputs %}
        {% if input.doc is defined %}
note left of {{ to_puml_name(workflow.id) }}::{{ input.id }}
    {{ input.doc }}
end note
        {% endif %}
    {% endfor %}
{% endfor %}
@enduml
'''

def to_puml(workflows: list[Workflow], output: str):
    for diagram_type, sring_template in { 'components': _COMPONENTS_TEMPLATE, 'class': _CLASS_TEMPLATE }.items():
        output_path = Path(f"{output}_{diagram_type}.puml")

        print(f"Saving the new PlantUML Workflow diagram to {output_path}...")

        template = Template(sring_template)

        with output_path.open("w") as f:
            f.write(template.render(workflows=workflows))

        print(f"PlantUML Workflow diagram successfully saved to {output_path}!")
