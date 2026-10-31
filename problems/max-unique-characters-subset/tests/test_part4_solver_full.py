from __future__ import annotations

import unittest

from max_unique import maximize_unique_characters
from tests.test_helpers import check_valid_subset, tally_distinct_chars


class TestPart4SolverFull(unittest.TestCase):
    def test_full_alphanumeric_coverage(self):
        words = [
            "abc", "def", "ghi", "jkl", "mno", "pqr",
            "stu", "vwx", "yz0", "123", "456", "789",
            "ab", "cde", "fgh", "ijk", "lmn", "opq", "rst", "uvw", "xyz",
            "az", "by", "cx", "dw", "ev", "fu", "gt", "hs", "ir", "jq",
            "k0", "l1", "m2", "n3", "o4", "p5", "q6", "r7", "s8", "t9",
            "aa", "bb", "101", "232", "letter", "noon",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
            "u", "v", "w", "x", "y", "z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        ]

        chosen = maximize_unique_characters(words)
        check_valid_subset(self, words, chosen)
        self.assertEqual(36, tally_distinct_chars(chosen))

    def test_duplicate_strings_in_input(self):
        words = ["ab", "ab", "cd", "ef", "gh", "ij"]

        chosen = maximize_unique_characters(words)
        check_valid_subset(self, words, chosen)
        self.assertEqual(10, tally_distinct_chars(chosen))

    def test_returns_actual_subset_not_only_score(self):
        words = ["ab", "cd", "ef", "gh"]

        chosen = maximize_unique_characters(words)

        self.assertIsInstance(chosen, set)
        check_valid_subset(self, words, chosen)
        self.assertEqual({"ab", "cd", "ef", "gh"}, chosen)


if __name__ == "__main__":
    unittest.main()
