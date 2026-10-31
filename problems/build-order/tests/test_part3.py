import pytest
from solution import TaskGraph


def test_durations_on_chain():
    g = TaskGraph()
    g.add_task("a", duration=3)
    g.add_task("b", ["a"], duration=2)
    assert g.earliest_start("b") == 3
    assert g.total_time() == 5


def test_parallel_branches_take_longest():
    g = TaskGraph()
    g.add_task("start", duration=1)
    g.add_task("fast", ["start"], duration=2)
    g.add_task("slow", ["start"], duration=10)
    g.add_task("end", ["fast", "slow"], duration=1)
    assert g.earliest_start("end") == 11
    assert g.total_time() == 12


def test_independent_tasks_run_in_parallel():
    g = TaskGraph()
    g.add_task("a", duration=4)
    g.add_task("b", duration=7)
    assert g.total_time() == 7


def test_default_duration_and_zero_duration():
    g = TaskGraph()
    g.add_task("a")
    g.add_task("milestone", ["a"], duration=0)
    g.add_task("b", ["milestone"])
    assert g.earliest_start("b") == 1
    assert g.total_time() == 2


def test_empty_total_time():
    assert TaskGraph().total_time() == 0


def test_negative_duration():
    with pytest.raises(ValueError):
        TaskGraph().add_task("a", duration=-1)


def test_cycle_raises():
    g = TaskGraph()
    g.add_task("a", ["b"])
    g.add_task("b", ["a"])
    with pytest.raises(ValueError):
        g.total_time()
