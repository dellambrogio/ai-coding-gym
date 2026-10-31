from __future__ import annotations

import unittest

from recommenders import is_valid_suggestion
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


class TestPart1FixBug(unittest.TestCase):
    def test_rejects_self_recommendation(self):
        g = sample_network()
        self.assertFalse(is_valid_suggestion(g, "alice", ["alice"]))

    def test_rejects_existing_friend(self):
        g = sample_network()
        self.assertFalse(is_valid_suggestion(g, "alice", ["bob"]))

    def test_rejects_duplicates(self):
        g = sample_network()
        self.assertFalse(is_valid_suggestion(g, "alice", ["dave", "dave"]))

    def test_accepts_clean_candidate_list(self):
        g = sample_network()
        self.assertTrue(is_valid_suggestion(
            g, "alice", ["dave", "erin", "frank"]))


if __name__ == "__main__":
    unittest.main()
