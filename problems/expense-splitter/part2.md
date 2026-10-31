## Part 2: Settling up

- `add_payment(sender, receiver, amount)`: `sender` paid `receiver` directly (e.g. paying back a debt). `ValueError` if `amount <= 0` or `sender == receiver`.
- `settle() -> list[tuple[str, str, int]]`: a list of `(from, to, amount)` transfers that would bring every balance to 0, using this greedy rule: repeatedly take the person who owes the most and the person who is owed the most (ties broken alphabetically), and transfer the smaller of the two amounts. `settle` doesn't change any balances.
