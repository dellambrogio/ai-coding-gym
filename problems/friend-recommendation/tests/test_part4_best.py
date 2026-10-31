from __future__ import annotations

import unittest

from recommenders import pick_best_suggestion
from social_graph import Network


def sample_network() -> Network:
    g = Network()

    edges = [
        ("alice", "bob"),
        ("alice", "carol"),
        ("bob", "dave"),
        ("bob", "erin"),
        ("carol", "dave"),
        ("dave", "frank"),
    ]

    for a, b in edges:
        g.add_friendship(a, b)

    return g


class TestPart4BestSuggestion(unittest.TestCase):
    def test_picks_highest_mutual_score(self):
        g = sample_network()
        self.assertEqual(pick_best_suggestion(g, "alice"), "dave")

    def test_uses_lexicographic_tiebreak(self):
        g = Network()
        edges = [
            ("anna", "bob"),
            ("anna", "carl"),
            ("bob", "mona"),
            ("carl", "luca"),
        ]
        for a, b in edges:
            g.add_friendship(a, b)

        self.assertEqual(pick_best_suggestion(g, "anna"), "luca")

    def test_returns_none_if_no_valid_recommendation(self):
        g = Network()
        g.add_friendship("mike", "nina")
        g.add_friendship("mike", "oliver")
        g.add_friendship("nina", "oliver")
        self.assertIsNone(pick_best_suggestion(g, "mike"))


if __name__ == "__main__":
    unittest.main()
