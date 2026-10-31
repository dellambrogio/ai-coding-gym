from __future__ import annotations

from expense_rules import group_expenses_by_trip


def evaluate_rules(rules: list[object], expenses: list[dict[str, str]]) -> dict[str, dict[str, list[str]]]:
    expense_violations: dict[str, list[str]] = {}
    trip_violations: dict[str, list[str]] = {}

    for expense in expenses:
        hits = [rule.rule_id for rule in rules if rule.scope == "expense" and rule.matches(expense)]
        if hits:
            expense_violations[expense["expense_id"]] = hits

    for trip_id, trip_expenses in group_expenses_by_trip(expenses).items():
        hits = [rule.rule_id for rule in rules
                if rule.scope == "trip" and rule.matches_trip(trip_id, trip_expenses)]
        if hits:
            trip_violations[trip_id] = hits

    return {"expense_violations": expense_violations, "trip_violations": trip_violations}
