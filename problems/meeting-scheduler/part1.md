## Part 1: Overlap bug

A room booking service. Bookings are half-open intervals `[start, end)` in minutes, so a meeting ending at 30 and one starting at 30 don't overlap.

`booking_utils.overlaps` gets this wrong: fix it.

Tests: `tests/test_part1_overlap_bug.py`
