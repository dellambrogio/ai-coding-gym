## Part 2: Append, size, remove

- `append(path, content: str)`: add to the end of a file, creating it if missing (same parent rules as `write`).
- `size(path) -> int`: length of a file's content; for a directory, the total size of all files under it.
- `rm(path, recursive=False)`: remove a file or directory. Removing a non-empty directory without `recursive=True` raises `OSError`. Removing `/` raises `ValueError`. Missing path raises `FileNotFoundError`.
