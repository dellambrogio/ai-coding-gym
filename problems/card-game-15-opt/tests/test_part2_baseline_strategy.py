from __future__ import annotations

import unittest

from engine import is_legal_pick
from pieces import Mark
from strategies import choose_first_valid
from tests.test_helpers import p


class TestPart2BaselineStrategy(unittest.TestCase):
    def test_returns_none_when_no_move_exists(self):
        shown = [
            p(1, Mark.SUN),
            p(1, Mark.MOON),
            p(1, Mark.STAR),
            p(1, Mark.CLOUD),
        ]

        result = choose_first_valid(shown, [])

        self.assertIsNone(result)

    def test_returns_legal_move_when_move_exists(self):
        shown = [
            p(2, Mark.SUN),
            p(4, Mark.MOON),
            p(9, Mark.STAR),
            p(7, Mark.CLOUD),
        ]

        result = choose_first_valid(shown, [])

        self.assertIsNotNone(result)
        self.assertTrue(is_legal_pick(shown, result))

    def test_returned_cards_sum_to_target(self):
        shown = [
            p(5, Mark.SUN),
            p(5, Mark.MOON),
            p(5, Mark.STAR),
            p(8, Mark.CLOUD),
        ]

        result = choose_first_valid(shown, [])

        self.assertIsNotNone(result)
        self.assertEqual(15, sum(card.amount for card in result))


if __name__ == "__main__":
    unittest.main()
