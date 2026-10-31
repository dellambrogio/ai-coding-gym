import random
import time

from solution import OrderBook


def test_market_buy_sweeps():
    b = OrderBook()
    s1, _ = b.place("sell", 100, 2)
    s2, _ = b.place("sell", 500, 2)
    m, trades = b.place("buy", None, 3)
    assert trades == [(m, s1, 100, 2), (m, s2, 500, 1)]


def test_market_remainder_discarded():
    b = OrderBook()
    b.place("buy", 100, 2)
    m, trades = b.place("sell", None, 5)
    assert sum(t[3] for t in trades) == 2
    assert b.best_ask() is None and b.best_bid() is None
    assert b.cancel(m) is False


def test_market_on_empty_book():
    b = OrderBook()
    _, trades = b.place("buy", None, 1)
    assert trades == [] and b.best_bid() is None


def test_many_orders_fast():
    rnd = random.Random(3)
    b = OrderBook()
    ids = []
    start = time.perf_counter()
    for i in range(60_000):
        side = rnd.choice(["buy", "sell"])
        price = rnd.randint(900, 1000) if side == "buy" else rnd.randint(1001, 1100)
        oid, _ = b.place(side, price, rnd.randint(1, 10))
        ids.append(oid)
        if i % 3 == 0:
            b.cancel(rnd.choice(ids))
        b.best_bid()
        b.best_ask()
    assert time.perf_counter() - start < 3
