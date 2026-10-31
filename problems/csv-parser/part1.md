## Part 1: Parse CSV

In `solution.py`, implement `parse_csv(text: str) -> list[list[str]]` without using the `csv` module:

- Fields are separated by `,`; rows by `\n` or `\r\n`.
- A field may be wrapped in double quotes. Inside quotes, commas and newlines are part of the field, and `""` stands for one `"`.
- A trailing newline at the end of the text doesn't create an extra row. Empty lines are skipped.
- Raise `ValueError` if a quoted field is never closed.
