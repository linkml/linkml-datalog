# linkml-datalog

Validation and inference over LinkML instance data using souffle

## Requirements

This project requires [souffle](https://souffle-lang.github.io/)

After installing souffle, install the python here is a normal way.

Until this is released to pypi:

```bash
poetry install
```

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
  "sh:MaxValueTODO",
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

LinkML also has various features for boolean logic THESE ARE NOT TRANSLATED YET

You can also include your own rules in the header of your schema, e.g the following translates a 'reified' association modeling of relationships to direct slot assignments, and includes transitive inferences etc

```prolog
has_familial_relationship_to(i, p, j) :-
    Person_has_familial_relationships(i, r),
    FamilialRelationship_related_to(r, j),
    FamilialRelationship_type(r, p).

Person_parent_of(i, j) :-
    has_familial_relationship_to(i, "https://example.org/FamilialRelations#02", j).

Person_ancestor_of(i, j) :-
        Person_parent_of(i, z),
        Person_ancestor_of(z, j).

Person_ancestor_of(i, j) :-
        Person_parent_of(i, j).
```

In future these will be compilable from higher level predicates


## Background

See https://github.com/linkml/linkml/discussions/196

