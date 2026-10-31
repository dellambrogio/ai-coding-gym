import pytest
from solution import OrderBook


def test_resting_orders_and_best_prices():
    b = OrderBook()
    assert b.best_bid() is None and b.best_ask() is None
    b.place("buy", 99, 10)
    b.place("buy", 100, 5)
    b.place("sell", 105, 3)
    assert b.best_bid() == 100 and b.best_ask() == 105


def test_ids_increase():
    b = OrderBook()
    assert b.place("buy", 10, 1)[0] == 1
    assert b.place("sell", 20, 1)[0] == 2


def test_full_match_at_resting_price():
    b = OrderBook()
    s, _ = b.place("sell", 100, 5)
    bid, trades = b.place("buy", 102, 5)
    assert trades == [(bid, s, 100, 5)]
    assert b.best_ask() is None and b.best_bid() is None


def test_partial_fill_rests_remainder():
    b = OrderBook()
    s, _ = b.place("sell", 100, 3)
    bid, trades = b.place("buy", 100, 5)
    assert trades == [(bid, s, 100, 3)]
    assert b.best_bid() == 100 and b.best_ask() is None


def test_sweeps_multiple_levels_best_first():
    b = OrderBook()
    s1, _ = b.place("sell", 101, 2)
    s2, _ = b.place("sell", 100, 2)
    s3, _ = b.place("sell", 105, 2)
    bid, trades = b.place("buy", 103, 5)
    assert trades == [(bid, s2, 100, 2), (bid, s1, 101, 2)]
    assert b.best_bid() == 103 and b.best_ask() == 105


def test_time_priority_at_same_price():
    b = OrderBook()
    b1, _ = b.place("buy", 50, 1)
    b2, _ = b.place("buy", 50, 1)
    s, trades = b.place("sell", 50, 1)
    assert trades == [(b1, s, 50, 1)]


def test_sell_matches_highest_bid():
    b = OrderBook()
    b1, _ = b.place("buy", 98, 1)
    b2, _ = b.place("buy", 99, 1)
    s, trades = b.place("sell", 97, 2)
    assert trades == [(b2, s, 99, 1), (b1, s, 98, 1)]


def test_no_cross_no_trade():
    b = OrderBook()
    b.place("buy", 99, 1)
    _, trades = b.place("sell", 100, 1)
    assert trades == []


@pytest.mark.parametrize("args", [("hold", 10, 1), ("buy", 0, 1), ("buy", 10, 0), ("sell", -1, 1), ("buy", 10, 1.5)])
def test_invalid_orders(args):
    with pytest.raises(ValueError):
        OrderBook().place(*args)
