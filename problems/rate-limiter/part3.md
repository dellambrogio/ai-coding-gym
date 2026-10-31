## Part 3: Weighted requests

Some requests are more expensive. Change the signatures to:

- `allow(client_id, cost=1) -> bool`: allowed if the total cost of allowed requests in `(now - window, now]` plus `cost` is `<= limit`. If allowed, the request is recorded with its cost.
- `retry_after(client_id, cost=1) -> float`: seconds until a request of this `cost` would be allowed. If `cost` is larger than the client's limit, it can never be allowed: return `math.inf`.
- Raise `ValueError` if `cost < 1`.

The old behaviour (cost 1) must keep working.
