import random
import time

import pytest
from solution import Metrics


def make():
    m = Metrics()
    for ts, v in [(10, 1.0), (20, 5.0), (15, 3.0), (30, 2.0), (20, 1.0)]:
        m.record("cpu", ts, v)
    m.record("mem", 10, 100.0)
    return m


def test_aggregates():
    m = make()
    assert m.query("cpu", 0, 100, "sum") == 12.0
    assert m.query("cpu", 0, 100, "count") == 5
    assert m.query("cpu", 0, 100, "avg") == 2.4
    assert m.query("cpu", 0, 100, "min") == 1.0
    assert m.query("cpu", 0, 100, "max") == 5.0


def test_half_open_range():
    m = make()
    assert m.query("cpu", 15, 30, "count") == 3
    assert m.query("cpu", 20, 21, "sum") == 6.0


def test_empty_results():
    m = make()
    assert m.query("cpu", 31, 40, "sum") == 0
    assert m.query("cpu", 31, 40, "count") == 0
    assert m.query("cpu", 31, 40, "avg") is None
    assert m.query("disk", 0, 100, "max") is None


def test_metrics_are_separate():
    assert make().query("mem", 0, 100, "sum") == 100.0


def test_unknown_agg():
    with pytest.raises(ValueError):
        make().query("cpu", 0, 10, "median")


def test_queries_are_fast():
    m = Metrics()
    for ts in range(100_000):
        m.record("x", ts, 1.0)
    rnd = random.Random(5)
    start = time.perf_counter()
    for _ in range(3000):
        a = rnd.randint(0, 99_000)
        assert m.query("x", a, a + 500, "count") == 500
    assert time.perf_counter() - start < 2
