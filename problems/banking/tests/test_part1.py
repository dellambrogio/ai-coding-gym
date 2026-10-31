import pytest
from solution import Bank


def test_create_account():
    b = Bank()
    assert b.create_account("a") is True
    assert b.create_account("a") is False
    assert b.get_balance("a") == 0


def test_deposit():
    b = Bank()
    b.create_account("a")
    assert b.deposit("a", 100) == 100
    assert b.deposit("a", 50) == 150
    assert b.deposit("missing", 10) is None


def test_transfer():
    b = Bank()
    b.create_account("a")
    b.create_account("b")
    b.deposit("a", 100)
    assert b.transfer("a", "b", 30) == 70
    assert b.get_balance("b") == 30


def test_transfer_insufficient_funds():
    b = Bank()
    b.create_account("a")
    b.create_account("b")
    b.deposit("a", 10)
    assert b.transfer("a", "b", 11) is None
    assert b.get_balance("a") == 10 and b.get_balance("b") == 0


def test_transfer_exact_balance():
    b = Bank()
    b.create_account("a")
    b.create_account("b")
    b.deposit("a", 10)
    assert b.transfer("a", "b", 10) == 0


def test_transfer_invalid_accounts():
    b = Bank()
    b.create_account("a")
    b.deposit("a", 10)
    assert b.transfer("a", "a", 5) is None
    assert b.transfer("a", "nope", 5) is None
    assert b.transfer("nope", "a", 5) is None
    assert b.get_balance("a") == 10


def test_get_balance_missing():
    assert Bank().get_balance("x") is None


@pytest.mark.parametrize("amount", [0, -5])
def test_invalid_amount(amount):
    b = Bank()
    b.create_account("a")
    b.create_account("b")
    with pytest.raises(ValueError):
        b.deposit("a", amount)
    with pytest.raises(ValueError):
        b.transfer("a", "b", amount)
