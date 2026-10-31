## Part 3: Merges and freezes

- `merge_accounts(target, source) -> bool`: move `source`'s balance and spending total into `target` and delete `source` (its id can be created again later, starting fresh). Return `False` if either is missing, they're the same, or either is frozen.
- `freeze(account_id) -> bool` / `unfreeze(account_id) -> bool`: `False` if the account is missing. While frozen, `deposit`, `withdraw` and `transfer` involving that account (as sender or receiver) return `None` and change nothing. `get_balance` still works.
