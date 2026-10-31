## Part 1: Recency bug

`LruCache` in `lru_cache.py` tracks recency in `_order` (least recently used first). `keys_mru_to_lru()` should list keys from most to least recently used, but reading a key with `get` doesn't count as a use. Fix it.

Tests: `tests/test_part1_recency_bug.py`
