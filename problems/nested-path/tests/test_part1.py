import pytest
from solution import get

DATA = {
    "users": [
        {"name": "ann", "address": {"city": "Rome"}, "tags": ["a", "b"]},
        {"name": "bob", "address": None},
    ],
    "count": 2,
    "_meta": {"v1": True},
}


def test_simple_key():
    assert get(DATA, "count") == 2


def test_nested_path():
    assert get(DATA, "users[0].address.city") == "Rome"
    assert get(DATA, "users[0].tags[1]") == "b"
    assert get(DATA, "_meta.v1") is True


def test_negative_index():
    assert get(DATA, "users[-1].name") == "bob"


def test_root_index_and_empty_path():
    assert get([[1, 2], [3]], "[1][0]") == 3
    assert get(DATA, "") is DATA


@pytest.mark.parametrize("path", [
    "missing", "users[5].name", "users[-3]", "users[1].address.city", "count.x", "users.name", "_meta[0]",
])
def test_missing_returns_default(path):
    assert get(DATA, path) is None
    assert get(DATA, path, default="dflt") == "dflt"


def test_falsy_values_are_not_missing():
    assert get({"a": 0, "b": None}, "a", default=7) == 0
    assert get({"b": None}, "b", default=7) is None


@pytest.mark.parametrize("path", ["a..b", "a[", ".a", "a[x]", "a b", "a.", "[1]x", "1a"])
def test_invalid_syntax(path):
    with pytest.raises(ValueError):
        get({"a": {"b": 1}}, path)
