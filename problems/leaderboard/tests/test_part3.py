import random
import time

from solution import Leaderboard


def test_count_in_range():
    lb = Leaderboard()
    for p, s in [("a", 10), ("b", 20), ("c", 20), ("d", 30)]:
        lb.add_score(p, s)
    assert lb.count_in_range(20, 30) == 3
    assert lb.count_in_range(11, 19) == 0
    assert lb.count_in_range(0, 100) == 4
    assert lb.count_in_range(10, 10) == 1


def test_large_leaderboard_is_fast():
    rnd = random.Random(1)
    lb = Leaderboard()
    players = [f"p{i}" for i in range(20_000)]
    start = time.perf_counter()
    for i in range(100_000):
        lb.add_score(rnd.choice(players), rnd.randint(1, 100))
        if i % 50 == 0:
            lb.top(10)
            lb.rank(rnd.choice(players))
            lb.count_in_range(100, 300)
    assert time.perf_counter() - start < 4


def test_results_still_correct_at_scale():
    rnd = random.Random(2)
    lb = Leaderboard()
    expected = {}
    for _ in range(5000):
        p, s = f"p{rnd.randint(0, 999)}", rnd.randint(1, 50)
        lb.add_score(p, s)
        expected[p] = expected.get(p, 0) + s
    best = sorted(expected.items(), key=lambda kv: (-kv[1], kv[0]))[:5]
    assert lb.top(5) == best
    p = "p7"
    if p in expected:
        assert lb.rank(p) == 1 + sum(v > expected[p] for v in expected.values())
