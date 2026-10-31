## Part 3: Market orders

- `place(side, price, qty)` now accepts `price=None` for a **market order**: it matches against the best available prices regardless of price until filled or until the other side is empty. Any unfilled remainder is discarded, never rests, and can't be cancelled.
- The book must stay fast with many orders: `place`, `cancel`, `best_bid` and `best_ask` shouldn't scan every resting order.
