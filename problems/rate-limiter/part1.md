## Part 1: Sliding window limiter

In `solution.py`, implement `class RateLimiter`:

- `RateLimiter(limit: int, window: float, clock=time.monotonic)`: each client may make at most `limit` requests in any sliding window of `window` seconds. `clock` is a zero-argument function returning the current time in seconds.
- `allow(client_id) -> bool`: record a request from `client_id` at `clock()` and return whether it is allowed.
  - A request at time `now` is allowed if fewer than `limit` **allowed** requests from that client happened in the interval `(now - window, now]`.
  - Denied requests are not recorded and don't count against the limit.
- Clients are independent.
- Raise `ValueError` if `limit < 1` or `window <= 0`.
