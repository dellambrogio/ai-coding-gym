from __future__ import annotations

import unittest

from delivery_dashboard import DeliveryCostSystem
from tests.test_helpers import assert_money_equal


class TestPart3Payments(unittest.TestCase):
    def test_pay_up_to_moves_completed_deliveries_out_of_unpaid_total(self):
        system = DeliveryCostSystem()
        system.add_driver(1, 10.0)
        system.add_driver(2, 12.0)

        system.record_delivery(1, 0, 3600)
        system.record_delivery(2, 0, 1800)
        system.record_delivery(2, 2000, 5600)

        assert_money_equal(self, system.get_total_cost_unpaid(), 28.0)

        system.pay_up_to(1800)
        assert_money_equal(self, system.get_total_cost_unpaid(), 22.0)

        system.pay_up_to(4000)
        assert_money_equal(self, system.get_total_cost_unpaid(), 12.0)

    def test_repeated_pay_up_to_does_not_double_pay(self):
        system = DeliveryCostSystem()
        system.add_driver(5, 18.0)
        system.record_delivery(5, 100, 1900)

        system.pay_up_to(1900)
        first_unpaid = system.get_total_cost_unpaid()
        system.pay_up_to(1900)

        assert_money_equal(self, first_unpaid, 0.0)
        assert_money_equal(self, system.get_total_cost_unpaid(), 0.0)


if __name__ == "__main__":
    unittest.main()
