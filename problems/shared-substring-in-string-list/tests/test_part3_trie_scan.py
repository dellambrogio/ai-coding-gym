from __future__ import annotations

import unittest

from substring_finder import SubstringTrie, find_contained_string_trie

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


class TestPart3TrieScan(unittest.TestCase):
    def test_insert_then_find_contained_word(self):
        trie = SubstringTrie()
        trie.insert("am")
        trie.insert("pro")

        self.assertIn(trie.find_contained_word("programming"), {"am", "pro"})

    def test_find_contained_word_returns_none_when_no_match(self):
        trie = SubstringTrie()
        trie.insert("am")

        self.assertIsNone(trie.find_contained_word("zzzz"))

    def test_self_match_ignored_without_duplicate(self):
        trie = SubstringTrie()
        trie.insert("programming")

        self.assertIsNone(trie.find_contained_word("programming"))

    def test_self_match_reported_when_duplicate_exists(self):
        trie = SubstringTrie()
        trie.insert("am")
        trie.insert("am")

        self.assertEqual(trie.find_contained_word("am"), "am")

    def test_find_contained_string_trie_example(self):
        self.assertEqual(
            find_contained_string_trie(["programming", "am", "pro"]),
            "programming",
        )

    def test_trie_returns_none_when_no_pair_exists(self):
        self.assertIsNone(
            find_contained_string_trie(["hello", "world", "zebra"])
        )

    def test_trie_handles_duplicates(self):
        self.assertEqual(find_contained_string_trie(["am", "am"]), "am")

    def test_agrees_with_valid_containers_on_mixed_list(self):
        valid = valid_containers(MIXED)

        self.assertIn(find_contained_string_trie(MIXED), valid)


if __name__ == "__main__":
    unittest.main()
