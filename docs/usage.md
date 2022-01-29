# Usage

## Validation

Minimally you need to specify two inputs:

* A [linkml schema](https://linkml.io/linkml/schemas)
* A datafile in YAML, JSON, RDF, or TSV conformant with the schema

The current main use case is data validation. Pass in your schema and data:

```bash
linkml-dl -d tmp -s personinfo.yaml example_personinfo_data.yaml
```

The output will be a ValidationReport object, in yaml

For example, given a simple schema modeling Person objects, including an age slot with a specified range:

```yaml
id: https://w3id.org/linkml/examples/personinfo
name: personinfo
description: |-
  Simple demo person schema
default_curi_maps:
  - semweb_context
imports:
  - linkml:types
prefixes:
  personinfo: https://w3id.org/linkml/examples/personinfo/
  linkml: https://w3id.org/linkml/
  P: https://example.org/P/
default_prefix: personinfo
default_range: string

classes:

  Container:
    tree_root: true
    attributes:
      persons:
        range: Person
        inlined: true
        inlined_as_list: true
        multivalued: true
        
  Person:
    description: >-
      A person (alive, dead, undead, or fictional).
    attributes:
      id:
        identifier: true
        slot_uri: schema:identifier
      name:
        slot_uri: schema:name
        required: true
      age_in_years:
        range: integer
        minimum_value: 0
        maximum_value: 999
```

Data a data object:

```yaml
persons:
  - id: P:003
    name: bobby
    age_in_years: 100001
```

Then we will get a validation result object telling us we have violated a MaxValue constraint:

```yaml
- type: sh:MaxValue
  subject: https://example.org/P/003
  instantiates: Person
  predicate: age_in_years
  object_str: '100001'
  info: Maximum is 999
```

Note that this in itself is not so impressive - it is more
conventional to use something like jsonschema or the builtin linkml
validator to do this kind of task.

However, because we are using a datalog engine behind the scenes we can do more powerful inferences and checks

## Inferring new slot values

The above example demonstrates the validation use case.

We can also add information to the schema about transitive relations as well as custom rules.

For example:

```bash
linkml-dl -s tests/inputs/personinfo.yaml tests/inputs/example_personinfo_data.yaml -d tmp
```

If the input set of objects include:

```yaml
  - id: P:001
  - id: P:004
    has_familial_relationships:
      - related_to: P:001
        type: PARENT_OF
  - id: P:005
    has_familial_relationships:
      - related_to: P:004
        type: PARENT_OF
    gender: cisgender man
```

and the schema has a schema-level rules:

```yaml
annotations:
  datalog: |-

    grandparent_of(i, j) :-
        parent_of(i, z),
        parent_of(z, j).

    grandfather_of(i, j) :-
        grandparent_of(i, j),
        is_man(i).
```

(TODO: this can be specified in a more compact way now with annotations on predicates)

the above exert elides some details but the basic idea is that we have transitive slot values inferred. Currently, to see these, consult the directory you specified in `-d` E.g. `tmp/Person_grandfather_of.csv`

|id|grandfather_of|
|---|---|
|https://example.org/P/005|https://example.org/P/001|

In future the inferences will be incorporated back into the core objects
