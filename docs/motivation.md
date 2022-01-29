# Motivation / Future Extensions

Many of the previous examples shows functionality that could easily be achieved by other means:

 - jsonschema
 - shape languages: shex/shacl

In fact the core linkml library already has wrappers for these. See [working with data](https://linkml.io/linkml/data/index.html) in linkml guide.

However, jsonschema in particular offers very limited expressivity. There are many more opportunities for expressivity with linkml.

In particular, LinkML 1.2 introduces autoclassification rules, conditional logic, and complex expressions -- THESE ARE NOT TRANSLATED YET, but they will be in future.

For now there are three ways to get expressive logical rules in:

 1. Using existing metamodel logical slots
 2. Using dedicated *annotations* -- these may become bona fide metamodel slots in the futur
 3. including rules in the header of your schema

## Use Cases

### Biolink

TODO

### GFF3

There are many business rules that need encoded in a GFF schema:

 * if the genome is non-circular then start<=end
 * a codon is always of length 3
 * there exists some intron between two adjacent exons

See more:

 * [Formalization of Genome Interval Relations](https://www.biorxiv.org/content/10.1101/006650v1)

### Annotation QC

Many annotation systems have QC rules TODO
