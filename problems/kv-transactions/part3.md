## Part 3: Scale

- `keys_with_prefix(prefix: str) -> list[str]`: sorted list of keys that currently exist and start with `prefix`, including uncommitted changes.
- Performance: `set`, `get`, `delete` and `count` must stay fast with many keys and deep nesting. For example, 100 nested transactions with 1,000 writes each, then rolling them all back, should take well under a second. `begin()` must not copy the whole store.
