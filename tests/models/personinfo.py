# Auto generated from personinfo.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-12-13T18:36:13
# Schema: personinfo
#
# id: https://w3id.org/linkml/examples/personinfo
# description: Information about people, based on [schema.org](http://schema.org)
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, Date, Float, Integer, String
from linkml_runtime.utils.metamodelcore import Bool, XSDDate

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
CODE = CurieNamespace('CODE', 'https://example.org/CODE/')
GEO = CurieNamespace('GEO', 'https://example.org/GEO/')
GSSO = CurieNamespace('GSSO', 'http://purl.obolibrary.org/obo/GSSO_')
HSAPDV = CurieNamespace('HsapDv', 'http://purl.obolibrary.org/obo/HsapDv_')
P = CurieNamespace('P', 'https://example.org/P/')
ROR = CurieNamespace('ROR', 'https://example.org/ROR/')
FAMREL = CurieNamespace('famrel', 'https://example.org/FamilialRelations#')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PERSONINFO = CurieNamespace('personinfo', 'https://w3id.org/linkml/examples/personinfo/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'http://example.org/UNKNOWN/skos/')
DEFAULT_ = PERSONINFO


# Types

# Class references
class NamedThingId(extended_str):
    pass


class PersonId(NamedThingId):
    pass


class OrganizationId(NamedThingId):
    pass


class PlaceId(extended_str):
    pass


class ConceptId(NamedThingId):
    pass


class DiagnosisConceptId(ConceptId):
    pass


class ProcedureConceptId(ConceptId):
    pass


@dataclass
class NamedThing(YAMLRoot):
    """
    A generic grouping for any identifiable entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.NamedThing
    class_class_curie: ClassVar[str] = "personinfo:NamedThing"
    class_name: ClassVar[str] = "NamedThing"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.NamedThing

    id: Union[str, NamedThingId] = None
    name: str = None
    description: Optional[str] = None
    image: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.image is not None and not isinstance(self.image, str):
            self.image = str(self.image)

        super().__post_init__(**kwargs)


@dataclass
class Person(NamedThing):
    """
    A person (alive, dead, undead, or fictional).
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA.Person
    class_class_curie: ClassVar[str] = "schema:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Person

    id: Union[str, PersonId] = None
    name: str = None
    primary_email: Optional[str] = None
    birth_date: Optional[str] = None
    age_in_years: Optional[int] = None
    gender: Optional[Union[str, "GenderType"]] = None
    current_address: Optional[Union[dict, "Address"]] = None
    has_employment_history: Optional[Union[Union[dict, "EmploymentEvent"], List[Union[dict, "EmploymentEvent"]]]] = empty_list()
    has_familial_relationships: Optional[Union[Union[dict, "FamilialRelationship"], List[Union[dict, "FamilialRelationship"]]]] = empty_list()
    has_medical_history: Optional[Union[Union[dict, "MedicalEvent"], List[Union[dict, "MedicalEvent"]]]] = empty_list()
    sibling_of: Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]] = empty_list()
    parent_of: Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]] = empty_list()
    child_of: Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]] = empty_list()
    father_of: Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]] = empty_list()
    grandparent_of: Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]] = empty_list()
    grandfather_of: Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]] = empty_list()
    grandmother_of: Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]] = empty_list()
    ancestor_of: Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]] = empty_list()
    mother_of: Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]] = empty_list()
    has_siblings: Optional[Union[bool, Bool]] = None
    age_category: Optional[Union[str, "AgeCategory"]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self.primary_email is not None and not isinstance(self.primary_email, str):
            self.primary_email = str(self.primary_email)

        if self.birth_date is not None and not isinstance(self.birth_date, str):
            self.birth_date = str(self.birth_date)

        if self.age_in_years is not None and not isinstance(self.age_in_years, int):
            self.age_in_years = int(self.age_in_years)

        if self.gender is not None and not isinstance(self.gender, GenderType):
            self.gender = GenderType(self.gender)

        if self.current_address is not None and not isinstance(self.current_address, Address):
            self.current_address = Address(**as_dict(self.current_address))

        if not isinstance(self.has_employment_history, list):
            self.has_employment_history = [self.has_employment_history] if self.has_employment_history is not None else []
        self.has_employment_history = [v if isinstance(v, EmploymentEvent) else EmploymentEvent(**as_dict(v)) for v in self.has_employment_history]

        self._normalize_inlined_as_list(slot_name="has_familial_relationships", slot_type=FamilialRelationship, key_name="type", keyed=False)

        if not isinstance(self.has_medical_history, list):
            self.has_medical_history = [self.has_medical_history] if self.has_medical_history is not None else []
        self.has_medical_history = [v if isinstance(v, MedicalEvent) else MedicalEvent(**as_dict(v)) for v in self.has_medical_history]

        if not isinstance(self.sibling_of, list):
            self.sibling_of = [self.sibling_of] if self.sibling_of is not None else []
        self.sibling_of = [v if isinstance(v, PersonId) else PersonId(v) for v in self.sibling_of]

        if not isinstance(self.parent_of, list):
            self.parent_of = [self.parent_of] if self.parent_of is not None else []
        self.parent_of = [v if isinstance(v, PersonId) else PersonId(v) for v in self.parent_of]

        if not isinstance(self.child_of, list):
            self.child_of = [self.child_of] if self.child_of is not None else []
        self.child_of = [v if isinstance(v, PersonId) else PersonId(v) for v in self.child_of]

        if not isinstance(self.father_of, list):
            self.father_of = [self.father_of] if self.father_of is not None else []
        self.father_of = [v if isinstance(v, PersonId) else PersonId(v) for v in self.father_of]

        if not isinstance(self.grandparent_of, list):
            self.grandparent_of = [self.grandparent_of] if self.grandparent_of is not None else []
        self.grandparent_of = [v if isinstance(v, PersonId) else PersonId(v) for v in self.grandparent_of]

        if not isinstance(self.grandfather_of, list):
            self.grandfather_of = [self.grandfather_of] if self.grandfather_of is not None else []
        self.grandfather_of = [v if isinstance(v, PersonId) else PersonId(v) for v in self.grandfather_of]

        if not isinstance(self.grandmother_of, list):
            self.grandmother_of = [self.grandmother_of] if self.grandmother_of is not None else []
        self.grandmother_of = [v if isinstance(v, PersonId) else PersonId(v) for v in self.grandmother_of]

        if not isinstance(self.ancestor_of, list):
            self.ancestor_of = [self.ancestor_of] if self.ancestor_of is not None else []
        self.ancestor_of = [v if isinstance(v, PersonId) else PersonId(v) for v in self.ancestor_of]

        if not isinstance(self.mother_of, list):
            self.mother_of = [self.mother_of] if self.mother_of is not None else []
        self.mother_of = [v if isinstance(v, PersonId) else PersonId(v) for v in self.mother_of]

        if self.has_siblings is not None and not isinstance(self.has_siblings, Bool):
            self.has_siblings = Bool(self.has_siblings)

        if self.age_category is not None and not isinstance(self.age_category, AgeCategory):
            self.age_category = AgeCategory(self.age_category)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass
class HasAliases(YAMLRoot):
    """
    A mixin applied to any class that can have aliases/alternateNames
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.HasAliases
    class_class_curie: ClassVar[str] = "personinfo:HasAliases"
    class_name: ClassVar[str] = "HasAliases"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.HasAliases

    aliases: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass
class Organization(NamedThing):
    """
    An organization such as a company or university
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA.Organization
    class_class_curie: ClassVar[str] = "schema:Organization"
    class_name: ClassVar[str] = "Organization"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Organization

    id: Union[str, OrganizationId] = None
    name: str = None
    mission_statement: Optional[str] = None
    founding_date: Optional[str] = None
    founding_location: Optional[Union[str, PlaceId]] = None
    aliases: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OrganizationId):
            self.id = OrganizationId(self.id)

        if self.mission_statement is not None and not isinstance(self.mission_statement, str):
            self.mission_statement = str(self.mission_statement)

        if self.founding_date is not None and not isinstance(self.founding_date, str):
            self.founding_date = str(self.founding_date)

        if self.founding_location is not None and not isinstance(self.founding_location, PlaceId):
            self.founding_location = PlaceId(self.founding_location)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass
