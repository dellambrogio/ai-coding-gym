## Part 1: Suggestions

In `solution.py`, implement `class Autocomplete`:

- `add(word: str, weight: int = 1)`: add `weight` to the word's score (new words start at 0). Words are case-insensitive: store them lowercased. Raise `ValueError` if `weight <= 0`.
- `suggest(prefix: str, k: int = 5) -> list[str]`: up to `k` words starting with `prefix` (case-insensitive), by score descending, then alphabetically.
