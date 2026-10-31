from __future__ import annotations

import unittest

from max_unique import maximize_unique_characters
from tests.test_helpers import check_valid_subset, tally_distinct_chars


class TestPart3SolverOptimized(unittest.TestCase):
    def test_medium_letters_dataset(self):
        words = [
            "ab", "cd", "ef", "gh", "ij", "kl", "mn", "op", "qr", "st", "uv", "wx", "yz",
            "ace", "bdf", "ghij", "klmn", "opqr", "stuv", "wxyz",
            "aa", "hello", "moon", "dad",
            "a", "bcdef", "mnop", "qrst", "uvw",
        ]

        chosen = maximize_unique_characters(words)
        check_valid_subset(self, words, chosen)
        self.assertEqual(26, tally_distinct_chars(chosen))

    def test_month_style_dataset(self):
        words = [
            "jan", "feb", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "oct", "nov", "dec"
        ]

        chosen = maximize_unique_characters(words)
        check_valid_subset(self, words, chosen)
        self.assertEqual(12, tally_distinct_chars(chosen))

    def test_empty_string_is_allowed(self):
        words = ["", "ab", "cd", "a", "ef"]

        chosen = maximize_unique_characters(words)
        check_valid_subset(self, words, chosen)
        self.assertEqual(6, tally_distinct_chars(chosen))

    def test_large_pairwise_dataset(self):
        alpha = "abcdefghijkl"
        words = [alpha[i] + alpha[j]
                 for i in range(len(alpha)) for j in range(i + 1, len(alpha))]

        chosen = maximize_unique_characters(words)
        check_valid_subset(self, words, chosen)
        self.assertEqual(12, tally_distinct_chars(chosen))


if __name__ == "__main__":
    unittest.main()
