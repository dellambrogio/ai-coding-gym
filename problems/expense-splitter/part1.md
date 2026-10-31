## Part 1: Equal splits

In `solution.py`, implement `class Splitter`. Amounts are integer cents.

- `add_expense(payer: str, amount: int, participants: list[str])`: `payer` paid `amount` for everyone in `participants` (which may or may not include the payer). Split it equally; if it doesn't divide evenly, the leftover cents go one each to participants in alphabetical order.
- `balances() -> dict[str, int]`: everyone who has appeared so far mapped to their net balance: positive means they're owed money, negative means they owe. Balances always sum to 0.
- Raise `ValueError` if `amount <= 0`, `participants` is empty, or has duplicates.
