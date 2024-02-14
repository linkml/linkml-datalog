# Usage

## Execution

Minimally you need to specify two inputs:

* A [linkml schema](https://linkml.io/linkml/schemas/)
* A [datafile](https://linkml.io/linkml/data/) datafile in YAML, JSON, RDF, or TSV conformant with the schema

Then run the `linkml-dl` script:

```bash
linkml-dl -d tmp -s personinfo.yaml example_personinfo_data.yaml
```

This produces two output:

- a ValidationReport object
- a new version of the data file, with new inferences injected on

## Inference Example

The following schema models friend-of-a-friend networks. It introduces
a class *Person*, with attributes:

- `friend_of` for stating one person is a friend of another
- `in_network_of` which is true if there is a chain of friendships between two people

### Schema

`foaf.yaml`:

```yaml
id: http://example.org/foaf
prefixes:
  ex: http://example.org/foaf/
  p: http://example.org/person/
  linkml: https://w3id.org/linkml/
default_prefix: ex
imports:
  - linkml:types

classes:
  Database:
    attributes:
      persons:
        range: Person
        multivalued: true
        inlined_as_list: true
  Person:
    attributes:
      name:
        identifier: true
      friend_of:
        multivalued: true
        range: Person
        symmetric: true
      in_network_of:
        range: Person
        multivalued: true
        annotations:
          transitive_closure_of: friend_of
```

note that `friend_of` is declared *transitive*, and `in_network_of` has an annotation
stating it is the *transitive closure of* `friend_of`

==Note in LinkML 1.2 there will be direct support for transitive_closure_of==

Don't worry about the `Database` class, this just acts as a holder for our
main data objects, which is a list of Persons

### Data

Data can be specified as YAML, JSON, or RDF. For simple flat schemas,
data can also be passed as TSV/CSVs.

`foaf_data.{yaml,json,tsv,ttl}`:

=== "YAML"

    ```yaml
    persons:
      - name: p:akira
        friend_of: [p:bill]
      - name: p:bill
        friend_of: [p:carrie]
      - name: p:carrie
        friend_of:
    ```

=== "JSON"

    ```json
    {
        "persons": [
            {
                "name": "p:akira",
                "friend_of": [
                    "p:bill"
                ]
            },
            {
                "name": "p:bill",
                "friend_of": [
                    "p:carrie"
                ]
            },
            {
                "name": "p:carrie",
                "friend_of": []
            }
        ],
    }
    ```

=== "TSV"

    |name|friend_of|
    |---|---|
    |p:akira|p:bill|
    |p:bill|p:carrie|
    |p:carrie||

=== "Turtle"

    ```turtle
    @prefix ns1: <http://example.org/foaf/> .

    <http://example.org/person/akira> a ns1:Person ;
        ns1:friend_of <http://example.org/person/bill> .
    <http://example.org/person/bill> a ns1:Person ;
        ns1:friend_of <http://example.org/person/carrie> .
    <http://example.org/person/carrie> a ns1:Person .

    [] a ns1:Database ;
        ns1:persons <http://example.org/person/akira>,
            <http://example.org/person/bill>,
            <http://example.org/person/carrie> .
    ```

### Execution

Once you have a schema and a data file, you can run the script:

```bash
linkml-dl -s foaf.yaml foaf_data.yaml
```

This will generate an output file that is the input injected with inferred slot-values.

```yaml
persons:
- name: p:akira
  friend_of:
  - p:bill
  in_network_of:
  - p:carrie
  - p:bill
  - p:akira
- name: p:bill
  friend_of:
  - p:carrie
  - p:akira
  in_network_of:
  - p:carrie
  - p:bill
  - p:akira
- name: p:carrie
  friend_of:
  - p:bill
  in_network_of:
  - p:carrie
  - p:bill
  - p:akira
```

## Validation Example

For example, given a simple schema modeling Person objects, including an age slot with a specified range:

### Schema

```yaml
id: http://example.org/foaf
prefixes:
  ex: http://example.org/foaf/
  p: http://example.org/person/
  linkml: https://w3id.org/linkml/
default_prefix: ex
imports:
  - linkml:types
default_curi_maps:
  - semweb_context

classes:
  Database:
    attributes:
      persons:
        range: Person
        multivalued: true
        inlined_as_list: true
  Person:
    attributes:
      name:
        identifier: true
      age_in_years:
        range: integer
        minimum_value: 0
        maximum_value: 200
```

### Data

`foaf_data.{yaml,json,tsv,ttl}`:

=== "YAML"

    ```yaml
    persons:
    - name: p:methuselah
      age_in_years: 999
    ```

=== "JSON"

    ```json
    {
        "persons": [
            {
                "name": "p:methuselah",
                "age": 999
            }
        ]
    }
    ```

=== "TSV"

    |name|age|
    |---|---|
    |p:methuselah|999|

=== "Turtle"

    ```turtle
    @prefix ns1: <http://example.org/foaf/> .

    <http://example.org/person/methuselah> a ns1:Person ;
        ns1:age_in_years 999 .

    [] a ns1:Database ;
        ns1:persons <http://example.org/person/methuselah> .
    ```

### Execution

You can execute in the same way. In this case we are not interested in new inferences,
so we can suppress the writing of the inferred object file with `--validate-only`

```bash
linkml-dl --validate-only -s foaf_validation.yaml foaf_validation_data.yaml
```

This generates a validation report object conforming to the LinkML validation schema (modeled after SHACL):

```yaml
results:
- type: sh:MaxInclusiveConstraintComponent
  subject: http://example.org/person/methuselah
  instantiates: Person
  predicate: age_in_years
  object_str: '999'
  info: Maximum is 200
```

A result of type [sh:sh:MaxInclusiveConstraintComponent](https://www.w3.org/TR/shacl/#validator-MaxInclusiveConstraintComponent)
tells us that the subject (methuselah) has an age that exceeds the maximum specified in the schema

== Note that this kind of simple validation can easily be done using frameworks like JSON-Schema, the advantage of LinkML datalog is the incoporation of expressive rules ==