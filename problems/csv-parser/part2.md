## Part 2: Typed records

`read_records(text: str) -> list[dict]`: the first row is the header; each later row becomes a dict.

- Convert values: `""` → `None`; integers like `42`, `-7` → `int`; decimals like `3.5`, `-0.25`, `.5` → `float`; `true`/`false` (any case) → `bool`; anything else stays a string.
- Raise `ValueError` if the header has duplicate names, or a row has a different number of fields than the header.
- Empty text returns `[]`.
