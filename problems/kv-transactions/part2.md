## Part 2: Nested transactions

- `begin()`: open a new transaction. Transactions can be nested.
- `commit()`: merge the **innermost** transaction's changes into its parent (or into the main store if it's the outermost one).
- `rollback()`: discard the innermost transaction's changes.
- `commit()` or `rollback()` with no open transaction raises `RuntimeError`.

`get`, `delete` and `count` always reflect the current state, including uncommitted changes in open transactions.
