from __future__ import annotations

import unittest

from engine import is_legal_pick
from pieces import Mark
from tests.test_helpers import p


class TestPart1FixBug(unittest.TestCase):
    def test_rejects_card_not_on_table(self):
        shown = [
            p(1, Mark.SUN),
            p(5, Mark.MOON),
            p(9, Mark.STAR),
        ]
        fake = p(5, Mark.CLOUD)

        self.assertFalse(
            is_legal_pick(shown, [shown[0], fake, shown[2]])
        )

    def test_rejects_using_same_single_card_twice(self):
        shown = [
            p(5, Mark.SUN),
            p(4, Mark.MOON),
            p(6, Mark.STAR),
        ]

        self.assertFalse(
            is_legal_pick(shown, [shown[0], shown[0], shown[2]])
        )

    def test_accepts_real_triple_from_table(self):
        shown = [
            p(2, Mark.SUN),
            p(4, Mark.MOON),
            p(9, Mark.STAR),
            p(7, Mark.CLOUD),
        ]

        self.assertTrue(
            is_legal_pick(shown, [shown[0], shown[1], shown[2]])
        )


if __name__ == "__main__":
    unittest.main()
