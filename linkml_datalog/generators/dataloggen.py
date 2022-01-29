import os
from dataclasses import dataclass
from typing import Union, TextIO, Optional, Set, List, Any, Callable, Dict, Tuple
import logging

import click
from jinja2 import Template

from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition, SlotDefinition, Element, \
    ClassDefinitionName, \
    SlotDefinitionName, \
    ElementName, TypeDefinitionName, TypeDefinition, Definition, DefinitionName, PermissibleValue
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView


macros = """
{% macro slot(s, c=None) -%}
// MACRO SLOT: {{s.name}} {{c}}

{%- endmacro %}
"""

template = macros + """


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

// closure
.decl uri_subsumed_by(s:symbol, o:symbol)
uri_subsumed_by(s,o) :- uri_subsumed_by(s,z), uri_subsumed_by(z,o).

.decl validation_result(type: symbol, subject: symbol, instantiates: symbol, path: symbol, value: symbol, info:symbol)
.output validation_result


{% if 'datalog' in schemaview.schema.annotations %}
// ------------------
// -- SCHEMA RULES --
// ------------------
{{ schemaview.schema.annotations['datalog'].value }}
{% endif %}

// -------------
// -- Slots --
// -------------
{% for s in schemaview.all_slots().values() %}
{% set dltype = gen.datalog_type(s) %}
// Slot: {{s.name}} TYPE: {{ dltype }}
{{slot(s)}}
{% set spred = gen.pred(s) -%}
.decl {{ spred }}_asserted(i: identifier, v: {{ dltype }})
.decl {{ spred }}(i: identifier, v: {{ dltype }})
.output {{ spred }}
{{ spred }}(i, v) :- 
    {{ spred }}_asserted(i, v).
{{ spred }}_asserted(i, v) :- 
    {% if dltype == 'identifier' %}
    triple(i, "{{ gen.uri(s) }}", v).
    {% else %}
    triple(i, "{{ gen.uri(s) }}", x),
    {% if dltype == 'number' %}
    literal_number(x, v).
    {% else %}
     literal_symbol(x, v).
    {% endif %}
    {% endif %}
    
uri_subsumed_by("{{ gen.uri(s) }}", "{{ gen.uri(s) }}").
{% for p in gen.parents(s) %}
{{ gen.pred(p) }}(i, v) :- {{ spred }}(i, v).
uri_subsumed_by("{{ gen.uri(s) }}", "{{ gen.uri(p) }}").
{% endfor %}

{% if s.inverse %}
// inverse
{{ spred }}(i, v) :- {{ gen.pred(s.inverse) }}(v, i). 
{% endif %}

{% if s.symmetric %}
// symmetric
{{ spred }}(i, v) :- {{ spred }}(v, i). 
{% endif %}

{% if gen.is_transitive(s) %}
// transitive
{{ spred }}(i, v) :- 
    {{ spred }}(i, z),
    {{ spred }}(z, v).
{% endif %}

{% if 'transitive_closure_of' in s.annotations %}
// transitive
{{ spred }}(i, v) :- 
    {{ gen.pred(s.annotations['transitive_closure_of'].value) }}(i, v).
{% endif %}

// DOMAIN AND RANGE

validation_result(
  "sh:ClosedConstraintComponent",
  i,
  "{{s.name}}",
  "{{s.name}}",
  //to_string(v),
  "",
  "Expected domain is {{gen.domains(s)}}") :-
    {{spred}}(i, _v)
    {%- for domain in gen.domains(s) -%}
    , ! {{ gen.pred(domain) }}(i)
    {%- endfor %} .
    
{% if s.range and not s.range in schemaview.all_types() %}
validation_result(
  "sh:Range",
  i,
  "{{s.name}}",
  "{{s.name}}",
  //as(v, value),
  "",
  "Expected range is {{s.range}}") :-
    {{spred}}(i, v),
    ! {{ gen.pred(s.range) }}(v).
{% endif %}
    
{% endfor %}
// end of slots block

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


{% if gen.reification_of(c.name) %}
{% set reif = gen.reification_of(c.name) %}
// DE-REIFICATION RULE:
triple(i, p, v) :-
        {% if reif.subject %}
        {{gen.pred(reif.subject)}}(r, i)
        {% else %}
        triple(i, _container_prop, r),
        {% endif %}
        {{gen.pred(reif.object)}}(r, v),
        {{gen.pred(reif.predicate)}}(r, p).
{% endif %} 

{% if c.defining_slots %}
// Auto-classification from defining slots: {{c.defining_slots}}

{{ cpred }}(i) :-
    {{ gen.pred(c.is_a) }}(i)
    {% for ds in c.defining_slots %}
    {% set islot = schemaview.induced_slot(ds, c.name) %}
    {% set spred = gen.pred(islot) %}
    {% if islot.subproperty_of %}
    , {{ spred }}(i, v_{{ spred }}), uri_subsumed_by(v_{{ spred }}, "{{ gen.uri(islot.subproperty_of) }}")
    {% else %}
    , {{ spred }}(i, v_{{ spred }}), {{ gen.pred(islot.range) }}(v_{{ spred }})
    {% endif %}
    {% endfor %}
    .
{% endif %}

{% for s in schemaview.class_induced_slots(c.name) %}
{% set spred = gen.class_slot_pred(c, s) -%}
{% set dltype = gen.datalog_type(s) %}
// CLASS_SLOT {{s.name}} TYPE: {{ dltype }}
.decl {{ spred }}_asserted(i: identifier, v: {{ dltype }})
.decl {{ spred }}(i: identifier, v: {{ dltype }})
.output {{ spred }}
.output {{ spred }}_asserted
{{ spred }}(i, v) :- 
    {{ spred }}_asserted(i, v).
{{ spred }}_asserted(i, v) :- 
    {{ cpred }}(i),
    {{ gen.pred(s) }}(i, v).
// TODO: inferring default values

{% if s.inverse and False %}
{% set inv = s.inverse %}
{% set inv_range = gen.get_slot_range(inv) %}
// Inverse of: {{inv}} range: {{inv_range}}
{% set spred_inv = gen.class_slot_pred(inv_range, inv) %}
{{ spred }}(i, v) :- {{ spred_inv }}(v, i). 
{% endif %}

{% if 'classified_from' in s.annotations %}
{% set classified_from = s.annotations['classified_from'].value %}
{% set enum = schemaview.get_enum(s.range) %}
// CLASSIFYING CATEGORY FROM OTHER SLOT {{enum.name}} . {{classified_from}}
{% for pv in enum.permissible_values.values() %}
// PV = {{pv.text}}
{% if 'expr' in pv.annotations %}
{% set expr = pv.annotations['expr'] %}
{{ spred }}(i, "{{ gen.uri(pv) }}" ) :-
     {{ classified_from }}(i, v),
     {{expr.value}} .
{% endif %}
{% endfor %}
{% endif %}

{% if not s.multivalued %}
validation_result(
  "sh:MaxCountConstraintComponent",
  i,
  "{{ cpred }}",
  "{{ s.name }}",
  "",
  //v1,
  "got two distinct values for subject and predicate") :-
    {{ spred }}(i, v1),
    {{ spred }}(i, v2),
    v1 != v2. 
{% endif %}

{% if s.required %}
validation_result(
  "sh:MinCountConstraintComponent",
  i,
  "{{ cpred }}",
  "{{ s.name }}",
  "",
  "") :-
    {{ cpred }}(i),
    ! {{spred}}(i, _).
{% endif %}

{% if s.maximum_value %}
validation_result(
  "sh:MaxInclusiveConstraintComponent",
  i,
  "{{ cpred }}",
  "{{s.name}}",
  to_string(v),
  "Maximum is {{s.maximum_value}}") :-
    {{ cpred }}(i),
    {{spred}}(i, v),
    v > {{ s.maximum_value }}.
{% endif %}

{% if s.range and not s.range in schemaview.all_types() %}
validation_result(
  "sh:ClassConstraintComponent",
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
{% set type_type = gen.type_to_datalog_type(t) %}
// Type: {{t.name}} . {{ type_type }}
//{% set tpred = gen.pred(t) -%}
//.decl {{ tpred }}(i: {{type_type}})
//{% if type_type == 'number' %}
//{% endif %}
//{{ tpred }}(i) :- literal_symbol(i, _).
//{{ tpred }}(i) :- literal_number(i, _).
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

@dataclass
class Reification:
    subject: SlotDefinitionName = None
    predicate: SlotDefinitionName = None
    object: SlotDefinitionName = None

class DatalogGenerator(Generator):
    """
    Generates Souffle datalog from a LinkML schema where the domain of discourse is RDF triples

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

    def uri(self, el: Union[Element, ElementName, PermissibleValue]) -> str:
        sv = self.schemaview
        sv: SchemaView
        if isinstance(el, PermissibleValue):
            if el.meaning:
                return self.meaning_uri(el.meaning)
        if not isinstance(el, Element):
            el = sv.get_element(el)
        if el is None:
            logging.error(f'NONE')
            return 'NONE'
        return sv.get_uri(el, expand=True)

    def meaning_uri(self, curie: str):
        return self.schemaview.expand_curie(curie)

    def domains(self, slot: SlotDefinition) -> List[ClassDefinitionName]:
        sv = self.schemaview
        domains = []
        for cn in sv.all_classes().keys():
            if slot.name in sv.class_slots(cn, direct=True):
                domains.append(cn)
        if slot.domain:
            domains.append(slot.domain)
        return domains

    def get_slot_range(self, sn: SlotDefinitionName):
        """
        TEMPORARY
        """
        sv = self.schemaview
        slot = sv.get_slot(sn)
        if slot.range:
            return slot.range
        elif slot.is_a:
            return self.get_slot_range(slot.is_a)
        else:
            raise ValueError(f'No range for slot {sn}')

    def datalog_type(self, s: Union[SlotDefinition, SlotDefinitionName]) -> str:
        sv = self.schemaview
        if not isinstance(s, SlotDefinition):
            s = sv.get_slot(s)
        if s.range in sv.all_types():
            return self.type_to_datalog_type(s.range)
        return 'identifier'

    def parents(self, e: Definition) -> List[DefinitionName]:
        sv = self.schemaview
        if isinstance(e, SlotDefinition):
            return sv.slot_parents(e.name)
        elif isinstance(e, ClassDefinition):
            return sv.class_parents(e.name)
        else:
            raise ValueError(f'Must be slot or class: {e}')

    def slot_is_numeric(self, s: Union[SlotDefinition, SlotDefinitionName]) -> bool:
        return self.datalog_type(s) == 'number'

    def is_transitive(self, s: SlotDefinition) -> bool:
        return self.has_annotation(s, 'transitive') or self.has_annotation(s, 'transitive_closure_of')

    def is_reflexive(self, s: SlotDefinition) -> bool:
        return self.has_annotation(s, 'transitive')

    def is_symmetric(self, s: SlotDefinition) -> bool:
        return s.symmetric

    def has_annotation(self, s: SlotDefinition, a: str) -> bool:
        return a in s.annotations

    def type_to_datalog_type(self, t: Union[TypeDefinition, TypeDefinitionName]) -> str:
        sv = self.schemaview
        if not isinstance(t, TypeDefinition):
            t = sv.get_type(t)
        if t.base == 'int' or t.base == 'float' or t.base == 'Decimal':
            return 'number'
        else:
            return 'symbol'

    def type_is_numeric(self, t: Union[TypeDefinition, TypeDefinitionName]) -> bool:
        return self.type_to_datalog_type(t) == 'number'

    def reification_of(self, cn: ClassDefinitionName) -> Optional[Reification]:
        """
        TODO: move to schemaview
        """
        sv = self.schemaview
        if sv.is_relationship(cn):
            islots = sv.class_induced_slots(cn)
            su = None
            pr = None
            ob = None
            for islot in islots:
                for anc in sv.class_ancestors(cn):
                    slot_uri = sv.induced_slot(islot.name, anc).slot_uri
                    if slot_uri == 'rdf:subject':
                        su = islot
                    if slot_uri == 'rdf:predicate':
                        pr = islot
                    if slot_uri == 'rdf:object':
                        ob = islot
            if pr is None:
                logging.error(f'No predicate for {cn}')
                return None
            if ob is None:
                logging.error(f'No object for {cn}')
                return None
            reif = Reification(subject=su,
                               predicate=pr,
                               object=ob)
            return reif
        else:
            return None



@shared_arguments(DatalogGenerator)
@click.command()
def cli(yamlfile, dir, **kwargs):
    """ Generate Souffle datalog from a LinkML schema """
    print(DatalogGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == '__main__':
    cli()
