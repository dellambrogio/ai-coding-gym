from __future__ import annotations

import unittest

from substring_finder import find_contained_string


class TestPart1BruteForce(unittest.TestCase):
    def test_returns_container_for_example(self):
        strings = ["programming", "am", "pro"]

        self.assertEqual(find_contained_string(strings), "programming")

    def test_returns_none_when_no_pair_exists(self):
        strings = ["hello", "world", "zebra"]

        self.assertIsNone(find_contained_string(strings))

    def test_single_string_returns_none(self):
        self.assertIsNone(find_contained_string(["solo"]))

    def test_duplicates_count_as_containment(self):
        # Identical strings at different positions contain each other.
        self.assertEqual(find_contained_string(["am", "am"]), "am")

    def test_is_case_sensitive(self):
        # "abc" does not occur inside "ABC" under case-sensitive matching.
        self.assertIsNone(find_contained_string(["ABC", "abc"]))

    def test_returns_a_valid_container_on_mixed_list(self):
        strings = [
            "interview",
            "view",
            "redis",
            "distributed",
            "trib",
            "mute",
            "network",
            "net",
            "work",
        ]
        valid = {
            container
            for i, container in enumerate(strings)
            for j, other in enumerate(strings)
            if i != j and other in container
        }

        self.assertIn(find_contained_string(strings), valid)


if __name__ == "__main__":
    unittest.main()
