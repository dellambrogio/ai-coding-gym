## Part 3: Group and aggregate

`group_by(records: list[dict], key: str, aggs: dict[str, str]) -> list[dict]`:

- Group records by `record[key]`, skipping records where it's `None`. Return one dict per group, sorted by the key value ascending.
- Each output dict has `key: <value>` plus one entry per item in `aggs`, where `aggs` maps a column to `"sum"`, `"avg"`, `"min"`, `"max"` or `"count"`. The output name is `f"{column}_{op}"`.
- `None` values are ignored by every aggregate. `count` counts non-`None` values. With no values, `sum` is `0`, `count` is `0`, and `avg`/`min`/`max` are `None`.
- Raise `ValueError` for an unknown op.
