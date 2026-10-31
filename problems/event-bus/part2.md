## Part 2: Wildcards

Subscription topics may contain wildcards:

- `*` matches exactly one segment: `orders.*` matches `orders.created` but not `orders` or `orders.eu.created`.
- `#` matches zero or more segments and may only be the last segment: `orders.#` matches `orders`, `orders.created` and `orders.eu.created`. `#` alone matches everything.

Handlers are still called in subscription order. `subscribe` raises `ValueError` for an empty segment or a `#` that isn't last. `publish` raises `ValueError` if its topic contains `*` or `#`.
