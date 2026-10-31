from solution import LogAnalyzer


def line(ts, status):
    return f"{ts} GET /x {status} 5ms"


def test_errors_grouped_by_minute():
    a = LogAnalyzer()
    for ts, st in [("2026-10-29T12:00:01Z", 500), ("2026-10-29T12:00:59Z", 503),
                   ("2026-10-29T12:01:00Z", 502), ("2026-10-29T12:01:30Z", 200)]:
        a.add(line(ts, st))
    assert a.errors_per_minute("2026-10-29T12:00:00Z", "2026-10-29T13:00:00Z") == {
        "2026-10-29T12:00": 2, "2026-10-29T12:01": 1}


def test_4xx_not_counted():
    a = LogAnalyzer()
    a.add(line("2026-10-29T12:00:01Z", 404))
    a.add(line("2026-10-29T12:00:01Z", 499))
    assert a.errors_per_minute("2026-10-29T00:00:00Z", "2026-10-30T00:00:00Z") == {}


def test_range_is_half_open():
    a = LogAnalyzer()
    a.add(line("2026-10-29T12:00:00Z", 500))
    a.add(line("2026-10-29T12:05:00Z", 500))
    assert a.errors_per_minute("2026-10-29T12:00:00Z", "2026-10-29T12:05:00Z") == {"2026-10-29T12:00": 1}


def test_out_of_order_and_across_days():
    a = LogAnalyzer()
    a.add(line("2026-10-30T00:00:10Z", 500))
    a.add(line("2026-10-29T23:59:50Z", 500))
    a.add(line("2026-10-29T23:59:55Z", 501))
    assert a.errors_per_minute("2026-10-29T23:00:00Z", "2026-10-30T01:00:00Z") == {
        "2026-10-29T23:59": 2, "2026-10-30T00:00": 1}
