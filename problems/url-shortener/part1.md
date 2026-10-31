## Part 1: Shorten and resolve

In `solution.py`, implement `class Shortener`:

- `Shortener(clock=time.monotonic)`: `clock` returns the current time in seconds; you won't need it until part 3.
- `shorten(url: str) -> str`: return a 6-character code made of letters and digits. Shortening the same URL again returns the same code; different URLs get different codes. Raise `ValueError` unless the URL starts with `http://` or `https://`.
- `resolve(code) -> str | None`: the original URL, or `None` for an unknown code.
