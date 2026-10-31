import pytest
from clock import FakeClock
from solution import Shortener


def test_code_expires():
    clk = FakeClock()
    s = Shortener(clock=clk)
    code = s.shorten("https://a.com", ttl=10)
    clk.advance(9.9)
    assert s.resolve(code) == "https://a.com"
    clk.advance(0.1)
    assert s.resolve(code) is None
    assert s.clicks(code) == 0


def test_expired_alias_can_be_reused():
    clk = FakeClock()
    s = Shortener(clock=clk)
    s.shorten("https://a.com", alias="sale", ttl=5)
    clk.advance(5)
    assert s.shorten("https://b.com", alias="sale") == "sale"
    assert s.resolve("sale") == "https://b.com"


def test_new_automatic_code_after_expiry():
    clk = FakeClock()
    s = Shortener(clock=clk)
    old = s.shorten("https://a.com", ttl=5)
    clk.advance(5)
    new = s.shorten("https://a.com")
    assert s.resolve(new) == "https://a.com"
    clk.advance(1000)
    assert s.resolve(new) == "https://a.com"


def test_live_code_returned_unchanged():
    clk = FakeClock()
    s = Shortener(clock=clk)
    code = s.shorten("https://a.com", ttl=5)
    assert s.shorten("https://a.com", ttl=100) == code
    clk.advance(5)
    assert s.resolve(code) is None


def test_delete():
    clk = FakeClock()
    s = Shortener(clock=clk)
    code = s.shorten("https://a.com")
    assert s.delete(code) is True
    assert s.resolve(code) is None
    assert s.delete(code) is False
    short = s.shorten("https://b.com", ttl=1)
    clk.advance(1)
    assert s.delete(short) is False


@pytest.mark.parametrize("ttl", [0, -1])
def test_invalid_ttl(ttl):
    with pytest.raises(ValueError):
        Shortener().shorten("https://a.com", ttl=ttl)
