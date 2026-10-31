import pytest
from solution import TaskGraph


def valid(g_deps, order):
    pos = {t: i for i, t in enumerate(order)}
    return sorted(order) == sorted(g_deps) and all(pos[d] < pos[t] for t, ds in g_deps.items() for d in ds)


def test_chain():
    g = TaskGraph()
    g.add_task("deploy", ["test"])
    g.add_task("test", ["build"])
    g.add_task("build")
    assert g.order() == ["build", "test", "deploy"]


def test_alphabetical_tie_break():
    g = TaskGraph()
    for t in ["c", "a", "b"]:
        g.add_task(t)
    assert g.order() == ["a", "b", "c"]


def test_diamond():
    g = TaskGraph()
    g.add_task("d", ["b", "c"])
    g.add_task("c", ["a"])
    g.add_task("b", ["a"])
    g.add_task("a")
    assert g.order() == ["a", "b", "c", "d"]


def test_tie_break_applies_as_tasks_become_ready():
    g = TaskGraph()
    g.add_task("z")
    g.add_task("b", ["z"])
    g.add_task("y")
    assert g.order() == ["y", "z", "b"]


def test_duplicate_dependency_listed_twice():
    g = TaskGraph()
    g.add_task("a")
    g.add_task("b", ["a", "a"])
    assert g.order() == ["a", "b"]


def test_missing_dependency():
    g = TaskGraph()
    g.add_task("a", ["ghost"])
    with pytest.raises(KeyError):
        g.order()


def test_duplicate_task():
    g = TaskGraph()
    g.add_task("a")
    with pytest.raises(ValueError):
        g.add_task("a")


def test_empty():
    assert TaskGraph().order() == []
