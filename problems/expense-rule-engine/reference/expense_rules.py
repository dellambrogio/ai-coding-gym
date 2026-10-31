from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from typing import Sequence


def amount_to_cents(amount_text: str) -> int:
    amount = Decimal(amount_text) * Decimal("100")
    return int(amount.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def amount_exceeds(amount_text: str, threshold_usd: float) -> bool:
    return Decimal(amount_text) > Decimal(str(threshold_usd))


def group_expenses_by_trip(expenses: Sequence[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for expense in expenses:
        grouped[expense["trip_id"]].append(expense)
    return grouped


class ExpenseRule:
    scope = "expense"

    def __init__(self, rule_id: str) -> None:
        self.rule_id = rule_id

    def matches(self, expense: dict[str, str]) -> bool:
        raise NotImplementedError


class TripRule:
    scope = "trip"

    def __init__(self, rule_id: str) -> None:
        self.rule_id = rule_id

    def matches_trip(self, trip_id: str, expenses: Sequence[dict[str, str]]) -> bool:
        raise NotImplementedError


class VendorTypeAmountLimitRule(ExpenseRule):
    def __init__(self, rule_id: str, vendor_type: str, amount_limit_usd: float) -> None:
        super().__init__(rule_id)
        self.vendor_type = vendor_type
        self.amount_limit_usd = amount_limit_usd

    def matches(self, expense: dict[str, str]) -> bool:
        return expense.get("vendor_type") == self.vendor_type and amount_exceeds(
            expense["amount_usd"],
            self.amount_limit_usd,
        )


class ExpenseTypeDisallowedRule(ExpenseRule):
    def __init__(self, rule_id: str, expense_type: str) -> None:
        super().__init__(rule_id)
        self.expense_type = expense_type

    def matches(self, expense: dict[str, str]) -> bool:
        return expense.get("expense_type") == self.expense_type


class ExpenseAmountLimitRule(ExpenseRule):
    def __init__(self, rule_id: str, amount_limit_usd: float) -> None:
        super().__init__(rule_id)
        self.amount_limit_usd = amount_limit_usd

    def matches(self, expense: dict[str, str]) -> bool:
        return amount_exceeds(expense["amount_usd"], self.amount_limit_usd)


class TripTotalLimitRule(TripRule):
    def __init__(self, rule_id: str, amount_limit_usd: float) -> None:
        super().__init__(rule_id)
        self.amount_limit_cents = amount_to_cents(str(amount_limit_usd))

    def matches_trip(self, trip_id: str, expenses: Sequence[dict[str, str]]) -> bool:
        total_cents = sum(amount_to_cents(
            expense["amount_usd"]) for expense in expenses)
        return total_cents > self.amount_limit_cents


class TripCategoryLimitRule(TripRule):
    def __init__(self, rule_id: str, expense_type: str, amount_limit_usd: float) -> None:
        super().__init__(rule_id)
        self.expense_type = expense_type
        self.amount_limit_cents = amount_to_cents(str(amount_limit_usd))

    def matches_trip(self, trip_id: str, expenses: Sequence[dict[str, str]]) -> bool:
        total_cents = sum(
            amount_to_cents(expense["amount_usd"])
            for expense in expenses
            if expense.get("expense_type") == self.expense_type
        )
        return total_cents > self.amount_limit_cents


class Predicate:
    def matches(self, expense: dict[str, str]) -> bool:
        raise NotImplementedError


class FieldEqualsPredicate(Predicate):
    def __init__(self, field: str, value: str) -> None:
        self.field = field
        self.value = value

    def matches(self, expense: dict[str, str]) -> bool:
        return expense.get(self.field) == self.value


class AmountGreaterThanPredicate(Predicate):
    def __init__(self, amount_limit_usd: float) -> None:
        self.amount_limit_usd = amount_limit_usd

    def matches(self, expense: dict[str, str]) -> bool:
        return amount_exceeds(expense["amount_usd"], self.amount_limit_usd)


class AndPredicate(Predicate):
    def __init__(self, *predicates: Predicate) -> None:
        self.predicates = predicates

    def matches(self, expense: dict[str, str]) -> bool:
        return all(p.matches(expense) for p in self.predicates)


class OrPredicate(Predicate):
    def __init__(self, *predicates: Predicate) -> None:
        self.predicates = predicates

    def matches(self, expense: dict[str, str]) -> bool:
        return any(p.matches(expense) for p in self.predicates)


class NotPredicate(Predicate):
    def __init__(self, predicate: Predicate) -> None:
        self.predicate = predicate

    def matches(self, expense: dict[str, str]) -> bool:
        return not self.predicate.matches(expense)


class PredicateExpenseRule(ExpenseRule):
    def __init__(self, rule_id: str, predicate: Predicate) -> None:
        super().__init__(rule_id)
        self.predicate = predicate

    def matches(self, expense: dict[str, str]) -> bool:
        return self.predicate.matches(expense)
