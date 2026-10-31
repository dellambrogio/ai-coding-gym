import pytest
from solution import Leaderboard


def test_add_and_score():
    lb = Leaderboard()
    lb.add_score("ann", 10)
    lb.add_score("ann", 5)
    assert lb.score("ann") == 15
    assert lb.score("nobody") == 0


def test_top_order_and_ties():
    lb = Leaderboard()
    for p, s in [("cat", 50), ("bob", 70), ("ann", 50), ("dan", 10)]:
        lb.add_score(p, s)
    assert lb.top(3) == [("bob", 70), ("ann", 50), ("cat", 50)]


def test_top_updates_after_more_points():
    lb = Leaderboard()
    lb.add_score("a", 10)
    lb.add_score("b", 20)
    lb.add_score("a", 15)
    assert lb.top(1) == [("a", 25)]


def test_top_k_larger_than_players():
    lb = Leaderboard()
    lb.add_score("a", 1)
    assert lb.top(5) == [("a", 1)]
    assert Leaderboard().top(3) == []


@pytest.mark.parametrize("pts", [0, -3])
def test_invalid_points(pts):
    with pytest.raises(ValueError):
        Leaderboard().add_score("a", pts)
