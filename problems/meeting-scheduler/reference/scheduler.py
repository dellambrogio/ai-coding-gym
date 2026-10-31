from __future__ import annotations

import bisect
import threading
from dataclasses import dataclass

from booking_utils import overlaps


@dataclass(frozen=True)
class Booking:
    start: int
    end: int


class MeetingScheduler:
    def __init__(self, bookings: list[Booking] | None = None) -> None:
        self.bookings: list[Booking] = sorted(
            bookings or [], key=lambda booking: booking.start)

    def earliest_available_start(self, earliest_start: int, duration: int) -> int:
        candidate = earliest_start
        for booking in self.bookings:
            if booking.end <= candidate:
                continue
            if candidate + duration <= booking.start:
                break
            candidate = booking.end
        return candidate

    def add_booking(self, start: int, end: int) -> None:
        if start >= end:
            raise ValueError("start must be before end")
        i = bisect.bisect_left([b.start for b in self.bookings], start)
        for neighbor in self.bookings[max(i - 1, 0):i + 1]:
            if overlaps(start, end, neighbor.start, neighbor.end):
                raise ValueError("booking overlaps an existing booking")
        self.bookings.insert(i, Booking(start, end))


class ThreadSafeMeetingScheduler(MeetingScheduler):
    def __init__(self, bookings: list[Booking] | None = None) -> None:
        super().__init__(bookings)
        self._lock = threading.Lock()
        self._reservation_hook = lambda: None

    def reserve_earliest_slot(self, earliest_start: int, duration: int) -> int:
        with self._lock:
            start = self.earliest_available_start(earliest_start, duration)
            self._reservation_hook()
            self.add_booking(start, start + duration)
            return start
