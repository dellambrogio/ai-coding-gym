from __future__ import annotations

import unittest

from delivery_models import calculate_delivery_cost_cents


class TestPart1Precision(unittest.TestCase):
    def test_ninety_minutes_is_not_truncated_to_one_hour(self):
        self.assertEqual(1500, calculate_delivery_cost_cents(10.0, 0, 5400))

    def test_half_hour_uses_second_precision(self):
        self.assertEqual(625, calculate_delivery_cost_cents(12.5, 100, 1900))


if __name__ == "__main__":
    unittest.main()
