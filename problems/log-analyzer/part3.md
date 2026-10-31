## Part 3: Error rate over time

- `errors_per_minute(start: str, end: str) -> dict[str, int]`: count requests with status `>= 500` whose timestamp is in `[start, end)`. `start` and `end` are ISO timestamps like the ones in the log. Keys are the minute in the form `"2026-10-29T12:00"`. Include only minutes that have at least one error.
- Lines may arrive out of order; results must not depend on insertion order.
