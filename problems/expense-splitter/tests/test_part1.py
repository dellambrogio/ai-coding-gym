import pytest
from solution import Splitter


def test_even_split_including_payer():
    s = Splitter()
    s.add_expense("ann", 900, ["ann", "bob", "cat"])
    assert s.balances() == {"ann": 600, "bob": -300, "cat": -300}


def test_payer_not_participating():
    s = Splitter()
    s.add_expense("ann", 1000, ["bob", "cat"])
    assert s.balances() == {"ann": 1000, "bob": -500, "cat": -500}


def test_leftover_cents_alphabetical():
    s = Splitter()
    s.add_expense("zed", 100, ["cat", "ann", "bob"])
    assert s.balances() == {"zed": 100, "ann": -34, "bob": -33, "cat": -33}


def test_multiple_expenses_accumulate_and_sum_to_zero():
    s = Splitter()
    s.add_expense("ann", 1001, ["ann", "bob", "cat"])
    s.add_expense("bob", 250, ["ann", "bob"])
    b = s.balances()
    assert sum(b.values()) == 0
    assert b == {"ann": 667 - 125, "bob": -334 + 125, "cat": -333}


@pytest.mark.parametrize("amount,people", [(0, ["a"]), (-5, ["a"]), (10, []), (10, ["a", "a"])])
def test_invalid(amount, people):
    with pytest.raises(ValueError):
        Splitter().add_expense("x", amount, people)
