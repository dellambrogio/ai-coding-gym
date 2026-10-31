import pytest
from solution import LRUCache


def test_get_missing_returns_none():
    assert LRUCache(2).get("x") is None


def test_put_then_get():
    c = LRUCache(2)
    c.put("a", 1)
    assert c.get("a") == 1


def test_update_existing_key():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("a", 2)
    assert c.get("a") == 2


def test_evicts_least_recently_used():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("c", 3)
    assert c.get("a") is None
    assert c.get("b") == 2 and c.get("c") == 3


def test_get_refreshes_recency():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.get("a")
    c.put("c", 3)
    assert c.get("b") is None
    assert c.get("a") == 1


def test_update_refreshes_recency_without_eviction():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)
    c.put("c", 3)
    assert c.get("b") is None
    assert c.get("a") == 10


def test_capacity_one():
    c = LRUCache(1)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") is None and c.get("b") == 2


def test_falsy_values_are_stored():
    c = LRUCache(3)
    c.put("zero", 0)
    c.put("empty", "")
    assert c.get("zero") == 0 and c.get("empty") == ""


def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)


def test_large_workload_is_fast():
    import time
    c = LRUCache(1000)
    start = time.perf_counter()
    for i in range(200_000):
        c.put(i, i)
        c.get(i - 500)
    assert time.perf_counter() - start < 3
