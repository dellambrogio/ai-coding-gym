from __future__ import annotations

import unittest

from expense_engine import evaluate_rules
from expense_rules import (
    AmountGreaterThanPredicate,
    AndPredicate,
    FieldEqualsPredicate,
    NotPredicate,
    OrPredicate,
    PredicateExpenseRule,
)


class TestPart4CompositeRules(unittest.TestCase):
    def test_supports_and_or_and_not_rule_composition(self):
        expenses = [
            {
                "expense_id": "101",
                "trip_id": "trip-a",
                "amount_usd": "60.00",
                "expense_type": "meals",
                "vendor_type": "restaurant",
                "vendor_name": "Cafe Blue",
            },
            {
                "expense_id": "102",
                "trip_id": "trip-a",
                "amount_usd": "150.00",
                "expense_type": "entertainment",
                "vendor_type": "theater",
                "vendor_name": "Grand Stage",
            },
            {
                "expense_id": "103",
                "trip_id": "trip-a",
                "amount_usd": "40.00",
                "expense_type": "client_hosting",
                "vendor_type": "hotel",
                "vendor_name": "Park Suites",
            },
            {
                "expense_id": "104",
                "trip_id": "trip-a",
                "amount_usd": "150.00",
                "expense_type": "supplies",
                "vendor_type": "retailer",
                "vendor_name": "Staples",
            },
            {
                "expense_id": "105",
                "trip_id": "trip-a",
                "amount_usd": "150.00",
                "expense_type": "supplies",
                "vendor_type": "retailer",
                "vendor_name": "OfficeMax",
            },
        ]
        rules = [
            PredicateExpenseRule(
                "restaurant_meal_over_50",
                AndPredicate(
                    FieldEqualsPredicate("vendor_type", "restaurant"),
                    FieldEqualsPredicate("expense_type", "meals"),
                    AmountGreaterThanPredicate(50),
                ),
            ),
            PredicateExpenseRule(
                "entertainment_over_100_or_hosting",
                OrPredicate(
                    AndPredicate(
                        FieldEqualsPredicate("expense_type", "entertainment"),
                        AmountGreaterThanPredicate(100),
                    ),
                    FieldEqualsPredicate("expense_type", "client_hosting"),
                ),
            ),
            PredicateExpenseRule(
                "over_100_not_staples",
                AndPredicate(
                    AmountGreaterThanPredicate(100),
                    NotPredicate(FieldEqualsPredicate(
                        "vendor_name", "Staples")),
                ),
            ),
        ]

        result = evaluate_rules(rules, expenses)

        self.assertEqual(
            {
                "101": ["restaurant_meal_over_50"],
                "102": ["entertainment_over_100_or_hosting", "over_100_not_staples"],
                "103": ["entertainment_over_100_or_hosting"],
                "105": ["over_100_not_staples"],
            },
            result["expense_violations"],
        )
        self.assertEqual({}, result["trip_violations"])


if __name__ == "__main__":
    unittest.main()
