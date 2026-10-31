import pytest
from solution import read_records


def test_types():
    recs = read_records("i,f,b,s,n\n42,3.5,TRUE,hello,\n-7,.5,false,007x,")
    assert recs == [
        {"i": 42, "f": 3.5, "b": True, "s": "hello", "n": None},
        {"i": -7, "f": 0.5, "b": False, "s": "007x", "n": None},
    ]
    assert type(recs[0]["i"]) is int and type(recs[0]["f"]) is float


def test_things_that_stay_strings():
    recs = read_records("v\n1e5\n1.2.3\nyes\n-\n 1")
    assert [r["v"] for r in recs] == ["1e5", "1.2.3", "yes", "-", " 1"]


def test_quoted_values():
    assert read_records('name,city\n"Doe, Jane","New\nYork"') == [{"name": "Doe, Jane", "city": "New\nYork"}]


def test_duplicate_header():
    with pytest.raises(ValueError):
        read_records("a,a\n1,2")


def test_wrong_field_count():
    with pytest.raises(ValueError):
        read_records("a,b\n1,2\n3")


def test_empty_and_header_only():
    assert read_records("") == []
    assert read_records("a,b\n") == []
