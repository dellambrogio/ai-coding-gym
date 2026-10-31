import pytest
from solution import Splitter


def apply(balances, transfers):
    b = dict(balances)
    for frm, to, amt in transfers:
        assert amt > 0
        b[frm] += amt
        b[to] -= amt
    return b


def test_payment_reduces_debt():
    s = Splitter()
    s.add_expense("ann", 1000, ["bob"])
    s.add_payment("bob", "ann", 400)
    assert s.balances() == {"ann": 600, "bob": -600}


def test_settle_greedy():
    s = Splitter()
    s.add_expense("ann", 3000, ["ann", "bob", "cat"])
    s.add_expense("bob", 600, ["cat", "dan"])
    assert s.balances() == {"ann": 2000, "bob": -400, "cat": -1300, "dan": -300}
    assert s.settle() == [("cat", "ann", 1300), ("bob", "ann", 400), ("dan", "ann", 300)]


def test_settle_ties_alphabetical():
    s = Splitter()
    s.add_expense("ann", 200, ["cat", "bob"])
    s.add_expense("dan", 200, ["cat", "bob"])
    assert s.balances() == {"ann": 200, "cat": -200, "bob": -200, "dan": 200}
    assert s.settle() == [("bob", "ann", 200), ("cat", "dan", 200)]


def test_settle_zeroes_everything_and_keeps_state():
    s = Splitter()
    s.add_expense("a", 999, ["a", "b", "c", "d"])
    s.add_expense("c", 500, ["a", "d"])
    s.add_payment("d", "a", 100)
    before = s.balances()
    transfers = s.settle()
    assert all(v == 0 for v in apply(before, transfers).values())
    assert len(transfers) <= len(before) - 1
    assert s.balances() == before


def test_settle_nothing_owed():
    s = Splitter()
    s.add_expense("a", 100, ["a"])
    assert s.settle() == []


def test_invalid_payment():
    with pytest.raises(ValueError):
        Splitter().add_payment("a", "a", 10)
    with pytest.raises(ValueError):
        Splitter().add_payment("a", "b", 0)
