## Part 3: Move and find

- `mv(src, dst)`: if `dst` is an existing directory, move `src` into it (keeping its name); otherwise move/rename `src` to the path `dst`, whose parent must exist (`FileNotFoundError`). Raise `FileExistsError` if the final target path already exists, and `ValueError` when moving a directory into itself or its own subtree. Missing `src` raises `FileNotFoundError`.
- `find(path, pattern) -> list[str]`: sorted full paths of all **files** under `path` whose name matches the glob `pattern` (`*`, `?`, `[abc]`, case-sensitive, as in `fnmatch.fnmatchcase`).
