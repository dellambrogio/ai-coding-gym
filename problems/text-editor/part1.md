## Part 1: Typing and cursor

In `solution.py`, implement `class Editor`:

- attributes `text: str` (starts `""`) and `cursor: int` (starts `0`, always between `0` and `len(text)`).
- `type(s: str)`: insert `s` at the cursor; the cursor moves to just after the inserted text.
- `move(pos: int)`: move the cursor to `pos`, clamped to the valid range.
- `backspace(n: int = 1)`: delete up to `n` characters before the cursor.
