## Part 1: Matching orders

In `solution.py`, implement `class OrderBook` for a single stock:

- `place(side: str, price: int, qty: int) -> tuple[int, list]`: `side` is `"buy"` or `"sell"`. Returns `(order_id, trades)`; order ids start at 1 and increase.
  - A buy matches resting sells with price `<=` its price, best (lowest) price first; a sell matches resting buys with price `>=` its price, best (highest) first. At the same price, older orders match first.
  - Each trade is `(buy_order_id, sell_order_id, price, qty)` and executes at the **resting** order's price.
  - Whatever quantity is left after matching rests in the book.
- `best_bid() -> int | None`: highest resting buy price. `best_ask() -> int | None`: lowest resting sell price.
- Raise `ValueError` for an invalid side or a `price`/`qty` that isn't a positive integer.
