import pytest
from solution import Sheet


def test_numbers_and_empty():
    s = Sheet()
    s.set("A1", 5)
    s.set("B2", 2.5)
    assert s.get("A1") == 5 and s.get("B2") == 2.5
    assert s.get("Z99") == 0


def test_formula_references():
    s = Sheet()
    s.set("A1", 2)
    s.set("A2", 3)
    s.set("A3", "=A1+A2*4")
    assert s.get("A3") == 14


def test_formula_sees_updates():
    s = Sheet()
    s.set("A1", 1)
    s.set("B1", "=A1*10")
    s.set("A1", 7)
    assert s.get("B1") == 70


def test_parentheses_unary_minus_division():
    s = Sheet()
    s.set("A1", 4)
    s.set("B1", "=-(A1 - 10) / 4")
    assert s.get("B1") == 1.5


def test_chained_formulas_and_empty_refs():
    s = Sheet()
    s.set("A1", "=B1+1")
    s.set("B1", "=C1+1")
    assert s.get("A1") == 2


def test_division_by_zero():
    s = Sheet()
    s.set("A1", "=1/B1")
    with pytest.raises(ZeroDivisionError):
        s.get("A1")


@pytest.mark.parametrize("cell", ["a1", "A0", "A100", "AA1", "A01", "1A", ""])
def test_invalid_cell(cell):
    with pytest.raises(ValueError):
        Sheet().set(cell, 1)


@pytest.mark.parametrize("value", ["=1+", "=A1 A2", "=(1", "=foo", "hello", None, [1]])
def test_invalid_values(value):
    with pytest.raises(ValueError):
        Sheet().set("A1", value)
