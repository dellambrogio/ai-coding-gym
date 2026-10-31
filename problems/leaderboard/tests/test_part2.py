from solution import Leaderboard


def test_competition_rank():
    lb = Leaderboard()
    for p, s in [("a", 100), ("b", 90), ("c", 90), ("d", 80)]:
        lb.add_score(p, s)
    assert [lb.rank(p) for p in "abcd"] == [1, 2, 2, 4]


def test_rank_unknown():
    assert Leaderboard().rank("x") is None


def test_reset():
    lb = Leaderboard()
    lb.add_score("a", 100)
    lb.add_score("b", 50)
    assert lb.reset("a") is True
    assert lb.rank("b") == 1
    assert lb.score("a") == 0 and lb.rank("a") is None
    assert lb.top(5) == [("b", 50)]
    assert lb.reset("a") is False


def test_reset_then_add_again():
    lb = Leaderboard()
    lb.add_score("a", 100)
    lb.reset("a")
    lb.add_score("a", 1)
    assert lb.score("a") == 1
