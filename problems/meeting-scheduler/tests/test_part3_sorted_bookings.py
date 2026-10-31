from __future__ import annotations

import unittest

from scheduler import Booking, MeetingScheduler


class TestPart3SortedBookings(unittest.TestCase):
    def test_inserts_and_keeps_bookings_sorted(self):
        scheduler = MeetingScheduler([Booking(30, 60), Booking(90, 120)])
        scheduler.add_booking(60, 75)
        scheduler.add_booking(0, 20)
        self.assertEqual(scheduler.bookings, [Booking(0, 20), Booking(
            30, 60), Booking(60, 75), Booking(90, 120)])

    def test_rejects_overlapping_booking(self):
        scheduler = MeetingScheduler([Booking(30, 60)])
        with self.assertRaises(ValueError):
            scheduler.add_booking(50, 80)

    def test_rejects_invalid_interval(self):
        scheduler = MeetingScheduler()
        with self.assertRaises(ValueError):
            scheduler.add_booking(25, 25)


if __name__ == "__main__":
    unittest.main()
