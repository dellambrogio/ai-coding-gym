import pytest
from solution import get, set_path


def test_set_existing():
    d = {"a": {"b": 1}}
    set_path(d, "a.b", 2)
    assert d == {"a": {"b": 2}}


def test_creates_dicts_and_lists():
    d = {}
    set_path(d, "a.b[0].c", 5)
    assert d == {"a": {"b": [{"c": 5}]}}


def test_append_at_len():
    d = {"xs": [1, 2]}
    set_path(d, "xs[2]", 3)
    assert d["xs"] == [1, 2, 3]


def test_index_too_large():
    with pytest.raises(IndexError):
        set_path({"xs": [1]}, "xs[3]", 0)


def test_negative_index_existing():
    d = {"xs": [1, 2, 3]}
    set_path(d, "xs[-1]", 9)
    assert d["xs"] == [1, 2, 9]
    with pytest.raises(IndexError):
        set_path(d, "xs[-4]", 0)


def test_type_errors():
    with pytest.raises(TypeError):
        set_path({"a": [1]}, "a.b", 1)
    with pytest.raises(TypeError):
        set_path({"a": {}}, "a[0]", 1)
    with pytest.raises(TypeError):
        set_path({"a": 5}, "a.b", 1)


def test_empty_path():
    with pytest.raises(ValueError):
        set_path({}, "", 1)


def test_roundtrip_with_get():
    d = {}
    set_path(d, "config.servers[0].port", 8080)
    set_path(d, "config.servers[1].port", 9090)
    assert get(d, "config.servers[1].port") == 9090
