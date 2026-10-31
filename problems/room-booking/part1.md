## Part 1: Book a room

In `solution.py`, implement `class Calendar`:

- `Calendar()`: one meeting room.
- `book(start: int, end: int) -> bool`: book the half-open interval `[start, end)`. Return `True` and store it if it doesn't overlap any existing booking, otherwise return `False` and store nothing. Touching intervals like `[1, 3)` and `[3, 5)` don't overlap.
- Raise `ValueError` if `start >= end`.
