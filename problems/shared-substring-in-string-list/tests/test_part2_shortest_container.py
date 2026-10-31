from __future__ import annotations

import unittest

from substring_finder import find_shortest_contained_string

# Mixed list with planted containments: "interview" contains "view",
# "distributed" contains "trib", "network" contains "net" and "work",
# and "queue" appears twice.
MIXED = [
    "interview",
    "view",
    "redis",
    "distributed",
    "trib",
    "mute",
    "network",
    "net",
    "work",
    "queue",
    "queue",
]


def valid_containers(strings: list[str]) -> set[str]:
    return {
        container
        for i, container in enumerate(strings)
        for j, other in enumerate(strings)
        if i != j and other in container
    }


class TestPart2ShortestContainer(unittest.TestCase):
    def test_matches_example_contract(self):
        self.assertEqual(
            find_shortest_contained_string(["programming", "am", "pro"]),
            "programming",
        )

    def test_returns_none_when_no_pair_exists(self):
        self.assertIsNone(find_shortest_contained_string(["hello", "world", "zebra"]))

    def test_handles_duplicate_strings(self):
        # Equal-length duplicates contain each other; pruning to strictly
        # shorter candidates would miss this legal pair.
        self.assertEqual(find_shortest_contained_string(["am", "am"]), "am")

    def test_handles_equal_length_list_without_pairs(self):
        strings = ["abcd", "abdc", "dcba"]

        self.assertIsNone(find_shortest_contained_string(strings))

    def test_prefers_shortest_container_over_input_order(self):
        # "programming" and "prompt" are both valid containers, but "prompt"
        # (length 6) is the shortest, so the required answer is "prompt".
        # An any-container solver may return "programming" (length 11)
        # instead, which fails this test.
        strings = ["programming", "am", "pro", "prompt"]

        self.assertEqual(find_shortest_contained_string(strings), "prompt")

    def test_agrees_with_valid_containers_on_mixed_list(self):
        valid = valid_containers(MIXED)
        self.assertEqual(
            valid, {"interview", "distributed", "network", "queue"}
        )

        self.assertIn(find_shortest_contained_string(MIXED), valid)


if __name__ == "__main__":
    unittest.main()
