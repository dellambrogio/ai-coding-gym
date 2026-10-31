from __future__ import annotations

import unittest

from max_unique import maximize_unique_characters
from tests.test_helpers import check_valid_subset, tally_distinct_chars


class TestPart2SolverBasic(unittest.TestCase):
    def test_unique_optimum_basic(self):
        words = ["ab", "cd", "efg", "a", "cdef"]

        chosen = maximize_unique_characters(words)
        check_valid_subset(self, words, chosen)
        self.assertEqual({"ab", "cd", "efg"}, chosen)
        self.assertEqual(7, tally_distinct_chars(chosen))

    def test_reject_internal_duplicate_words(self):
        words = ["aa", "bc", "def"]

        chosen = maximize_unique_characters(words)
        check_valid_subset(self, words, chosen)
        self.assertEqual({"bc", "def"}, chosen)
        self.assertEqual(5, tally_distinct_chars(chosen))

    def test_digits_supported(self):
        words = ["2357", "19", "04", "1001"]

        chosen = maximize_unique_characters(words)
        check_valid_subset(self, words, chosen)
        self.assertEqual({"2357", "19", "04"}, chosen)
        self.assertEqual(8, tally_distinct_chars(chosen))

    def test_empty_input(self):
        words: list[str] = []

        chosen = maximize_unique_characters(words)
        self.assertEqual(set(), chosen)

    def test_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            maximize_unique_characters(["ab", 123])  # type: ignore[list-item]


if __name__ == "__main__":
    unittest.main()
