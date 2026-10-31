import time

from solution import KVStore


def test_keys_with_prefix():
    s = KVStore()
    for k in ["user:2", "user:1", "order:1", "user"]:
        s.set(k, "v")
    assert s.keys_with_prefix("user:") == ["user:1", "user:2"]
    assert s.keys_with_prefix("") == ["order:1", "user", "user:1", "user:2"]
    assert s.keys_with_prefix("zzz") == []


def test_keys_with_prefix_in_transaction():
    s = KVStore()
    s.set("a1", "v")
    s.begin()
    s.set("a2", "v")
    s.delete("a1")
    assert s.keys_with_prefix("a") == ["a2"]
    s.rollback()
    assert s.keys_with_prefix("a") == ["a1"]


def test_begin_does_not_copy_store():
    s = KVStore()
    for i in range(200_000):
        s.set(f"k{i}", "v")
    start = time.perf_counter()
    for _ in range(500):
        s.begin()
    for _ in range(500):
        s.rollback()
    assert time.perf_counter() - start < 0.5


def test_deep_nesting_is_fast():
    s = KVStore()
    start = time.perf_counter()
    for depth in range(100):
        s.begin()
        for i in range(1000):
            s.set(f"k{i}", str(depth))
    assert s.count("99") == 1000
    for _ in range(100):
        s.rollback()
    assert s.get("k0") is None and s.count("99") == 0
    assert time.perf_counter() - start < 1.5
