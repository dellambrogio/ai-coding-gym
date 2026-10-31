import pytest
from clock import FakeClock
from solution import LRUCache


def test_entry_available_before_expiry():
    clk = FakeClock()
    c = LRUCache(2, clock=clk)
    c.put("a", 1, ttl=10)
    clk.advance(9.9)
    assert c.get("a") == 1


def test_entry_expires_exactly_at_ttl():
    clk = FakeClock()
    c = LRUCache(2, clock=clk)
    c.put("a", 1, ttl=10)
    clk.advance(10)
    assert c.get("a") is None


def test_no_ttl_never_expires():
    clk = FakeClock()
    c = LRUCache(2, clock=clk)
    c.put("a", 1)
    clk.advance(1e9)
    assert c.get("a") == 1


def test_update_resets_ttl():
    clk = FakeClock()
    c = LRUCache(2, clock=clk)
    c.put("a", 1, ttl=10)
    clk.advance(8)
    c.put("a", 2, ttl=10)
    clk.advance(8)
    assert c.get("a") == 2


def test_update_without_ttl_removes_expiry():
    clk = FakeClock()
    c = LRUCache(2, clock=clk)
    c.put("a", 1, ttl=5)
    c.put("a", 2)
    clk.advance(100)
    assert c.get("a") == 2


def test_get_does_not_extend_ttl():
    clk = FakeClock()
    c = LRUCache(2, clock=clk)
    c.put("a", 1, ttl=10)
    clk.advance(6)
    c.get("a")
    clk.advance(6)
    assert c.get("a") is None


@pytest.mark.parametrize("ttl", [0, -1])
def test_invalid_ttl(ttl):
    with pytest.raises(ValueError):
        LRUCache(2).put("a", 1, ttl=ttl)
