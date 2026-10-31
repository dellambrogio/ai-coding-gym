import pytest
from solution import Splitter


def test_weighted_split():
    s = Splitter()
    s.add_expense("ann", 1000, ["ann", "bob"], shares=[3, 1])
    assert s.balances() == {"ann": 250, "bob": -250}


def test_leftover_to_largest_fraction():
    s = Splitter()
    # 100 * [1, 2, 4] / 7 = 14.28, 28.57, 57.14 -> floor 14, 28, 57 (99); bob has the largest fraction
    s.add_expense("zed", 100, ["ann", "bob", "cat"], shares=[1, 2, 4])
    assert s.balances() == {"zed": 100, "ann": -14, "bob": -29, "cat": -57}


def test_leftover_ties_alphabetical():
    s = Splitter()
    s.add_expense("zed", 10, ["cat", "ann", "bob"], shares=[1, 1, 1])
    assert s.balances() == {"zed": 10, "ann": -4, "bob": -3, "cat": -3}


def test_default_shares_match_part1():
    a, b = Splitter(), Splitter()
    a.add_expense("x", 101, ["p", "q", "r"])
    b.add_expense("x", 101, ["p", "q", "r"], shares=[1, 1, 1])
    assert a.balances() == b.balances()


@pytest.mark.parametrize("shares", [[1], [1, 0], [2, -1], [1, 1, 1]])
def test_invalid_shares(shares):
    with pytest.raises(ValueError):
        Splitter().add_expense("x", 100, ["a", "b"], shares=shares)
