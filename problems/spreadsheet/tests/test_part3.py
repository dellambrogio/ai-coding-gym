import pytest
from solution import Sheet


def test_self_reference():
    with pytest.raises(ValueError):
        Sheet().set("A1", "=A1+1")


def test_indirect_cycle_rejected_and_sheet_unchanged():
    s = Sheet()
    s.set("A1", "=B1+1")
    s.set("B1", "=C1+1")
    s.set("C1", 5)
    with pytest.raises(ValueError):
        s.set("C1", "=A1")
    assert s.get("C1") == 5
    assert s.get("A1") == 7


def test_cycle_through_range():
    s = Sheet()
    s.set("B1", "=SUM(A1:A5)")
    with pytest.raises(ValueError):
        s.set("A3", "=B1")


def test_replacing_formula_can_remove_cycle_risk():
    s = Sheet()
    s.set("A1", "=B1")
    s.set("A1", 3)
    s.set("B1", "=A1")
    assert s.get("B1") == 3


def test_clear():
    s = Sheet()
    s.set("A1", 4)
    s.set("B1", "=A1*2")
    s.clear("A1")
    assert s.get("A1") == 0 and s.get("B1") == 0
    s.clear("C3")
    s.clear("B1")
    s.set("A1", "=B1")
    assert s.dependents("B1") == ["A1"]