class Place(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Place
    class_class_curie: ClassVar[str] = "personinfo:Place"
    class_name: ClassVar[str] = "Place"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Place

    id: Union[str, PlaceId] = None
    name: str = None
    aliases: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PlaceId):
            self.id = PlaceId(self.id)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass
class Address(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA.PostalAddress
    class_class_curie: ClassVar[str] = "schema:PostalAddress"
    class_name: ClassVar[str] = "Address"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Address

    street: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.street is not None and not isinstance(self.street, str):
            self.street = str(self.street)

        if self.city is not None and not isinstance(self.city, str):
            self.city = str(self.city)

        if self.postal_code is not None and not isinstance(self.postal_code, str):
            self.postal_code = str(self.postal_code)

        super().__post_init__(**kwargs)


@dataclass
class Event(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Event
    class_class_curie: ClassVar[str] = "personinfo:Event"
    class_name: ClassVar[str] = "Event"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Event

    started_at_time: Optional[Union[str, XSDDate]] = None
    ended_at_time: Optional[Union[str, XSDDate]] = None
    duration: Optional[float] = None
    is_current: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.started_at_time is not None and not isinstance(self.started_at_time, XSDDate):
            self.started_at_time = XSDDate(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, XSDDate):
            self.ended_at_time = XSDDate(self.ended_at_time)

        if self.duration is not None and not isinstance(self.duration, float):
            self.duration = float(self.duration)

        if self.is_current is not None and not isinstance(self.is_current, Bool):
            self.is_current = Bool(self.is_current)

        super().__post_init__(**kwargs)


@dataclass
class Concept(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Concept
    class_class_curie: ClassVar[str] = "personinfo:Concept"
    class_name: ClassVar[str] = "Concept"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Concept

    id: Union[str, ConceptId] = None
    name: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ConceptId):
            self.id = ConceptId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class DiagnosisConcept(Concept):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.DiagnosisConcept
    class_class_curie: ClassVar[str] = "personinfo:DiagnosisConcept"
    class_name: ClassVar[str] = "DiagnosisConcept"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.DiagnosisConcept

    id: Union[str, DiagnosisConceptId] = None
    name: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DiagnosisConceptId):
            self.id = DiagnosisConceptId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ProcedureConcept(Concept):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.ProcedureConcept
    class_class_curie: ClassVar[str] = "personinfo:ProcedureConcept"
    class_name: ClassVar[str] = "ProcedureConcept"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.ProcedureConcept

    id: Union[str, ProcedureConceptId] = None
    name: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProcedureConceptId):
            self.id = ProcedureConceptId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Relationship(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = RDF.Statement
    class_class_curie: ClassVar[str] = "rdf:Statement"
    class_name: ClassVar[str] = "Relationship"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Relationship

    started_at_time: Optional[Union[str, XSDDate]] = None
    ended_at_time: Optional[Union[str, XSDDate]] = None
    related_to: Optional[Union[str, NamedThingId]] = None
    type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.started_at_time is not None and not isinstance(self.started_at_time, XSDDate):
            self.started_at_time = XSDDate(self.started_at_time)

        if self.ended_at_time is not None and not isinstance(self.ended_at_time, XSDDate):
            self.ended_at_time = XSDDate(self.ended_at_time)

        if self.related_to is not None and not isinstance(self.related_to, NamedThingId):
            self.related_to = NamedThingId(self.related_to)

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


@dataclass
class FamilialRelationship(Relationship):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.FamilialRelationship
    class_class_curie: ClassVar[str] = "personinfo:FamilialRelationship"
    class_name: ClassVar[str] = "FamilialRelationship"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.FamilialRelationship

    type: Union[str, "FamilialRelationshipType"] = None
    related_to: Union[str, PersonId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, FamilialRelationshipType):
            self.type = FamilialRelationshipType(self.type)

        if self._is_empty(self.related_to):
            self.MissingRequiredField("related_to")
        if not isinstance(self.related_to, PersonId):
            self.related_to = PersonId(self.related_to)

        super().__post_init__(**kwargs)


@dataclass
class EmploymentEvent(Event):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.EmploymentEvent
    class_class_curie: ClassVar[str] = "personinfo:EmploymentEvent"
    class_name: ClassVar[str] = "EmploymentEvent"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.EmploymentEvent

    employed_at: Optional[Union[str, OrganizationId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.employed_at is not None and not isinstance(self.employed_at, OrganizationId):
            self.employed_at = OrganizationId(self.employed_at)

        super().__post_init__(**kwargs)


@dataclass
class MedicalEvent(Event):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.MedicalEvent
    class_class_curie: ClassVar[str] = "personinfo:MedicalEvent"
    class_name: ClassVar[str] = "MedicalEvent"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.MedicalEvent

    in_location: Optional[Union[str, PlaceId]] = None
    diagnosis: Optional[Union[dict, DiagnosisConcept]] = None
    procedure: Optional[Union[dict, ProcedureConcept]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_location is not None and not isinstance(self.in_location, PlaceId):
            self.in_location = PlaceId(self.in_location)

        if self.diagnosis is not None and not isinstance(self.diagnosis, DiagnosisConcept):
            self.diagnosis = DiagnosisConcept(**as_dict(self.diagnosis))

        if self.procedure is not None and not isinstance(self.procedure, ProcedureConcept):
            self.procedure = ProcedureConcept(**as_dict(self.procedure))

        super().__post_init__(**kwargs)


@dataclass
class WithLocation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.WithLocation
    class_class_curie: ClassVar[str] = "personinfo:WithLocation"
    class_name: ClassVar[str] = "WithLocation"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.WithLocation

    in_location: Optional[Union[str, PlaceId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.in_location is not None and not isinstance(self.in_location, PlaceId):
            self.in_location = PlaceId(self.in_location)

        super().__post_init__(**kwargs)


@dataclass
class Container(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSONINFO.Container
    class_class_curie: ClassVar[str] = "personinfo:Container"
    class_name: ClassVar[str] = "Container"
    class_model_uri: ClassVar[URIRef] = PERSONINFO.Container

    persons: Optional[Union[Dict[Union[str, PersonId], Union[dict, Person]], List[Union[dict, Person]]]] = empty_dict()
    organizations: Optional[Union[Dict[Union[str, OrganizationId], Union[dict, Organization]], List[Union[dict, Organization]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="persons", slot_type=Person, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="organizations", slot_type=Organization, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations
class FamilialRelationshipType(EnumDefinitionImpl):

    SIBLING_OF = PermissibleValue(text="SIBLING_OF",
                                           meaning=FAMREL["01"])
    PARENT_OF = PermissibleValue(text="PARENT_OF",
                                         meaning=FAMREL["02"])
    CHILD_OF = PermissibleValue(text="CHILD_OF",
                                       meaning=FAMREL["01"])

    _defn = EnumDefinition(
        name="FamilialRelationshipType",
    )

class GenderType(EnumDefinitionImpl):

    _defn = EnumDefinition(
        name="GenderType",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "nonbinary man",
                PermissibleValue(text="nonbinary man",
                                 meaning=GSSO["009254"]) )
        setattr(cls, "nonbinary woman",
                PermissibleValue(text="nonbinary woman",
                                 meaning=GSSO["009253"]) )
        setattr(cls, "transgender man",
                PermissibleValue(text="transgender man",
                                 meaning=GSSO["000372"]) )
        setattr(cls, "cisgender man",
                PermissibleValue(text="cisgender man",
                                 meaning=GSSO["000371"]) )
        setattr(cls, "transgender woman",
                PermissibleValue(text="transgender woman",
                                 meaning=GSSO["000384"]) )
        setattr(cls, "cisgender woman",
                PermissibleValue(text="cisgender woman",
                                 meaning=GSSO["000385"]) )

class DiagnosisType(EnumDefinitionImpl):

    _defn = EnumDefinition(
        name="DiagnosisType",
    )

class AgeCategory(EnumDefinitionImpl):

    adult = PermissibleValue(text="adult",
                                 meaning=HSAPDV["0000087"])
    infant = PermissibleValue(text="infant",
                                   meaning=HSAPDV["0000083"])
    adolescent = PermissibleValue(text="adolescent",
                                           meaning=HSAPDV["0000086"])

    _defn = EnumDefinition(
        name="AgeCategory",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=SCHEMA.identifier, name="id", curie=SCHEMA.curie('identifier'),
                   model_uri=PERSONINFO.id, domain=None, range=URIRef)

slots.name = Slot(uri=SCHEMA.name, name="name", curie=SCHEMA.curie('name'),
                   model_uri=PERSONINFO.name, domain=None, range=str)

slots.description = Slot(uri=SCHEMA.description, name="description", curie=SCHEMA.curie('description'),
                   model_uri=PERSONINFO.description, domain=None, range=Optional[str])

slots.image = Slot(uri=SCHEMA.image, name="image", curie=SCHEMA.curie('image'),
                   model_uri=PERSONINFO.image, domain=None, range=Optional[str])

slots.gender = Slot(uri=SCHEMA.gender, name="gender", curie=SCHEMA.curie('gender'),
                   model_uri=PERSONINFO.gender, domain=None, range=Optional[Union[str, "GenderType"]])

slots.primary_email = Slot(uri=SCHEMA.email, name="primary_email", curie=SCHEMA.curie('email'),
                   model_uri=PERSONINFO.primary_email, domain=None, range=Optional[str])

slots.birth_date = Slot(uri=SCHEMA.birthDate, name="birth_date", curie=SCHEMA.curie('birthDate'),
                   model_uri=PERSONINFO.birth_date, domain=None, range=Optional[str])

slots.employed_at = Slot(uri=PERSONINFO.employed_at, name="employed_at", curie=PERSONINFO.curie('employed_at'),
                   model_uri=PERSONINFO.employed_at, domain=None, range=Optional[Union[str, OrganizationId]])

slots.is_current = Slot(uri=PERSONINFO.is_current, name="is_current", curie=PERSONINFO.curie('is_current'),
                   model_uri=PERSONINFO.is_current, domain=None, range=Optional[Union[bool, Bool]])

slots.has_employment_history = Slot(uri=PERSONINFO.has_employment_history, name="has_employment_history", curie=PERSONINFO.curie('has_employment_history'),
                   model_uri=PERSONINFO.has_employment_history, domain=None, range=Optional[Union[Union[dict, EmploymentEvent], List[Union[dict, EmploymentEvent]]]])

slots.has_medical_history = Slot(uri=PERSONINFO.has_medical_history, name="has_medical_history", curie=PERSONINFO.curie('has_medical_history'),
                   model_uri=PERSONINFO.has_medical_history, domain=None, range=Optional[Union[Union[dict, MedicalEvent], List[Union[dict, MedicalEvent]]]])

slots.has_familial_relationships = Slot(uri=PERSONINFO.has_familial_relationships, name="has_familial_relationships", curie=PERSONINFO.curie('has_familial_relationships'),
                   model_uri=PERSONINFO.has_familial_relationships, domain=None, range=Optional[Union[Union[dict, FamilialRelationship], List[Union[dict, FamilialRelationship]]]])

slots.in_location = Slot(uri=PERSONINFO.in_location, name="in_location", curie=PERSONINFO.curie('in_location'),
                   model_uri=PERSONINFO.in_location, domain=None, range=Optional[Union[str, PlaceId]])

slots.current_address = Slot(uri=PERSONINFO.current_address, name="current_address", curie=PERSONINFO.curie('current_address'),
                   model_uri=PERSONINFO.current_address, domain=None, range=Optional[Union[dict, Address]])

slots.age_in_years = Slot(uri=PERSONINFO.age_in_years, name="age_in_years", curie=PERSONINFO.curie('age_in_years'),
                   model_uri=PERSONINFO.age_in_years, domain=None, range=Optional[int])

slots.age_category = Slot(uri=PERSONINFO.age_category, name="age_category", curie=PERSONINFO.curie('age_category'),
                   model_uri=PERSONINFO.age_category, domain=None, range=Optional[Union[str, "AgeCategory"]])

slots.related_to = Slot(uri=PERSONINFO.related_to, name="related_to", curie=PERSONINFO.curie('related_to'),
                   model_uri=PERSONINFO.related_to, domain=None, range=Optional[Union[str, NamedThingId]])

slots.person_to_person_related_to = Slot(uri=PERSONINFO.person_to_person_related_to, name="person_to_person_related_to", curie=PERSONINFO.curie('person_to_person_related_to'),
                   model_uri=PERSONINFO.person_to_person_related_to, domain=None, range=Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]])

slots.ancestor_of = Slot(uri=PERSONINFO.ancestor_of, name="ancestor_of", curie=PERSONINFO.curie('ancestor_of'),
                   model_uri=PERSONINFO.ancestor_of, domain=None, range=Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]])

slots.parent_of = Slot(uri=FAMREL['02'], name="parent_of", curie=FAMREL.curie('02'),
                   model_uri=PERSONINFO.parent_of, domain=None, range=Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]])

slots.child_of = Slot(uri=PERSONINFO.child_of, name="child_of", curie=PERSONINFO.curie('child_of'),
                   model_uri=PERSONINFO.child_of, domain=None, range=Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]])

slots.father_of = Slot(uri=PERSONINFO.father_of, name="father_of", curie=PERSONINFO.curie('father_of'),
                   model_uri=PERSONINFO.father_of, domain=None, range=Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]])

