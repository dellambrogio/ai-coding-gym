import pytest
from clock import FakeClock
from solution import RateLimiter


def test_set_limit_override():
    rl = RateLimiter(1, 10, clock=FakeClock())
    rl.set_limit("vip", 3)
    assert [rl.allow("vip") for _ in range(4)] == [True, True, True, False]
    assert [rl.allow("a") for _ in range(2)] == [True, False]


def test_lowering_limit_counts_existing_requests():
    rl = RateLimiter(5, 10, clock=FakeClock())
    for _ in range(3):
        rl.allow("a")
    rl.set_limit("a", 2)
    assert not rl.allow("a")


def test_invalid_override():
    with pytest.raises(ValueError):
        RateLimiter(1, 10).set_limit("a", 0)


def test_retry_after_zero_when_allowed():
    rl = RateLimiter(2, 10, clock=FakeClock())
    rl.allow("a")
    assert rl.retry_after("a") == 0
    assert rl.retry_after("unknown") == 0


def test_retry_after_when_limited():
    clk = FakeClock()
    rl = RateLimiter(2, 10, clock=clk)
    rl.allow("a")                 # t=0
    clk.advance(3)
    rl.allow("a")                 # t=3
    clk.advance(1)                # t=4
    assert rl.retry_after("a") == pytest.approx(6)
    clk.advance(6)
    assert rl.allow("a")


def test_retry_after_does_not_record():
    rl = RateLimiter(1, 10, clock=FakeClock())
    for _ in range(5):
        rl.retry_after("a")
    assert rl.allow("a")
