## Part 3: Retention

- `Metrics(retention: int | None = None)`: with a retention, each metric keeps only recent points. Let `latest` be the largest timestamp recorded so far for that metric (including the point being recorded). Points with `ts < latest - retention` are discarded.
- `record` now returns `bool`: `False` if the point is already too old to keep (it isn't stored), `True` otherwise.
- Without a retention nothing is ever discarded and `record` always returns `True`.
