from __future__ import annotations

import unittest

from expense_engine import evaluate_rules
from expense_rules import (
    ExpenseAmountLimitRule,
    ExpenseTypeDisallowedRule,
    TripCategoryLimitRule,
    TripTotalLimitRule,
    VendorTypeAmountLimitRule,
)
from tests.test_helpers import sample_expenses


class TestPart3TripRules(unittest.TestCase):
    def test_reports_trip_level_violations_alongside_expense_violations(self):
        rules = [
            VendorTypeAmountLimitRule("restaurant_over_75", "restaurant", 75),
            ExpenseTypeDisallowedRule("no_airfare", "airfare"),
            ExpenseTypeDisallowedRule("no_entertainment", "entertainment"),
            ExpenseAmountLimitRule("over_250", 250),
            TripTotalLimitRule("trip_over_2000", 2000),
            TripCategoryLimitRule("meals_over_200", "meals", 200),
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
        self.assertEqual(
            {
                "002": ["trip_over_2000", "meals_over_200"],
            },
            result["trip_violations"],
        )


if __name__ == "__main__":
    unittest.main()
