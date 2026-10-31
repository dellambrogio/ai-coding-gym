import pytest
from solution import group_by

RECS = [
    {"dept": "eng", "salary": 100, "bonus": 10},
    {"dept": "ops", "salary": 80, "bonus": None},
    {"dept": "eng", "salary": 120, "bonus": None},
    {"dept": None, "salary": 999, "bonus": 1},
    {"dept": "ops", "salary": None, "bonus": None},
]


def test_group_sum_count_avg():
    out = group_by(RECS, "dept", {"salary": "sum", "bonus": "count"})
    assert out == [
        {"dept": "eng", "salary_sum": 220, "bonus_count": 1},
        {"dept": "ops", "salary_sum": 80, "bonus_count": 0},
    ]


def test_avg_min_max_with_missing_values():
    out = group_by(RECS, "dept", {"bonus": "avg"})
    assert out == [{"dept": "eng", "bonus_avg": 10}, {"dept": "ops", "bonus_avg": None}]
    out = group_by(RECS, "dept", {"salary": "max"})
    assert out == [{"dept": "eng", "salary_max": 120}, {"dept": "ops", "salary_max": 80}]


def test_several_columns():
    out = group_by(RECS, "dept", {"salary": "min", "bonus": "sum"})
    assert out[0] == {"dept": "eng", "salary_min": 100, "bonus_sum": 10}
    assert out[1] == {"dept": "ops", "salary_min": 80, "bonus_sum": 0}


def test_sorted_numeric_keys():
    recs = [{"k": 10, "v": 1}, {"k": 2, "v": 2}, {"k": 10, "v": 3}]
    assert group_by(recs, "k", {"v": "sum"}) == [{"k": 2, "v_sum": 2}, {"k": 10, "v_sum": 4}]


def test_empty_records():
    assert group_by([], "k", {"v": "sum"}) == []


def test_unknown_op():
    with pytest.raises(ValueError):
        group_by(RECS, "dept", {"salary": "median"})
