import pytest
from clock import FakeClock
from solution import RateLimiter


def test_allows_up_to_limit():
    rl = RateLimiter(3, 10, clock=FakeClock())
    assert [rl.allow("a") for _ in range(4)] == [True, True, True, False]


def test_clients_are_independent():
    rl = RateLimiter(1, 10, clock=FakeClock())
    assert rl.allow("a") and rl.allow("b")
    assert not rl.allow("a")


def test_window_slides():
    clk = FakeClock()
    rl = RateLimiter(2, 10, clock=clk)
    assert rl.allow("a")          # t=0
    clk.advance(5)
    assert rl.allow("a")          # t=5
    assert not rl.allow("a")
    clk.advance(5)                # t=10: request at t=0 left the window
    assert rl.allow("a")
    assert not rl.allow("a")


def test_window_boundary_is_exclusive_of_old_edge():
    clk = FakeClock()
    rl = RateLimiter(1, 10, clock=clk)
    rl.allow("a")
    clk.advance(9.999)
    assert not rl.allow("a")
    clk.advance(0.001)
    assert rl.allow("a")


def test_denied_requests_do_not_count():
    clk = FakeClock()
    rl = RateLimiter(1, 10, clock=clk)
    rl.allow("a")                 # t=0 allowed
    clk.advance(5)
    assert not rl.allow("a")      # t=5 denied, not recorded
    clk.advance(5)
    assert rl.allow("a")          # t=10 allowed


def test_no_fixed_window_burst():
    clk = FakeClock(9)
    rl = RateLimiter(2, 10, clock=clk)
    assert rl.allow("a") and rl.allow("a")  # t=9
    clk.advance(2)                           # t=11, a fixed window would reset at 10
    assert not rl.allow("a")


@pytest.mark.parametrize("limit,window", [(0, 10), (1, 0), (1, -5)])
def test_invalid_args(limit, window):
    with pytest.raises(ValueError):
        RateLimiter(limit, window)


def test_many_requests_are_fast():
    import time
    clk = FakeClock()
    rl = RateLimiter(100, 1, clock=clk)
    start = time.perf_counter()
    for i in range(200_000):
        clk.advance(0.001)
        rl.allow(i % 10)
    assert time.perf_counter() - start < 3
