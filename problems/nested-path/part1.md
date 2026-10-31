## Part 1: Read a path

Data is nested dicts and lists, like parsed JSON. A path looks like `users[0].address.city`:

- a key is `[A-Za-z_][A-Za-z0-9_]*`; keys after the first are preceded by `.`
- an index is `[n]` where `n` is an integer (negative counts from the end, as in Python)
- the path may start with a key or an index; the empty path `""` means the whole data

In `solution.py`, implement:

- `get(data, path: str, default=None)`: the value at `path`, or `default` if anything along the way is missing or has the wrong type (a key on a list, an index on a dict, an index out of range).
- Raise `ValueError` for a path with invalid syntax, like `"a..b"`, `"a["`, `".a"`, `"a[x]"`, `"a b"`.
