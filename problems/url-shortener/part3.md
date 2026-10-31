## Part 3: Expiry and deletion

- `shorten(url, alias=None, ttl=None)`: `ttl` in seconds (`ValueError` if `<= 0`). A code created at time `t` expires when `clock() >= t + ttl`. If the URL already has a live automatic code, `shorten(url)` returns it unchanged (ignoring `ttl`).
- Expired codes behave as if they never existed: `resolve` returns `None`, `clicks` returns `0`, the alias can be taken by any URL, and `shorten(url)` creates a new automatic code.
- `delete(code) -> bool`: remove a live code. `False` if it doesn't exist or has expired.
