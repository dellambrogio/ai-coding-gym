from __future__ import annotations

import unittest

from engine import RoundState, is_legal_pick, play_from_state
from pieces import Mark
from strategies import choose_best_outcome, choose_first_valid
from tests.test_helpers import p


class TestPart4ImprovedStrategy(unittest.TestCase):
    def test_improved_strategy_picks_a_legal_move(self):
        shown = [
            p(1, Mark.SUN),
            p(5, Mark.MOON),
            p(9, Mark.STAR),
            p(2, Mark.CLOUD),
            p(4, Mark.SUN),
            p(8, Mark.MOON),
        ]

        result = choose_best_outcome(shown, [])

        self.assertIsNotNone(result)
        self.assertTrue(is_legal_pick(shown, result))

    def test_improved_strategy_can_beat_simple_first_choice_on_fixed_state(self):
        state = RoundState(
            visible=[
                p(1, Mark.SUN),
                p(5, Mark.MOON),
                p(9, Mark.STAR),
                p(2, Mark.CLOUD),
                p(4, Mark.SUN),
                p(8, Mark.MOON),
            ],
            reserve=[
                p(6, Mark.STAR),
                p(3, Mark.CLOUD),
                p(7, Mark.SUN),
            ],
            points=0,
        )

        simple_score = play_from_state(state, choose_first_valid)
        better_score = play_from_state(state, choose_best_outcome)

        self.assertGreaterEqual(better_score, simple_score)

    def test_improved_strategy_never_returns_illegal_move_in_small_search_case(self):
        state = RoundState(
            visible=[
                p(3, Mark.SUN),
                p(3, Mark.MOON),
                p(9, Mark.STAR),
                p(6, Mark.CLOUD),
                p(1, Mark.SUN),
                p(5, Mark.STAR),
            ],
            reserve=[
                p(4, Mark.MOON),
                p(2, Mark.CLOUD),
                p(8, Mark.SUN),
            ],
            points=0,
        )

        result = choose_best_outcome(state.visible, state.reserve)

        self.assertIsNotNone(result)
        self.assertTrue(is_legal_pick(state.visible, result))


if __name__ == "__main__":
    unittest.main()
