from solution import Sheet


def test_sum_range():
    s = Sheet()
    for i, v in enumerate([1, 2, 3], start=1):
        s.set(f"A{i}", v)
    s.set("B1", "=SUM(A1:A3)")
    assert s.get("B1") == 6


def test_rectangle_any_corner_order():
    s = Sheet()
    for c in ["A1", "A2", "B1", "B2"]:
        s.set(c, 1)
    s.set("C1", "=SUM(B2:A1)")
    assert s.get("C1") == 4


def test_min_max_mixed_args():
    s = Sheet()
    s.set("A1", 5)
    s.set("A2", -3)
    s.set("B1", "=MAX(A1:A2, 2) + MIN(A1, A2, 0)")
    assert s.get("B1") == 2


def test_example_from_statement():
    s = Sheet()
    s.set("A1", 1)
    s.set("A2", 2)
    s.set("B1", 3)
    s.set("B2", 4)
    s.set("C1", "=SUM(A1:A3, 10) * MAX(B1, B2)")
    assert s.get("C1") == 52


def test_dependents_direct_and_indirect():
    s = Sheet()
    s.set("A1", 1)
    s.set("B1", "=A1*2")
    s.set("C1", "=B1+1")
    s.set("D1", "=SUM(A1:A3)")
    s.set("E1", 5)
    assert s.dependents("A1") == ["B1", "C1", "D1"]
    assert s.dependents("A2") == ["D1"]
    assert s.dependents("E1") == []


def test_dependents_sorted_numerically():
    s = Sheet()
    s.set("A10", "=Z1")
    s.set("A2", "=Z1")
    s.set("B1", "=Z1")
    assert s.dependents("Z1") == ["A2", "A10", "B1"]
