## Part 3: Wildcards

`get_all(data, path: str) -> list`: like `get`, but the path may contain wildcards:

- `.*` (or `*` at the start): every value of a dict, in insertion order
- `[*]`: every element of a list

Return all matching values in order. Branches where the path doesn't apply (missing key, wrong type) are skipped. A path without wildcards returns `[value]`, or `[]` if it's missing.

`get` and `set_path` raise `ValueError` if their path contains a wildcard.
