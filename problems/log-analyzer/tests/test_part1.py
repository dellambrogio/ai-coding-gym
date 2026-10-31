import pytest
from solution import LogAnalyzer

GOOD = "2026-10-29T12:00:01Z GET /api/users?id=7 200 123ms"


def test_valid_line():
    a = LogAnalyzer()
    assert a.add(GOOD) is True
    assert a.count_by_status() == {200: 1}
    assert a.malformed == 0


def test_surrounding_whitespace_ok():
    a = LogAnalyzer()
    assert a.add("  " + GOOD + "\n")


@pytest.mark.parametrize("line", [
    "",
    "garbage",
    "2026-10-29T12:00:01Z GET /api/users 200",                 # missing field
    "2026-10-29T12:00:01Z GET /api/users 200 123ms extra",     # extra field
    "yesterday GET /api/users 200 123ms",                      # bad timestamp
    "2026-10-29T12:00:01Z FETCH /api/users 200 123ms",         # bad method
    "2026-10-29T12:00:01Z GET api/users 200 123ms",            # path without /
    "2026-10-29T12:00:01Z GET /api/users 2xx 123ms",           # status not int
    "2026-10-29T12:00:01Z GET /api/users 600 123ms",           # status out of range
    "2026-10-29T12:00:01Z GET /api/users 200 123",             # latency without ms
    "2026-10-29T12:00:01Z GET /api/users 200 -5ms",            # negative latency
])
def test_malformed_lines(line):
    a = LogAnalyzer()
    assert a.add(line) is False
    assert a.malformed == 1
    assert a.count_by_status() == {}


def test_count_by_status_mixed():
    a = LogAnalyzer()
    for status in [200, 200, 404, 500, 200]:
        a.add(f"2026-10-29T12:00:01Z GET /x {status} 5ms")
    a.add("bad line")
    assert a.count_by_status() == {200: 3, 404: 1, 500: 1}
    assert a.malformed == 1
