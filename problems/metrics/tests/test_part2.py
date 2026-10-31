import pytest
from solution import Metrics


def make():
    m = Metrics()
    for ts, v in [(0, 1.0), (5, 3.0), (12, 10.0), (35, 7.0), (39, 1.0)]:
        m.record("req", ts, v)
    return m


def test_downsample_skips_empty_buckets():
    assert make().downsample("req", 0, 40, 10, "sum") == [(0, 4.0), (10, 10.0), (30, 8.0)]


def test_downsample_avg_and_count():
    m = make()
    assert m.downsample("req", 0, 40, 10, "avg") == [(0, 2.0), (10, 10.0), (30, 4.0)]
    assert m.downsample("req", 0, 40, 20, "count") == [(0, 3), (20, 2)]


def test_last_bucket_cut_at_end():
    assert make().downsample("req", 0, 36, 20, "count") == [(0, 3), (20, 1)]


def test_offset_start():
    assert make().downsample("req", 5, 15, 5, "max") == [(5, 3.0), (10, 10.0)]


def test_invalid():
    with pytest.raises(ValueError):
        make().downsample("req", 0, 10, 0, "sum")
    with pytest.raises(ValueError):
        make().downsample("req", 0, 10, 5, "p99")
