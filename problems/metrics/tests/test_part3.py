from solution import Metrics


def test_old_points_dropped():
    m = Metrics(retention=10)
    assert m.record("x", 100, 1.0) is True
    assert m.record("x", 95, 1.0) is True
    assert m.record("x", 112, 1.0) is True
    assert m.query("x", 0, 1000, "count") == 1
    assert m.record("x", 101, 1.0) is False
    assert m.record("x", 102, 1.0) is True
    assert m.query("x", 0, 1000, "count") == 2


def test_boundary_kept():
    m = Metrics(retention=10)
    m.record("x", 0, 1.0)
    m.record("x", 10, 1.0)
    assert m.query("x", 0, 100, "count") == 2
    m.record("x", 11, 1.0)
    assert m.query("x", 0, 100, "count") == 2


def test_retention_per_metric():
    m = Metrics(retention=5)
    m.record("a", 100, 1.0)
    assert m.record("b", 1, 1.0) is True
    assert m.query("b", 0, 10, "count") == 1


def test_no_retention_keeps_everything():
    m = Metrics()
    assert m.record("x", 1_000_000, 1.0) is True
    assert m.record("x", 0, 1.0) is True
    assert m.query("x", 0, 2_000_000, "count") == 2
