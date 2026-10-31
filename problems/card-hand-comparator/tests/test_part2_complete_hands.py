from __future__ import annotations

import unittest

from card_hand import PLAYER1, PLAYER2, TIE, compare_hands
from tests.test_helpers import assert_outcome


class TestPart2CompleteHands(unittest.TestCase):
    def test_three_of_a_kind_beats_one_pair(self):
        hand1 = ["AH", "AD", "AS", "7C", "2D"]
        hand2 = ["KH", "KD", "QC", "JS", "9D"]

        assert_outcome(self, compare_hands(hand1, hand2), PLAYER1)

    def test_pair_tiebreak_uses_pair_rank_then_kickers(self):
        hand1 = ["AH", "AD", "KC", "7S", "2D"]
        hand2 = ["KH", "KD", "QC", "JS", "9D"]

        assert_outcome(self, compare_hands(hand1, hand2), PLAYER1)

    def test_same_rank_pattern_and_kickers_is_a_tie(self):
        hand1 = ["AH", "AD", "KC", "7S", "2D"]
        hand2 = ["AS", "AC", "KD", "7H", "2C"]

        assert_outcome(self, compare_hands(hand1, hand2), TIE)

    def test_full_house_beats_three_of_a_kind(self):
        hand1 = ["QH", "QD", "QS", "2C", "2D"]
        hand2 = ["AH", "AD", "AS", "7C", "3D"]

        assert_outcome(self, compare_hands(hand1, hand2), PLAYER1)

    def test_high_card_can_lose(self):
        hand1 = ["AH", "KD", "9C", "7S", "3D"]
        hand2 = ["QH", "QD", "8C", "5S", "2D"]

        assert_outcome(self, compare_hands(hand1, hand2), PLAYER2)


if __name__ == "__main__":
    unittest.main()
