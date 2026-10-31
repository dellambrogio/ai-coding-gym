## Part 1: Scores and top players

In `solution.py`, implement `class Leaderboard`:

- `add_score(player: str, points: int)`: add `points` to the player's total (new players start at 0). Raise `ValueError` if `points <= 0`.
- `score(player) -> int`: total score, `0` if unknown.
- `top(k: int) -> list[tuple[str, int]]`: the `k` best players as `(player, score)`, sorted by score descending, then name ascending.
