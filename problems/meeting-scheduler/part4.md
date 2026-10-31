## Part 4: Concurrent reservations

Implement `ThreadSafeMeetingScheduler.reserve_earliest_slot(earliest_start, duration)`: find the earliest slot, book it and return its start. Many threads call it at once; each must get its own slot. Call `self._reservation_hook()` between finding the slot and booking it (tests use it to widen the race window).

Tests: `tests/test_part4_thread_safe_reservation.py`
