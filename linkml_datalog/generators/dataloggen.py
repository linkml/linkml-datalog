import os
import re
from typing import Union, TextIO, Optional, Set, List, Any, Callable, Dict, Tuple
import logging

import click
from jinja2 import Template

from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition, SlotDefinition, Element, \
    ClassDefinitionName, \
    SlotDefinitionName, \
    TypeDefinition, TypeDefinitionName, ElementName
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.typereferences import References
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import URIRef
from rdflib.namespace import RDF, RDFS, SKOS

prefixes: Dict[str, URIRef] = {
    "RDF_TYPE": RDF['type']
}

RESERVED = ['range']
CONSTRAINT_FAIL_ON_EVAL = 'constraint_fail_on_eval'

template = """
/**
 Schema: {{schema.name}}
*/

// Declarations
#define RDF_TYPE "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

.type identifier = symbol
.type value = symbol

// Mapping from RDF
.decl triple(s:symbol, p:symbol, o:symbol)
.input triple
.decl literal_number(s:symbol, o:number)
.input literal_number
.decl literal_symbol(s:symbol, o:symbol)
.input literal_symbol

.decl validation_result(type: symbol, subject: symbol, instantiates: symbol, path: symbol, value: symbol, info:symbol)
.output validation_result

// -------------
// -- CLASSES --
// -------------
{% for c in schemaview.all_classes().values() %}
// Class: {{c.name}}
{% set cpred = gen.pred(c) -%}
.decl {{ cpred }}(i: symbol)
.decl {{ cpred }}_asserted(i: identifier)
.output {{ cpred }}
{{ cpred }}_asserted(i) :- triple(i, RDF_TYPE, "{{ gen.uri(c) }}").
{{ cpred }}(i) :- {{ cpred }}_asserted(i).
{% if c.is_a %}
{{ gen.pred(c.is_a) }}(i) :- {{ cpred }}(i).
{% endif %}
{% for p in c.mixins %}
{{ gen.pred(p) }}(i) :- {{ cpred }}(i).
{% endfor %}

{% for s in schemaview.class_induced_slots(c.name) %}
{% set spred = gen.class_slot_pred(c, s) -%}
.decl {{ spred }}_asserted(i: identifier, v: value)
.decl {{ spred }}(i: identifier, v: value)
.output {{ spred }}
.output {{ spred }}_asserted
{{ spred }}(i, v) :- 
    {{ spred }}_asserted(i, v).
{{ spred }}_asserted(i, v) :- 
    {{ cpred }}(i),
    triple(i, "{{ gen.uri(s) }}", v).
// TODO: inferring default values

{% if not s.multivalued %}
validation_result(
  "sh:MaxCountConstraintComponent",
  i,
  "{{ cpred }}",
  "TODO path",
  v1,
  "") :-
    {{ spred }}(i, v1),
    {{ spred }}(i, v2),
    v1 != v2. 
{% endif %}

{% if s.required %}
validation_result(
  "sh:MaxCountConstraintComponent",
  i,
  "{{ cpred }}",
  "TODO path",
  "",
  "") :-
    {{ cpred }}(i),
    ! {{spred}}(i, _).
{% endif %}

{% if s.maximum_value %}
validation_result(
  "sh:MaxValueTODO",
  i,
  "{{ cpred }}",
  "{{s.name}}",
  v,
  "Maximum is {{s.maximum_value}}") :-
    {{ cpred }}(i),
    {{spred}}(i, v),
    literal_number(v,num),
    num > {{ s.maximum_value }}.
{% endif %}

{% if s.range %}
validation_result(
  "sh:Range",
  i,
  "{{ cpred }}",
  "{{s.name}}",
  v,
  "Expected range is {{s.range}}") :-
    {{ cpred }}(i),
    {{spred}}(i, v),
    ! {{ gen.pred(s.range) }}(v).
{% endif %}

{% endfor %}
// end of class slots block

{% endfor %}
// end of classes block

// -------------
// -- Types --
// -------------
{% for t in schemaview.all_types().values() %}
// Type: {{t.name}}
{% set tpred = gen.pred(t) -%}
.decl {{ tpred }}(i: symbol)
{{ tpred }}(i) :- literal_symbol(i, _).
{{ tpred }}(i) :- literal_number(i, _).
// TODO!
{% endfor %}
// end of types block

// -------------
// -- Enums --
// -------------
{% for e in schemaview.all_enums().values() %}
// Enum: {{e.name}}
{% set epred = gen.pred(e) -%}
.decl {{ epred }}(i: symbol)
{{ epred }}(i) :- literal_symbol(i, _).
// TODO!
{% for pv in e.permissible_values.values() %}
{% if pv.meaning %}
{{ epred }}("{{ gen.meaning_uri(pv.meaning) }}").
{% else %}
{% endif %}
{% endfor %}
{% endfor %}
// end of enums block

"""

class DatalogTerm:
    predicate: str

class Declaration(DatalogTerm):
    None

class DatalogGenerator(Generator):
    """
    Generates Souffle datalog from a LinkML schema where the domain of discourse is RDF triples

    Example output:

    ```
    // Slot: current_address
    // The address at which a person currently lives
    .decl current_address_asserted(s:symbol, o:symbol)
    .decl current_address(s:symbol, o:symbol)
    current_address_asserted(s,o) :- rdf(s, "<https://w3id.org/linkml/examples/personinfo/current_address>", o).
    current_address(s,o) :- current_address_asserted(s,o).
   ```

    (OLDER EXPERIMENT?)
    """
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ['dl']
    visit_all_class_slots = True
    visited = set()
    type_field_uris: List[str] = []
    schemaview: SchemaView = []

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], format: str = valid_formats[0], **kwargs) -> None:
        self.format = format
        self.schemaview = SchemaView(schema)

    def serialize(self, **kwargs) -> str:
        sv = self.schemaview
        template_obj = Template(template)
        code = template_obj.render(schemaview=self.schemaview,
                                   schema=self.schemaview.schema,
                                   gen=self)
        return code


    def pred(self, el: Union[Element, ElementName]) -> str:
        sv = self.schemaview
        sv: SchemaView
        if el == '':
            return 'NONE'
        if not isinstance(el, Element):
            if sv.get_element(el) is None:
                logging.error(f'No such element: "{el}" // {type(el)}')
                return 'UNDEFINED'
            el = sv.get_element(el)
        if isinstance(el, SlotDefinition):
            pred = underscore(el.name)
        else:
            pred = camelcase(el.name)
        return pred

    def class_slot_pred(self, c: Union[ClassDefinition, ClassDefinitionName], s: Union[SlotDefinition, SlotDefinitionName]) -> str:
        return f'{self.pred(c)}_{self.pred(s)}'

    def uri(self, el: Union[Element, ElementName]) -> str:
        sv = self.schemaview
        sv: SchemaView
        if not isinstance(el, Element):
            el = sv.get_element(el)
        if el is None:
            logging.error(f'NONE')
            return 'NONE'
        return sv.get_uri(el, expand=True)

    def meaning_uri(self, curie: str):
        return self.schemaview.expand_curie(curie)


@shared_arguments(DatalogGenerator)
@click.command()
def cli(yamlfile, dir, **kwargs):
    """ Generate Souffle datalog from a LinkML schema """
    print(DatalogGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == '__main__':
    cli()
