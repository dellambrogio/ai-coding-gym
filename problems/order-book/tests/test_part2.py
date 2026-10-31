from solution import OrderBook


def test_cancel():
    b = OrderBook()
    oid, _ = b.place("buy", 100, 5)
    assert b.cancel(oid) is True
    assert b.best_bid() is None
    assert b.cancel(oid) is False


def test_cancel_filled_or_unknown():
    b = OrderBook()
    s, _ = b.place("sell", 100, 1)
    b.place("buy", 100, 1)
    assert b.cancel(s) is False
    assert b.cancel(999) is False


def test_cancelled_order_does_not_match():
    b = OrderBook()
    s1, _ = b.place("sell", 100, 1)
    s2, _ = b.place("sell", 101, 1)
    b.cancel(s1)
    bid, trades = b.place("buy", 101, 1)
    assert trades == [(bid, s2, 101, 1)]


def test_depth():
    b = OrderBook()
    for p, q in [(99, 5), (100, 2), (99, 3), (97, 1)]:
        b.place("buy", p, q)
    for p, q in [(105, 1), (103, 4)]:
        b.place("sell", p, q)
    assert b.depth("buy", 2) == [(100, 2), (99, 8)]
    assert b.depth("sell", 5) == [(103, 4), (105, 1)]


def test_depth_reflects_partial_fills():
    b = OrderBook()
    b.place("sell", 100, 10)
    b.place("buy", 100, 4)
    assert b.depth("sell", 1) == [(100, 6)]
