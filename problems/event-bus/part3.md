## Part 3: Robustness

- If a handler raises, the remaining handlers still run. Record each failure in the list attribute `errors` as `(sub_id, exception)`. `publish` returns the number of handlers called, failing ones included.
- `subscribe(topic, handler, once=False)`: a `once` subscription is removed just before its first call.
- Handlers may subscribe or unsubscribe during `publish`. The set of handlers called is fixed when `publish` starts: changes take effect from the next `publish`.
