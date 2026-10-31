import time

from solution import KVStore


def test_set_get():
    s = KVStore()
    s.set("a", "1")
    assert s.get("a") == "1"
    assert s.get("missing") is None


def test_overwrite():
    s = KVStore()
    s.set("a", "1")
    s.set("a", "2")
    assert s.get("a") == "2"


def test_delete():
    s = KVStore()
    s.set("a", "1")
    assert s.delete("a") is True
    assert s.get("a") is None
    assert s.delete("a") is False


def test_count():
    s = KVStore()
    s.set("a", "x")
    s.set("b", "x")
    s.set("c", "y")
    assert s.count("x") == 2
    s.set("a", "y")
    assert s.count("x") == 1 and s.count("y") == 2
    s.delete("b")
    assert s.count("x") == 0
    assert s.count("never") == 0


def test_set_same_value_twice_counts_once():
    s = KVStore()
    s.set("a", "x")
    s.set("a", "x")
    assert s.count("x") == 1


def test_count_is_fast():
    s = KVStore()
    for i in range(50_000):
        s.set(f"k{i}", str(i % 10))
    start = time.perf_counter()
    for _ in range(50_000):
        s.count("3")
    assert time.perf_counter() - start < 1
