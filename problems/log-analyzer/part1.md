## Part 1: Parse and count

Each log line has five space-separated fields:

```
2026-10-29T12:00:01Z GET /api/users?id=7 200 123ms
<timestamp>          <method> <path> <status> <latency>
```

- timestamp: ISO 8601 in UTC, ending in `Z`
- method: one of `GET POST PUT PATCH DELETE`
- path: starts with `/`
- status: integer from 100 to 599
- latency: a non-negative integer followed by `ms`

In `solution.py`, implement `class LogAnalyzer`:

- `add(line: str) -> bool`: parse and store one line. Return `False` and store nothing if the line is malformed (wrong number of fields or any invalid field). Surrounding whitespace is fine.
- `malformed: int` attribute: number of malformed lines seen.
- `count_by_status() -> dict[int, int]`: number of valid lines per status code.
