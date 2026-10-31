## Part 2: Cancel and depth

- `cancel(order_id) -> bool`: remove a resting order. `False` if it's unknown, already fully filled, or already cancelled.
- `depth(side: str, levels: int) -> list[tuple[int, int]]`: the best `levels` price levels on that side as `(price, total_resting_qty)`, best first (highest first for `"buy"`, lowest first for `"sell"`).
