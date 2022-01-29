# Usage

Pass in a schema and a data file

```bash
linkml-dl -d tmp -s personinfo.yaml example_personinfo_data.yaml
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

In future the inferences will be incorporated back into the core objects
