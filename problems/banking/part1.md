## Part 1: Accounts and transfers

In `solution.py`, implement `class Bank`. Amounts are integers (cents).

- `create_account(account_id: str) -> bool`: `False` if it already exists.
- `deposit(account_id, amount) -> int | None`: new balance, or `None` if the account doesn't exist.
- `get_balance(account_id) -> int | None`
- `transfer(src, dst, amount) -> int | None`: move money; return the new balance of `src`. Return `None` (and change nothing) if either account is missing, `src == dst`, or `src` has insufficient funds.
- Any `amount <= 0` raises `ValueError`.
