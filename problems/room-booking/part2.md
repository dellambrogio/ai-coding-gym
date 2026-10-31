## Part 2: Cancel and find free time

- `cancel(start: int, end: int) -> bool`: remove a booking with exactly these bounds. Return `False` if there is none.
- `free_slots(day_start: int, day_end: int, min_length: int = 1) -> list[tuple[int, int]]`: the maximal free intervals inside `[day_start, day_end)`, sorted, keeping only those with length `>= min_length`. Bookings that stick out of the range are clipped to it.
