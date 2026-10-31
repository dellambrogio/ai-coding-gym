## Part 2: Time to live

Extend `put` to `put(key, value, ttl=None)`:

- `ttl` is a number of seconds. An entry put at time `t` with `ttl` expires when `clock() >= t + ttl`. `ttl=None` means it never expires.
- `get` on an expired key returns `None` and removes the entry.
- Updating a key with `put` resets its TTL (an update with `ttl=None` makes it never expire).
- Raise `ValueError` if `ttl` is not `None` and `ttl <= 0`.
