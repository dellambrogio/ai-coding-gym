## Part 1: Amounts

An expense policy checker. Expenses are dicts of strings (`expense_id`, `trip_id`, `amount_usd`, `expense_type`, `vendor_type`, `vendor_name`); rules in `expense_rules.py` flag the ones that break company policy.

`amount_exceeds("100.00", 75)` returns `False`. Amounts must be compared as numbers: fix it.

Tests: `tests/test_part1_amounts.py`
