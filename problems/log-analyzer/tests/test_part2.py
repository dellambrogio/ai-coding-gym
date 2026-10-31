from solution import LogAnalyzer


def make(lines):
    a = LogAnalyzer()
    for l in lines:
        a.add(l)
    return a


def line(path, latency=10, status=200, ts="2026-10-29T12:00:00Z"):
    return f"{ts} GET {path} {status} {latency}ms"


def test_top_paths_ignores_query_string():
    a = make([line("/a?x=1"), line("/a?x=2"), line("/b")])
    assert a.top_paths(1) == [("/a", 2)]


def test_top_paths_tie_break_alphabetical():
    a = make([line("/b"), line("/a"), line("/c"), line("/c")])
    assert a.top_paths(3) == [("/c", 2), ("/a", 1), ("/b", 1)]


def test_top_paths_n_larger_than_distinct():
    a = make([line("/a")])
    assert a.top_paths(10) == [("/a", 1)]


def test_p95_nearest_rank():
    a = make([line("/api/x", latency=i) for i in range(1, 21)])  # 1..20
    assert a.p95_latency() == 19


def test_p95_single_value():
    assert make([line("/a", latency=42)]).p95_latency() == 42


def test_p95_unsorted_input():
    a = make([line("/a", latency=l) for l in [50, 10, 40, 20, 30]])
    assert a.p95_latency() == 50


def test_p95_path_prefix():
    a = make([line("/api/users", latency=100), line("/api/orders", latency=5), line("/health", latency=999)])
    assert a.p95_latency("/api") == 100
    assert a.p95_latency("/api/orders") == 5


def test_p95_no_match():
    assert make([line("/a")]).p95_latency("/zzz") is None
    assert LogAnalyzer().p95_latency() is None
