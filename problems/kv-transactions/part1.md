## Part 1: Basic store

In `solution.py`, implement `class KVStore`:

- `set(key: str, value: str)`
- `get(key: str) -> str | None`: `None` if the key is missing.
- `delete(key: str) -> bool`: `True` if the key existed.
- `count(value: str) -> int`: how many keys currently have exactly this value.

All operations should be O(1) on average.
