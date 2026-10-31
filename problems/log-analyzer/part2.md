## Part 2: Paths and latency

From now on, the **path** is the part before any `?` (the query string is ignored).

- `top_paths(n: int) -> list[tuple[str, int]]`: the `n` most requested paths with their counts, sorted by count descending, then path ascending.
- `p95_latency(path_prefix: str = "") -> int | None`: the 95th percentile latency in ms of requests whose path starts with `path_prefix`, using the **nearest-rank** method: sort the latencies and take the element at 1-based rank `ceil(0.95 * N)`. Return `None` if no requests match.
