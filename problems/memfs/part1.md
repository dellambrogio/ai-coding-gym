## Part 1: Directories and files

In `solution.py`, implement `class FileSystem`. Paths are absolute, like `/a/b/c.txt`; `/` is the root.

- `mkdir(path)`: create the directory and any missing parents (like `mkdir -p`). Raise `FileExistsError` if a component of the path is an existing **file**.
- `write(path, content: str)`: create or overwrite a file. The parent directory must exist (`FileNotFoundError` otherwise). Raise `IsADirectoryError` if `path` is a directory.
- `read(path) -> str`: `FileNotFoundError` if missing, `IsADirectoryError` for a directory.
- `ls(path) -> list[str]`: for a directory, the sorted names it contains; for a file, `[file_name]`. `FileNotFoundError` if missing.
