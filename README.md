# linkml-datalog

Validation and inference over LinkML instance data using souffle

## Requirements

This project requires [souffle](https://souffle-lang.github.io/)

After installing souffle, install the python here is a normal way.

Until this is released to pypi:

```bash
poetry install
```

Docker containers will be provided in future

## Running

Pass in a schema and a data file

```bash
poetry run python -m linkml_datalog.engines.datalog_engine -d tmp -s personinfo.yaml example_personinfo_data.yaml
```

The output will be a ValidationReport object, in yaml

e.g.

```yaml
- type: sh:MaxValue
  subject: https://example.org/P/003
  instantiates: Person
  predicate: age_in_years
  object_str: '100001'
  info: Maximum is 999
```

Currently, to look at inferred edges, consult the directory you specified in `-d`

E.g.

`tmp/Person_grandfather_of.csv`

Will have a subject and object tuple P:005 to P:001


## How it works

 1. Schema is compiled to Souffle DL problem (see generated schema.dl file)
 2. Any embedded logic program in the schema is also added
 3. Data is converted to generic triple-like tuples (see `*.facts`)
 4. Souffle executed
 5. Inferred validation results turned into objects

Assuming input like this:

```yaml
classes:
  Person:
    attributes:
      age:
        range: integer
        maximum_value: 999
```

The generated souffle program will look like this:

```prolog
.decl Person_age_in_years_asserted(i: identifier, v: value)
.decl Person_age_in_years(i: identifier, v: value)
.output Person_age_in_years
.output Person_age_in_years_asserted
Person_age_in_years(i, v) :- 
    Person_age_in_years_asserted(i, v).
Person_age_in_years_asserted(i, v) :- 
    Person(i),
    triple(i, "https://w3id.org/linkml/examples/personinfo/age_in_years", v).

validation_result(
  "sh:MaxCountConstraintComponent",
  i,
  "Person",
  "age_in_years",
  v,
  "Maximum is 999") :-
    Person(i),
    Person_age_in_years(i, v),
    literal_number(v,num),
    num > 999.
```

`linkml_datalog.engines.datalog_engine` will do this compilation, translate your data to relational facts, then wrap calls to Souffle, exporting inferred facts to a working directory

The engine will then read back all `validation_result` facts and translate these to the LinkML validation data model (influenced by SHACL)

Currently other inferred facts are not read back in, but in future a new data object will be created.

## Motivation / Future Extensions

The above example shows functionality that could easily be achieved by other means:

 - jsonschema
 - shape languages: shex/shacl

In fact the core linkml library already has wrappers for these. See [working with data](https://linkml.io/linkml/data/index.html) in linkml guide.

However, jsonschema in particular offers very limited expressivity. There are many more opportunities for expressivity with linkml.

In particular, LinkML 1.2 introduces autoclassification rules, conditional logic, and complex expressions -- THESE ARE NOT TRANSLATED YET, but they will be in future.

For now there are three ways to get expressive logical rules in:

 1. Using existing metamodel logical slots
 2. Using dedicated *annotations* -- these may become bona fide metamodel slots in the futur
 3. including rules in the header of your schema

### Metamodel slots for expressing rules

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

### Logical annotations

Certain annotations are respected:

 - transitive
 - reflexive

Also:

```yaml
  ancestor_of:
    is_a: person_to_person_related_to
    annotations:
      transitive_closure_of: parent_of
```

these may be added as bona-fide metamodel slots in the future

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



### Schema level rules

For now, you can also include your own rules in the header of your schema as an annotation

E.g. see tests/inputs/personinfo.yaml, which has this as a schema-level annotation:

```prolog

    grandparent_of(i, j) :-
        parent_of(i, z),
        parent_of(z, j).

    grandfather_of(i, j) :-
        grandparent_of(i, j),
        is_man(i).

    grandmother_of(i, j) :-
        grandparent_of(i, j),
        is_woman(i).

    // GSSO-compliant definitions
    .decl is_man(i: identifier)
    .decl is_woman(i: identifier)
    is_man(i) :- gender(i, "http://purl.obolibrary.org/obo/GSSO_000372").
    is_man(i) :- gender(i, "http://purl.obolibrary.org/obo/GSSO_000371").
    is_woman(i) :- gender(i, "http://purl.obolibrary.org/obo/GSSO_000384").
    is_woman(i) :- gender(i, "http://purl.obolibrary.org/obo/GSSO_000385").
```

See tests for more details.

## Background

See [#196](https://github.com/linkml/linkml/discussions/196)

