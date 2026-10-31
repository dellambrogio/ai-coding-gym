from __future__ import annotations

import unittest

from card_hand import PLAYER1, UNKNOWN, compare_partial_hands
from tests.test_helpers import assert_outcome


class TestPart3PartialHands(unittest.TestCase):
    def test_returns_winner_when_outcome_is_already_forced(self):
        hand1 = ["AH", "AD", "AC", "AS"]
        hand2 = ["KH", "KD", "KC", "2S", "2D"]

        assert_outcome(self, compare_partial_hands(hand1, hand2), PLAYER1)

    def test_returns_unknown_when_missing_cards_can_change_the_result(self):
        hand1 = ["AH", "KD", "7C", "8D"]
        hand2 = ["QH", "QS", "2C", "3D"]

        assert_outcome(self, compare_partial_hands(hand1, hand2), UNKNOWN)


if __name__ == "__main__":
    unittest.main()
