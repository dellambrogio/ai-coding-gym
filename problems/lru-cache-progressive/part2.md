## Part 2: Eviction

The cache never enforces its capacity. When `put` adds a new key to a full cache, evict the least recently used key. Updating an existing key evicts nothing and makes it the most recently used. Think about the cost of each operation.

Tests: `tests/test_part2_capacity_eviction.py`
