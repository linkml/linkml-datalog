# Schema level rules

For now, you can also include your own rules in the header of your schema as an annotation

E.g. see tests/inputs/personinfo.yaml, which has this as a schema-level annotation:

```yaml
id: https://w3id.org/linkml/examples/personinfo

annotations:
  datalog: |-
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

See tests/ for more details.
