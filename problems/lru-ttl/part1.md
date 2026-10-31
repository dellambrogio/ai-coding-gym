## Part 1: LRU cache

In `solution.py`, implement `class LRUCache`:

- `LRUCache(capacity: int, clock=time.monotonic)`: `capacity` is the maximum number of entries. Raise `ValueError` if `capacity < 1`. `clock` is a zero-argument function returning the current time in seconds; you won't need it until part 2, but accept it now.
- `get(key)`: return the value for `key`, or `None` if it's missing. A successful `get` makes the key the most recently used.
- `put(key, value)`: insert or update `key`. It becomes the most recently used. If inserting a new key exceeds `capacity`, evict the least recently used key.

`get` and `put` should be O(1).
