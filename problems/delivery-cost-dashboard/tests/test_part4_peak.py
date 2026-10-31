from __future__ import annotations

import unittest

from delivery_dashboard import DeliveryCostSystem


class TestPart4Peak(unittest.TestCase):
    def test_counts_each_driver_once_even_with_overlapping_deliveries(self):
        system = DeliveryCostSystem()
        for driver_id in (1, 2, 3):
            system.add_driver(driver_id, 10.0)

        system.record_delivery(1, 0, 10)
        system.record_delivery(1, 5, 15)
        system.record_delivery(2, 7, 20)
        system.record_delivery(3, 17, 25)

        self.assertEqual(
            2, system.max_simultaneous_drivers_in_past_24_hours(30))

    def test_only_considers_the_last_24_hours(self):
        now = 100_000
        system = DeliveryCostSystem()
        system.add_driver(1, 10.0)
        system.add_driver(2, 10.0)

        system.record_delivery(1, 1_000, 2_000)
        system.record_delivery(1, 13_000, 14_000)
        system.record_delivery(2, 13_700, 15_000)

        self.assertEqual(
            2, system.max_simultaneous_drivers_in_past_24_hours(now))


if __name__ == "__main__":
    unittest.main()
