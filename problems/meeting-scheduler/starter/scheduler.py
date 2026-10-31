from __future__ import annotations

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
        raise NotImplementedError(
            "earliest_available_start() not implemented yet.")

    def add_booking(self, start: int, end: int) -> None:
        raise NotImplementedError("add_booking() not implemented yet.")


class ThreadSafeMeetingScheduler(MeetingScheduler):
    def __init__(self, bookings: list[Booking] | None = None) -> None:
        super().__init__(bookings)
        self._lock = threading.Lock()
        self._reservation_hook = lambda: None

    def reserve_earliest_slot(self, earliest_start: int, duration: int) -> int:
        raise NotImplementedError(
            "reserve_earliest_slot() not implemented yet.")
