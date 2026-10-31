from clock import FakeClock
from solution import LRUCache


def test_len_counts_live_entries():
    clk = FakeClock()
    c = LRUCache(5, clock=clk)
    c.put("a", 1, ttl=5)
    c.put("b", 2)
    assert len(c) == 2
    clk.advance(5)
    assert len(c) == 1


def test_delete_live_entry():
    c = LRUCache(2)
    c.put("a", 1)
    assert c.delete("a") is True
    assert c.get("a") is None
    assert len(c) == 0


def test_delete_missing_entry():
    assert LRUCache(2).delete("nope") is False


def test_delete_expired_entry_returns_false():
    clk = FakeClock()
    c = LRUCache(2, clock=clk)
    c.put("a", 1, ttl=1)
    clk.advance(2)
    assert c.delete("a") is False


def test_expired_entries_purged_before_lru_eviction():
    clk = FakeClock()
    c = LRUCache(3, clock=clk)
    c.put("old", 1)          # least recently used, no ttl
    c.put("tmp1", 2, ttl=5)
    c.put("tmp2", 3, ttl=5)
    clk.advance(5)
    c.put("new", 4)
    assert c.get("old") == 1, "expired entries should be evicted before the LRU live entry"
    assert c.get("new") == 4
    assert len(c) == 2


def test_lru_eviction_when_nothing_expired():
    clk = FakeClock()
    c = LRUCache(2, clock=clk)
    c.put("a", 1, ttl=100)
    c.put("b", 2)
    c.put("c", 3)
    assert c.get("a") is None
    assert len(c) == 2


def test_update_at_capacity_does_not_evict():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("b", 3)
    assert c.get("a") == 1 and c.get("b") == 3
