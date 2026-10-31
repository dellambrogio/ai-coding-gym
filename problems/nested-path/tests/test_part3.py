import pytest
from solution import get, get_all, set_path

DATA = {
    "users": [{"name": "ann", "langs": ["py", "go"]}, {"name": "bob", "langs": []}, {"nick": "c"}],
    "services": {"api": {"port": 80}, "db": {"port": 5432}, "cache": {}},
}


def test_list_wildcard():
    assert get_all(DATA, "users[*].name") == ["ann", "bob"]


def test_dict_wildcard():
    assert get_all(DATA, "services.*.port") == [80, 5432]


def test_nested_wildcards():
    assert get_all(DATA, "users[*].langs[*]") == ["py", "go"]


def test_leading_wildcard():
    assert get_all({"a": 1, "b": 2}, "*") == [1, 2]
    assert get_all([10, 20], "[*]") == [10, 20]


def test_wrong_type_skipped():
    assert get_all(DATA, "services[*]") == []
    assert get_all(DATA, "users.*") == []


def test_without_wildcards():
    assert get_all(DATA, "users[0].name") == ["ann"]
    assert get_all(DATA, "nope") == []


def test_get_and_set_reject_wildcards():
    with pytest.raises(ValueError):
        get(DATA, "users[*].name")
    with pytest.raises(ValueError):
        set_path({}, "a.*", 1)