slots.grandparent_of = Slot(uri=PERSONINFO.grandparent_of, name="grandparent_of", curie=PERSONINFO.curie('grandparent_of'),
                   model_uri=PERSONINFO.grandparent_of, domain=None, range=Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]])

slots.grandfather_of = Slot(uri=PERSONINFO.grandfather_of, name="grandfather_of", curie=PERSONINFO.curie('grandfather_of'),
                   model_uri=PERSONINFO.grandfather_of, domain=None, range=Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]])

slots.grandmother_of = Slot(uri=PERSONINFO.grandmother_of, name="grandmother_of", curie=PERSONINFO.curie('grandmother_of'),
                   model_uri=PERSONINFO.grandmother_of, domain=None, range=Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]])

slots.mother_of = Slot(uri=PERSONINFO.mother_of, name="mother_of", curie=PERSONINFO.curie('mother_of'),
                   model_uri=PERSONINFO.mother_of, domain=None, range=Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]])

slots.sibling_of = Slot(uri=FAMREL['01'], name="sibling_of", curie=FAMREL.curie('01'),
                   model_uri=PERSONINFO.sibling_of, domain=None, range=Optional[Union[Union[str, PersonId], List[Union[str, PersonId]]]])

slots.has_siblings = Slot(uri=PERSONINFO.has_siblings, name="has_siblings", curie=PERSONINFO.curie('has_siblings'),
                   model_uri=PERSONINFO.has_siblings, domain=None, range=Optional[Union[bool, Bool]])

