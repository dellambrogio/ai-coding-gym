## Part 2: Withdrawals and top spenders

- `withdraw(account_id, amount) -> int | None`: new balance; `None` if the account is missing or has insufficient funds.
- `top_spenders(n: int) -> list[tuple[str, int]]`: the `n` accounts with the most money sent out (outgoing transfers plus withdrawals), as `(account_id, total)`, sorted by total descending, then id ascending. Accounts that spent nothing are included with `0`.
