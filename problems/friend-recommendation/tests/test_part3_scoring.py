from __future__ import annotations

import unittest

from recommenders import recommendation_score
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


class TestPart3RecommendationScore(unittest.TestCase):
    def test_mutual_connection_count(self):
        g = sample_network()
        self.assertEqual(recommendation_score(g, "alice", "dave"), 2)

    def test_invalid_candidate_scores_zero(self):
        g = sample_network()
        self.assertEqual(recommendation_score(
            g, "alice", "bob"), 0)
        self.assertEqual(recommendation_score(g, "alice", "alice"), 0)

    def test_zero_when_no_mutual_connection(self):
        g = sample_network()
        self.assertEqual(recommendation_score(g, "erin", "frank"), 0)


if __name__ == "__main__":
    unittest.main()
