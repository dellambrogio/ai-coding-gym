from __future__ import annotations

import unittest

from delivery_dashboard import DeliveryCostSystem
from tests.test_helpers import assert_money_equal


class TestPart2LiveTotal(unittest.TestCase):
    def test_tracks_total_cost_across_multiple_drivers(self):
        system = DeliveryCostSystem()
        system.add_driver(1, 10.0)
        system.add_driver(2, 12.0)

        system.record_delivery(1, 0, 5400)
        system.record_delivery(2, 0, 1800)

        assert_money_equal(self, system.get_total_cost(), 21.0)

    def test_overlapping_deliveries_are_paid_independently(self):
        system = DeliveryCostSystem()
        system.add_driver(7, 20.0)

        system.record_delivery(7, 0, 3600)
        system.record_delivery(7, 1800, 5400)

        assert_money_equal(self, system.get_total_cost(), 40.0)


if __name__ == "__main__":
    unittest.main()
