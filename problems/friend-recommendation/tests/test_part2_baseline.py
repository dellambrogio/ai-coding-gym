from __future__ import annotations

import random
import unittest

from recommenders import pick_random_suggestion
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


class TestPart2RandomSuggestion(unittest.TestCase):
    def test_returns_none_when_no_candidate_exists(self):
        g = Network()
        g.add_friendship("u1", "u2")
        g.add_friendship("u1", "u3")
        g.add_friendship("u2", "u3")
        self.assertIsNone(pick_random_suggestion(g, "u1", random.Random(0)))

    def test_returns_valid_candidate(self):
        g = sample_network()
        result = pick_random_suggestion(g, "alice", random.Random(0))
        self.assertIn(result, {"dave", "erin", "frank"})

    def test_never_returns_self_or_existing_friend(self):
        g = sample_network()
        for seed in range(10):
            result = pick_random_suggestion(g, "bob", random.Random(seed))
            if result is not None:
                self.assertNotEqual(result, "bob")
                self.assertNotIn(result, g.get_person("bob").connections)


if __name__ == "__main__":
    unittest.main()
