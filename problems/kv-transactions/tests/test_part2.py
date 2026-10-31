import pytest
from solution import KVStore


def test_rollback_discards():
    s = KVStore()
    s.set("a", "1")
    s.begin()
    s.set("a", "2")
    s.set("b", "3")
    assert s.get("a") == "2"
    s.rollback()
    assert s.get("a") == "1" and s.get("b") is None


def test_commit_keeps():
    s = KVStore()
    s.begin()
    s.set("a", "1")
    s.commit()
    assert s.get("a") == "1"


def test_rollback_restores_deleted_key():
    s = KVStore()
    s.set("a", "1")
    s.begin()
    s.delete("a")
    assert s.get("a") is None
    s.rollback()
    assert s.get("a") == "1"


def test_nested_rollback_only_inner():
    s = KVStore()
    s.begin()
    s.set("a", "1")
    s.begin()
    s.set("a", "2")
    s.rollback()
    assert s.get("a") == "1"
    s.rollback()
    assert s.get("a") is None


def test_inner_commit_then_outer_rollback():
    s = KVStore()
    s.set("a", "0")
    s.begin()
    s.begin()
    s.set("a", "2")
    s.commit()
    assert s.get("a") == "2"
    s.rollback()
    assert s.get("a") == "0"


def test_count_inside_transactions():
    s = KVStore()
    s.set("a", "x")
    s.begin()
    s.set("b", "x")
    s.set("a", "y")
    assert s.count("x") == 1 and s.count("y") == 1
    s.rollback()
    assert s.count("x") == 1 and s.count("y") == 0


def test_multiple_writes_same_key_in_transaction():
    s = KVStore()
    s.set("a", "orig")
    s.begin()
    s.set("a", "1")
    s.set("a", "2")
    s.delete("a")
    s.set("a", "3")
    s.rollback()
    assert s.get("a") == "orig"
    assert s.count("orig") == 1 and s.count("3") == 0


def test_errors_without_transaction():
    s = KVStore()
    with pytest.raises(RuntimeError):
        s.commit()
    with pytest.raises(RuntimeError):
        s.rollback()
    s.begin()
    s.commit()
    with pytest.raises(RuntimeError):
        s.commit()
