from __future__ import annotations

import unittest

from expense_engine import evaluate_rules
from expense_rules import (
    ExpenseAmountLimitRule,
    ExpenseTypeDisallowedRule,
    VendorTypeAmountLimitRule,
)
from tests.test_helpers import sample_expenses


class TestPart2BasicRules(unittest.TestCase):
    def test_flags_expected_expenses_for_basic_rules(self):
        rules = [
            VendorTypeAmountLimitRule("restaurant_over_75", "restaurant", 75),
            ExpenseTypeDisallowedRule("no_airfare", "airfare"),
            ExpenseTypeDisallowedRule("no_entertainment", "entertainment"),
            ExpenseAmountLimitRule("over_250", 250),
        ]

        result = evaluate_rules(rules, sample_expenses())

        self.assertEqual(
            {
                "003": ["restaurant_over_75"],
                "004": ["no_airfare", "over_250"],
                "007": ["no_entertainment"],
            },
            result["expense_violations"],
        )
        self.assertEqual({}, result["trip_violations"])


if __name__ == "__main__":
    unittest.main()
