## Part 3: Several rooms

- `Calendar(rooms: int = 1)`: the calendar now manages `rooms` identical rooms. Raise `ValueError` if `rooms < 1`.
- `book` succeeds if, after adding the booking, no point in time has more than `rooms` overlapping bookings. You don't need to assign specific rooms.
- `free_slots` returns the intervals where **at least one** room is free.
- `cancel` works as before. The single-room behaviour must not change.