slots.type = Slot(uri=PERSONINFO.type, name="type", curie=PERSONINFO.curie('type'),
                   model_uri=PERSONINFO.type, domain=None, range=Optional[str])

slots.street = Slot(uri=PERSONINFO.street, name="street", curie=PERSONINFO.curie('street'),
                   model_uri=PERSONINFO.street, domain=None, range=Optional[str])

slots.city = Slot(uri=PERSONINFO.city, name="city", curie=PERSONINFO.curie('city'),
                   model_uri=PERSONINFO.city, domain=None, range=Optional[str])

slots.mission_statement = Slot(uri=PERSONINFO.mission_statement, name="mission_statement", curie=PERSONINFO.curie('mission_statement'),
                   model_uri=PERSONINFO.mission_statement, domain=None, range=Optional[str])

slots.founding_date = Slot(uri=PERSONINFO.founding_date, name="founding_date", curie=PERSONINFO.curie('founding_date'),
                   model_uri=PERSONINFO.founding_date, domain=None, range=Optional[str])

slots.founding_location = Slot(uri=PERSONINFO.founding_location, name="founding_location", curie=PERSONINFO.curie('founding_location'),
                   model_uri=PERSONINFO.founding_location, domain=None, range=Optional[Union[str, PlaceId]])

slots.postal_code = Slot(uri=PERSONINFO.postal_code, name="postal_code", curie=PERSONINFO.curie('postal_code'),
                   model_uri=PERSONINFO.postal_code, domain=None, range=Optional[str])

