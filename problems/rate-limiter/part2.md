## Part 2: Overrides and retry hints

- `set_limit(client_id, limit)`: give one client its own limit (same window). It applies to requests from now on; requests already recorded still count. Raise `ValueError` if `limit < 1`.
- `retry_after(client_id) -> float`: how many seconds from now until `allow(client_id)` would return `True`, assuming no other requests happen. Return `0` if it would be allowed right now. This must not record a request.
