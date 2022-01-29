# Logical annotations

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

