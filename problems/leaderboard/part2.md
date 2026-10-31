## Part 2: Rank and reset

- `rank(player) -> int | None`: competition ranking: `1 +` the number of players with a strictly higher score (so ties share a rank: 1, 2, 2, 4). `None` for unknown players.
- `reset(player) -> bool`: remove the player entirely. `False` if unknown.
