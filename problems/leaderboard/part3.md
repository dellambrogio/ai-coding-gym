## Part 3: Scale

- `count_in_range(lo: int, hi: int) -> int`: number of players whose score is in `[lo, hi]`.
- The leaderboard now has tens of thousands of players. `add_score`, `top` (small `k`), `rank` and `count_in_range` must all be fast: sorting every player on each call is too slow.
