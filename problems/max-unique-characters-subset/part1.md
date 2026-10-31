## Part 1: Validate a selection

Given a list of words, choose a subset in which no character appears twice: not inside a word, and not across two words. The goal is to cover as many distinct characters as possible.

`subset_utils.validate_selection(words, chosen) -> (is_valid, score)` should accept any legal selection of input words and return the number of characters it covers, or `(False, 0)` for an illegal one. It rejects legal selections: fix it.

Tests: `tests/test_part1_validation.py`
