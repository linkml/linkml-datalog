# How it works

## Overview

The linkml-dl wrapper works by executing the following steps:

- The schema is compiled to Souffle DL problem (see generated schema.dl file)
- Any embedded logic program in the schema is also added
- Data is converted to generic triple-like tuples (see `*.facts`)
- Souffle is executed
- Inferred facts are collected:
    - validation results are collected into a results object
    - inferred facts are incorporated into new copy of the input object

## Compilation of schemas to Datalog

Assuming input like this:

```yaml
classes:
  Person:
    class_uri: schema:Person
    attributes:
      age_in_years:
        range: integer
        maximum_value: 999
```

The generated souffle program will look like this:

```prolog
.decl Person(i: symbol)
.decl Person_asserted(i: identifier)
.output Person
Person_asserted(i) :- triple(i, RDF_TYPE, "http://schema.org/Person").
Person(i) :- Person_asserted(i).

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

(note that most users never need to see these programs, but if you want to write advanced rules it is useful to understand the structure)

## Conversion of data to Facts

The LinkML data file is converted to a triple-like model following the souffle spec:

```prolog
.decl triple(s:symbol, p:symbol, o:symbol)
.decl literal_number(s:symbol, o:number)
.decl literal_symbol(s:symbol, o:symbol)
```

Under the hood, this is a two step process:

1. convert the data to RDF using the [standard rdflib dumper](https://linkml.io/linkml/data/rdf.html)
2. convert triple to the tuples above
    - each triple is mapped to triple/3 facts
    - if the object is a literal:
         - it is serialized as a json string
         - an additional fact is added mapping this to a souffle number or symbol

Every slot-value assignment is turned into a triple. If the value is a literal/atom then an additional fact is added mapping the node to the number or symbol value.

## Execution

`linkml_datalog.engines.datalog_engine` will do this compilation, translate your data to relational facts, then wrap calls to Souffle

Note that Souffle needs to be on the command line for this to work

Generated programs and facts will be placed in a temporary working directory, unless `-d` is passed.

## Parsing

The engine will then read back all `validation_result` facts and translate these to the LinkML validation data model,
and will walk the input object reading any new inferences

