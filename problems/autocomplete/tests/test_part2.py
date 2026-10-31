import random
import string
import time

from solution import Autocomplete


def test_remove():
    ac = Autocomplete()
    ac.add("car", 5)
    ac.add("cart", 1)
    assert ac.remove("CAR") is True
    assert ac.suggest("car") == ["cart"]
    assert ac.remove("car") is False


def test_readd_after_remove_starts_fresh():
    ac = Autocomplete()
    ac.add("x", 100)
    ac.remove("x")
    ac.add("x")
    ac.add("xy", 2)
    assert ac.suggest("x") == ["xy", "x"]


def test_large_vocabulary_is_fast():
    rnd = random.Random(4)
    ac = Autocomplete()
    for _ in range(50_000):
        ac.add("".join(rnd.choices(string.ascii_lowercase, k=rnd.randint(4, 10))), rnd.randint(1, 100))
    prefixes = ["".join(rnd.choices(string.ascii_lowercase, k=rnd.randint(2, 3))) for _ in range(5_000)]
    start = time.perf_counter()
    for p in prefixes:
        ac.suggest(p, 5)
    assert time.perf_counter() - start < 2
