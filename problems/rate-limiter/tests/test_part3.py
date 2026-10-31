import math

import pytest
from clock import FakeClock
from solution import RateLimiter


def test_cost_counts_against_limit():
    rl = RateLimiter(5, 10, clock=FakeClock())
    assert rl.allow("a", cost=3)
    assert not rl.allow("a", cost=3)
    assert rl.allow("a", cost=2)
    assert not rl.allow("a")


def test_denied_costly_request_not_recorded():
    rl = RateLimiter(5, 10, clock=FakeClock())
    rl.allow("a", cost=4)
    assert not rl.allow("a", cost=2)
    assert rl.allow("a", cost=1)


def test_cost_above_limit_never_allowed():
    rl = RateLimiter(5, 10, clock=FakeClock())
    assert not rl.allow("a", cost=6)
    assert rl.retry_after("a", cost=6) == math.inf


def test_retry_after_with_cost_waits_for_enough_capacity():
    clk = FakeClock()
    rl = RateLimiter(5, 10, clock=clk)
    rl.allow("a", cost=2)         # t=0
    clk.advance(2)
    rl.allow("a", cost=2)         # t=2
    clk.advance(2)
    rl.allow("a", cost=1)         # t=4, used=5
    clk.advance(1)                # t=5
    assert rl.retry_after("a", cost=1) == pytest.approx(5)   # t=0 entry expires at 10
    assert rl.retry_after("a", cost=3) == pytest.approx(7)   # need t=0 and t=2 gone -> 12
    clk.advance(7)
    assert rl.allow("a", cost=3)


def test_override_applies_to_cost():
    rl = RateLimiter(2, 10, clock=FakeClock())
    rl.set_limit("vip", 10)
    assert rl.allow("vip", cost=8)
    assert rl.retry_after("vip", cost=11) == math.inf


@pytest.mark.parametrize("cost", [0, -1])
def test_invalid_cost(cost):
    with pytest.raises(ValueError):
        RateLimiter(5, 10).allow("a", cost=cost)
