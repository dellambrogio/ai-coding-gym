## Part 3: Size and smarter eviction

- `len(cache)` returns the number of entries that are **not** expired at the current `clock()` time.
- `delete(key) -> bool`: remove `key`; return `True` if a live (non-expired) entry was removed, otherwise `False`.
- When `put` inserts a new key and the cache is full, first remove **all** expired entries. Only if the cache is still full, evict the least recently used entry.
