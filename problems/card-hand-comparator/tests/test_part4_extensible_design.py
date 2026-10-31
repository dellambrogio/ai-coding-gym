from __future__ import annotations

import unittest

from card_hand import HandCategoryEvaluator, PLAYER1, build_default_evaluators, compare_with_evaluators
from hand_utils import HandSummary
from tests.test_helpers import assert_outcome


class AllRedCardsEvaluator(HandCategoryEvaluator):
    category_rank = 100

    def evaluate(self, summary: HandSummary) -> tuple[int, tuple[int, ...]] | None:
        if all(card.suit in {"H", "D"} for card in summary.cards):
            return (self.category_rank, summary.sorted_ranks_desc)
        return None


class TestPart4ExtensibleDesign(unittest.TestCase):
    def test_custom_evaluator_can_be_added_without_rewriting_comparator(self):
        evaluators = [AllRedCardsEvaluator(), *build_default_evaluators()]

        hand1 = ["AH", "KD", "9H", "7D", "3H"]
        hand2 = ["AS", "AC", "KD", "7C", "2D"]

        assert_outcome(self, compare_with_evaluators(
            hand1, hand2, evaluators), PLAYER1)


if __name__ == "__main__":
    unittest.main()
