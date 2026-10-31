import pytest
from solution import Autocomplete


def make(words):
    ac = Autocomplete()
    for w, s in words.items():
        ac.add(w, s)
    return ac


def test_score_order():
    ac = make({"car": 5, "cart": 10, "care": 1, "dog": 50})
    assert ac.suggest("car") == ["cart", "car", "care"]


def test_alphabetical_tie_break_and_k():
    ac = make({"bb": 1, "ba": 1, "bc": 1, "bd": 2})
    assert ac.suggest("b", k=3) == ["bd", "ba", "bb"]


def test_scores_accumulate():
    ac = make({"go": 1, "gone": 3})
    ac.add("go", 5)
    assert ac.suggest("go") == ["go", "gone"]


def test_case_insensitive():
    ac = Autocomplete()
    ac.add("Python", 2)
    ac.add("PYTHON")
    assert ac.suggest("pyT") == ["python"]


def test_no_match_and_empty_prefix():
    ac = make({"a": 1, "b": 2})
    assert ac.suggest("z") == []
    assert ac.suggest("") == ["b", "a"]


@pytest.mark.parametrize("w", [0, -1])
def test_invalid_weight(w):
    with pytest.raises(ValueError):
        Autocomplete().add("x", w)
