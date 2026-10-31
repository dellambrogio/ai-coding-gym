from __future__ import annotations

import unittest

from booking_utils import overlaps


class TestPart1OverlapBug(unittest.TestCase):
    def test_touching_intervals_do_not_overlap(self):
        self.assertFalse(overlaps(0, 30, 30, 60))

    def test_nested_intervals_overlap(self):
        self.assertTrue(overlaps(10, 40, 20, 30))

    def test_partial_overlap_is_detected(self):
        self.assertTrue(overlaps(0, 30, 20, 50))


if __name__ == "__main__":
    unittest.main()
