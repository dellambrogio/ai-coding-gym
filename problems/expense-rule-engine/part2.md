## Part 2: Expense rules

Implement `evaluate_rules(rules, expenses)` in `expense_engine.py` for expense-level rules (`scope == "expense"`). Return:

```python
{"expense_violations": {expense_id: [rule_id, ...]}, "trip_violations": {}}
```

listing only expenses with at least one violation, with rule ids in the order the rules were given.

Tests: `tests/test_part2_basic_rules.py`