slots.started_at_time = Slot(uri=PROV.startedAtTime, name="started_at_time", curie=PROV.curie('startedAtTime'),
                   model_uri=PERSONINFO.started_at_time, domain=None, range=Optional[Union[str, XSDDate]])

slots.duration = Slot(uri=PERSONINFO.duration, name="duration", curie=PERSONINFO.curie('duration'),
                   model_uri=PERSONINFO.duration, domain=None, range=Optional[float])

slots.diagnosis = Slot(uri=PERSONINFO.diagnosis, name="diagnosis", curie=PERSONINFO.curie('diagnosis'),
                   model_uri=PERSONINFO.diagnosis, domain=None, range=Optional[Union[dict, DiagnosisConcept]])

slots.procedure = Slot(uri=PERSONINFO.procedure, name="procedure", curie=PERSONINFO.curie('procedure'),
                   model_uri=PERSONINFO.procedure, domain=None, range=Optional[Union[dict, ProcedureConcept]])

slots.ended_at_time = Slot(uri=PROV.endedAtTime, name="ended_at_time", curie=PROV.curie('endedAtTime'),
                   model_uri=PERSONINFO.ended_at_time, domain=None, range=Optional[Union[str, XSDDate]])

slots.persons = Slot(uri=PERSONINFO.persons, name="persons", curie=PERSONINFO.curie('persons'),
                   model_uri=PERSONINFO.persons, domain=None, range=Optional[Union[Dict[Union[str, PersonId], Union[dict, Person]], List[Union[dict, Person]]]])

