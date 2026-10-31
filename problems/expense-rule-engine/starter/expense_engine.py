from __future__ import annotations

from expense_rules import group_expenses_by_trip


def evaluate_rules(rules: list[object], expenses: list[dict[str, str]]) -> dict[str, dict[str, list[str]]]:
    _ = group_expenses_by_trip(expenses)
    _ = rules
    raise NotImplementedError("evaluate_rules() not implemented yet.")
