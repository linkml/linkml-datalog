# Translations

`is_a` and `mixin` slots are used in inference of categories.

E.g. if `Person is_a NamedThing`, then:

```prolog
NamedThing(i) :- Person(i)
```

This is also used for ranges; e.g if Person has a slot `sibling_of` which has range `Person`, this will generate:

```prolog
validation_result('sh:ClassConstraintComponent', ...) :-
  Person(i), sibling_of(i,j), ! Person(j).
```

Slots can be declared as inverses:

```yaml
sibling_of:
    is_a: person_to_person_related_to
    inverse: sibling_of
```

This will generate

```yaml
sibling_of(i,j) :- sibling_of(j,i).
```

Compilation to datalog will also handle associative classes (e.g. reified statements). E.g.

given:

```yaml
classes:
  Relationship:
    class_uri: rdf:Statement
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

There will be an inferred 

```prolog
sibling_of(P:002, P:001)
```
