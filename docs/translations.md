# Translations of LinkML to Datalog

LinkML is primarily a data modeling language in the mold of
JSON-Schema, UML, or a shape language like SHACL. The core is
deliberately simple and does not have complex semantics.

LinkML is also designed to be flexible, and there are extensions to
the language that allow for more expressivity.

## Inheritance

See: [inheritance](https://linkml.io/linkml/schemas/inheritance.html)

`is_a` and `mixin` slots are used in inference of categories.

E.g. given:

```yaml
classes:
  Person:
    is_a: NamedThing
```

the following datalog is exported:

```prolog
NamedThing(i) :- Person(i)
```

This means someone querying data for instances of NamedThing would get instances of Person

of course, a transitive hierarchy can be specified.

## Ranges

See: [ranges](https://linkml.io/linkml/schemas/slots.html#ranges)

ranges are translated into validation checks.

E.g. given:

```yaml
classes:
  Person:
    attributes:
      sibling_of: Person
```

We get:

```prolog
validation_result('sh:ClassConstraintComponent', ...) :-
  Person(i), sibling_of(i,j), ! Person(j).
```

## Inverses

Slots can be declared as [inverses](https://w3id.org/linkml/inverse):

```yaml
sibling_of:
    inverse: sibling_of
```

This will generate

```yaml
sibling_of(i,j) :- sibling_of(j,i).
```

## Association classes

Compilation to datalog will also handle associative classes (e.g. reified statements). This is very useful when we want to be able to model
associations such as familiar relationships or events such as marriage as first-class entities, but also have the convenience of a direct link:

given:

```yaml
classes:
  Relationship:
    class_uri: rdf:Statement  ## REIFICATION
    slots:
      - started_at_time
      - ended_at_time
      - related_to
      - type
    slot_usage:
      related_to:
        slot_uri: rdf:object
      type:
        slot_uri: rdf:predicate

  FamilialRelationship:
    is_a: Relationship
    slot_usage:
      type:
        range: FamilialRelationshipType
        required: true
      related to:
        range: Person
        required: true

slots:
  sibling_of:
    inverse: sibling_of
    slot_uri: famrel:01

enums:
  FamilialRelationshipType:
    permissible_values:
      SIBLING_OF:
        meaning: famrel:01
      PARENT_OF:
        meaning: famrel:02
      CHILD_OF:
        meaning: famrel:03
```

this will assert a de-reified triple:

```prolog
triple(i, p, v) :-
        triple(i, _container_prop, r),
        related_to(r, v),
        type(r, p).
```

Such that if you have instance data

```yaml
id: P:002
    has_familial_relationships:
      - related_to: P:001
        type: SIBLING_OF
```

There will be an inferred fact:

```prolog
sibling_of(P:002, P:001)
```

## Slot logical characteristics

Additional characteristics can be specified as annotations

* [annotations](https://w3id.org/linkml/annotations)

Supported:

 - transitive
 - reflexive
 - transitive_closure_of

Example:

```yaml
  ancestor_of:
    annotations:
      transitive_closure_of: parent_of
```

these will be added as bona-fide metamodel slots in LinkML 1.2.

A special annotation is `classified_from`, this can be used to auto-classify using an enum based on another slot

```yaml
slots:
  age_category:
    range: AgeCategory
    annotations:
      classified_from: age_in_years

enums:
  AgeCategory:
    permissible_values:
      adult:
        meaning: HsapDv:0000087
        annotations:
          expr: v >= 19
      infant:
        meaning: HsapDv:0000083
        annotations:
          expr: v >= 0, v <= 2
      adolescent:
        meaning: HsapDv:0000086
        annotations:
          expr: v >= 13, v <= 18
```

This can be used to auto-assign enums based on numeric values for age.

In LinkML 1.2 this will be done via classification rules.

## Other metamodel translations

"informative" parts of the model intended for humans are not translated to datalog, as they have no logical entailments

But there are other constructs coming in LinkML 1.2

 * slot relational characteristics: transitivity, symmetry, ...
 * rich expression language
 * conditional rules
 * classification rules

These will all have direct translations for datalog. For now it is necessary to manually encoded datalog rules for these.
