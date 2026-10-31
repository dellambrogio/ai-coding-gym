## Part 1: Record and query

In `solution.py`, implement `class Metrics`:

- `record(name: str, ts: int, value: float)`: store a data point. Points can arrive in any order; several points may share a timestamp.
- `query(name, start: int, end: int, agg: str)`: aggregate the points of `name` with `start <= ts < end`. `agg` is `"sum"`, `"count"`, `"avg"`, `"min"` or `"max"`. With no points, `sum` and `count` return `0`, the others `None`. Unknown metric names have no points. Raise `ValueError` for an unknown `agg`.
- Queries over large series must be fast: don't scan all points of a metric on every query.
