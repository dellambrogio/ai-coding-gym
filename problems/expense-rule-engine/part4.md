## Part 4: Composite rules

Policies should be combinable without writing a new class for each one. In `expense_rules.py` add predicates with a `matches(expense)` method: `FieldEqualsPredicate(field, value)`, `AmountGreaterThanPredicate(limit_usd)`, `AndPredicate(*predicates)`, `OrPredicate(*predicates)`, `NotPredicate(predicate)`, and `PredicateExpenseRule(rule_id, predicate)`, an expense rule that flags expenses matching its predicate.

Tests: `tests/test_part4_composite_rules.py`