slots.organizations = Slot(uri=PERSONINFO.organizations, name="organizations", curie=PERSONINFO.curie('organizations'),
                   model_uri=PERSONINFO.organizations, domain=None, range=Optional[Union[Dict[Union[str, OrganizationId], Union[dict, Organization]], List[Union[dict, Organization]]]])

slots.hasAliases__aliases = Slot(uri=PERSONINFO.aliases, name="hasAliases__aliases", curie=PERSONINFO.curie('aliases'),
                   model_uri=PERSONINFO.hasAliases__aliases, domain=None, range=Optional[Union[str, List[str]]])

slots.related_to = Slot(uri=PERSONINFO.related_to, name="related to", curie=PERSONINFO.curie('related_to'),
                   model_uri=PERSONINFO.related_to, domain=None, range=Union[str, PersonId])

slots.Person_primary_email = Slot(uri=SCHEMA.email, name="Person_primary_email", curie=SCHEMA.curie('email'),
                   model_uri=PERSONINFO.Person_primary_email, domain=Person, range=Optional[str],
                   pattern=re.compile(r'^\S+@[\S+\.]+\S+'))

slots.Relationship_related_to = Slot(uri=RDF.object, name="Relationship_related_to", curie=RDF.curie('object'),
                   model_uri=PERSONINFO.Relationship_related_to, domain=Relationship, range=Optional[Union[str, NamedThingId]])

slots.Relationship_type = Slot(uri=RDF.predicate, name="Relationship_type", curie=RDF.curie('predicate'),
                   model_uri=PERSONINFO.Relationship_type, domain=Relationship, range=Optional[str])

slots.FamilialRelationship_type = Slot(uri=PERSONINFO.type, name="FamilialRelationship_type", curie=PERSONINFO.curie('type'),
                   model_uri=PERSONINFO.FamilialRelationship_type, domain=FamilialRelationship, range=Union[str, "FamilialRelationshipType"])

slots.FamilialRelationship_related_to = Slot(uri=PERSONINFO.related_to, name="FamilialRelationship_related to", curie=PERSONINFO.curie('related_to'),
                   model_uri=PERSONINFO.FamilialRelationship_related_to, domain=FamilialRelationship, range=Union[str, PersonId])
