from __future__ import annotations

import unittest

from benchmark import build_dataset, run_benchmark
from substring_finder import SubstringTrie, find_all_contained_pairs

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


def brute_force_pairs(strings: list[str]) -> set[tuple[str, str]]:
    return {
        (container, other)
        for i, container in enumerate(strings)
        for j, other in enumerate(strings)
        if i != j and other in container
    }


class TestPart4AllPairs(unittest.TestCase):
    def test_all_contained_words_sorted(self):
        trie = SubstringTrie()
        trie.insert("am")
        trie.insert("pro")
        trie.insert("gram")

        self.assertEqual(
            trie.all_contained_words("programming"), ["am", "gram", "pro"]
        )

    def test_all_pairs_for_example(self):
        pairs = find_all_contained_pairs(["programming", "am", "pro"])

        self.assertEqual(
            pairs, [("programming", "am"), ("programming", "pro")]
        )

    def test_duplicate_pair_reported_once(self):
        self.assertEqual(
            find_all_contained_pairs(["am", "am"]), [("am", "am")]
        )

    def test_no_pairs_returns_empty_list(self):
        self.assertEqual(
            find_all_contained_pairs(["hello", "world", "zebra"]), []
        )

    def test_chain_of_containments(self):
        pairs = find_all_contained_pairs(["abc", "bc", "c"])

        self.assertEqual(
            pairs, [("abc", "bc"), ("abc", "c"), ("bc", "c")]
        )

    def test_pairs_agree_with_brute_force(self):
        self.assertEqual(
            set(find_all_contained_pairs(MIXED)), brute_force_pairs(MIXED)
        )
        self.assertEqual(
            find_all_contained_pairs(MIXED), sorted(brute_force_pairs(MIXED))
        )

    def test_benchmark_strategies_agree_with_valid_answers(self):
        dataset = build_dataset()
        valid = {
            container
            for container, _ in brute_force_pairs(dataset)
        }
        self.assertTrue(valid)

        for row in run_benchmark(dataset):
            self.assertTrue(
                row["implemented"], f"{row['strategy']} should be implemented"
            )
            self.assertIn(row["answer"], valid)


if __name__ == "__main__":
    unittest.main()
