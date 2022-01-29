# Basics

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
