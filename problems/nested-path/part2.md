## Part 2: Write a path

`set_path(data, path: str, value)`: set the value at `path`, changing `data` in place.

- Missing dict keys along the way are created: as a `dict` if the next step is a key, as a `list` if the next step is an index.
- For lists, an index equal to `len(list)` appends; a larger index raises `IndexError`. Negative indexes must already exist.
- Using a key on something that isn't a dict, or an index on something that isn't a list, raises `TypeError`.
- The empty path raises `ValueError`.
