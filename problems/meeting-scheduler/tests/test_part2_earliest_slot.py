from __future__ import annotations

import unittest

from scheduler import Booking, MeetingScheduler


class TestPart2EarliestSlot(unittest.TestCase):
    def test_finds_gap_between_existing_meetings(self):
        scheduler = MeetingScheduler(
            [
                Booking(30, 60),
                Booking(90, 120),
            ]
        )
        self.assertEqual(scheduler.earliest_available_start(0, 20), 0)
        self.assertEqual(scheduler.earliest_available_start(35, 20), 60)

    def test_skips_over_blocked_window(self):
        scheduler = MeetingScheduler(
            [
                Booking(0, 45),
                Booking(45, 90),
                Booking(100, 140),
            ]
        )
        self.assertEqual(scheduler.earliest_available_start(10, 15), 140)

    def test_returns_earliest_start_after_last_booking(self):
        scheduler = MeetingScheduler([Booking(0, 15), Booking(20, 40)])
        self.assertEqual(scheduler.earliest_available_start(25, 30), 40)


if __name__ == "__main__":
    unittest.main()
