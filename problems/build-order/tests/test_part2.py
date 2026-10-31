import pytest
from solution import TaskGraph


def assert_cycle(g_deps, cyc):
    assert cyc is not None and len(cyc) >= 2 and cyc[0] == cyc[-1]
    for a, b in zip(cyc, cyc[1:]):
        assert b in g_deps[a], f"{b} is not a dependency of {a}"


def build(deps):
    g = TaskGraph()
    for t, ds in deps.items():
        g.add_task(t, ds)
    return g


def test_order_raises_on_cycle():
    with pytest.raises(ValueError):
        build({"a": ["b"], "b": ["a"]}).order()


def test_find_cycle_two_nodes():
    deps = {"a": ["b"], "b": ["a"]}
    assert_cycle(deps, build(deps).find_cycle())


def test_find_cycle_in_larger_graph():
    deps = {"root": ["x"], "x": ["y"], "y": ["z"], "z": ["x"], "other": []}
    cyc = build(deps).find_cycle()
    assert_cycle(deps, cyc)
    assert set(cyc) == {"x", "y", "z"}


def test_self_loop():
    deps = {"a": ["a"]}
    assert build(deps).find_cycle() == ["a", "a"]


def test_no_cycle():
    assert build({"a": [], "b": ["a"], "c": ["a", "b"]}).find_cycle() is None
