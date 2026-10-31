## Part 2: Custom aliases and click counts

- `shorten(url, alias=None)`: with an `alias`, use it as the code. An alias is 3–30 characters from `A-Z a-z 0-9 _ -` (`ValueError` otherwise). If the alias is already used for a **different** URL, raise `ValueError`; for the same URL, just return it.
- A URL can have several codes (its automatic one plus aliases). `shorten(url)` without an alias still returns the URL's automatic code, creating one if needed.
- `resolve` counts a click each time it succeeds. `clicks(code) -> int`: number of clicks, `0` for unknown codes.
