from solution import Autocomplete


def make(words):
    ac = Autocomplete()
    for w, s in words.items():
        ac.add(w, s)
    return ac


def test_substitution():
    ac = make({"python": 1})
    assert ac.suggest("pyx", typos=1) == ["python"]
    assert ac.suggest("pyx") == []


def test_insertion_and_deletion():
    ac = make({"python": 1})
    assert ac.suggest("pyhon", typos=1) == ["python"]
    assert ac.suggest("pyython", typos=1) == ["python"]


def test_two_edits_not_enough():
    ac = make({"python": 1})
    assert ac.suggest("pxxh", typos=1) == []


def test_exact_matches_first():
    ac = make({"cat": 1, "bat": 100, "car": 2})
    assert ac.suggest("ca", typos=1) == ["car", "cat", "bat"]


def test_k_limits_total():
    ac = make({"cat": 1, "bat": 100, "rat": 50})
    assert ac.suggest("ca", k=2, typos=1) == ["cat", "bat"]


def test_typos_zero_unchanged():
    ac = make({"cat": 1, "bat": 100})
    assert ac.suggest("ca", typos=0) == ["cat"]
