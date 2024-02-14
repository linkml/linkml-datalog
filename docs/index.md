# linkml-datalog

Validation and inference over LinkML instance data using Soufflé


![souffle logo](https://souffle-lang.github.io/img/logo-2x.png)
![linkml logo](https://avatars.githubusercontent.com/u/79337873?s=200&v=4)

=== "schema"

    ```yaml
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

=== "data"

    ```yaml
    persons:
    - name: p:akira
      friend_of: [p:bill]
    - name: p:bill
      friend_of: [p:carrie]
    - name: p:carrie
      friend_of:
    ```

=== "output"

    ```yaml
    persons:
    - name: p:akira
      friend_of:
        - p:bill
      in_network_of:
        - p:akira
        - p:bill
        - p:carrie
    - name: p:bill
      friend_of:
        - p:carrie
        - p:akira
      in_network_of:
        - p:akira
        - p:bill
        - p:carrie
    - name: p:carrie
      friend_of:
        - p:bill
      in_network_of:
        - p:akira
        - p:bill
        - p:carrie
    ```

__Caveats__

This is currently experimental/alpha software!
