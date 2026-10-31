from __future__ import annotations

import unittest

from subset_utils import validate_selection


class TestPart1Validation(unittest.TestCase):
    def test_accepts_legal_but_suboptimal_selection(self):
        words = ["ab", "cd", "ef"]
        chosen = {"ab", "cd"}

        is_valid, score = validate_selection(words, chosen)

        self.assertTrue(is_valid)
        self.assertEqual(4, score)

    def test_accepts_single_word(self):
        words = ["abc", "de"]
        chosen = {"abc"}

        is_valid, score = validate_selection(words, chosen)

        self.assertTrue(is_valid)
        self.assertEqual(3, score)

    def test_accepts_single_character_words(self):
        words = ["a", "b", "c"]
        chosen = {"a", "b"}

        is_valid, score = validate_selection(words, chosen)

        self.assertTrue(is_valid)
        self.assertEqual(2, score)

    def test_accepts_all_words_when_disjoint(self):
        words = ["ab", "cde", "fg"]
        chosen = {"ab", "cde", "fg"}

        is_valid, score = validate_selection(words, chosen)

        self.assertTrue(is_valid)
        self.assertEqual(7, score)

    def test_rejects_internal_duplicate_word_accepts_clean_word(self):
        words = ["aa", "bc", "def"]

        is_valid, score = validate_selection(words, {"aa"})
        self.assertFalse(is_valid)
        self.assertEqual(0, score)

        is_valid, score = validate_selection(words, {"bc"})
        self.assertTrue(is_valid)
        self.assertEqual(2, score)

    def test_rejects_global_character_overlap_accepts_disjoint_words(self):
        words = ["ab", "bc", "de"]

        is_valid, score = validate_selection(words, {"ab", "bc"})
        self.assertFalse(is_valid)
        self.assertEqual(0, score)

        is_valid, score = validate_selection(words, {"ab", "de"})
        self.assertTrue(is_valid)
        self.assertEqual(4, score)

    def test_rejects_words_not_in_input_accepts_listed_words(self):
        words = ["ab", "cd"]

        is_valid, score = validate_selection(words, {"ab", "xy"})
        self.assertFalse(is_valid)
        self.assertEqual(0, score)

        is_valid, score = validate_selection(words, {"ab"})
        self.assertTrue(is_valid)
        self.assertEqual(2, score)

    def test_empty_selection_is_valid(self):
        words = ["ab", "cd"]
        chosen = set()

        is_valid, score = validate_selection(words, chosen)

        self.assertTrue(is_valid)
        self.assertEqual(0, score)


if __name__ == "__main__":
    unittest.main()
