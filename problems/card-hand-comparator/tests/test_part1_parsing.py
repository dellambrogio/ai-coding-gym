from __future__ import annotations

import unittest

from hand_utils import parse_card


class TestPart1Parsing(unittest.TestCase):
    def test_parses_ten_as_a_two_character_rank(self):
        card = parse_card("10H")
        self.assertEqual(10, card.rank)
        self.assertEqual("H", card.suit)

    def test_parses_face_cards(self):
        card = parse_card("QS")
        self.assertEqual(12, card.rank)
        self.assertEqual("S", card.suit)


if __name__ == "__main__":
    unittest.main()
