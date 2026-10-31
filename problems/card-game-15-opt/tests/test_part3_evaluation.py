from __future__ import annotations

import unittest
from unittest.mock import call, patch

from engine import PERFECT_SCORE
from strategies import choose_first_valid, count_perfect_finishes


class TestPart3Evaluation(unittest.TestCase):
    def test_counts_exact_number_of_perfect_finishes(self):
        scores_by_seed = {
            10: PERFECT_SCORE,
            11: 150,
            12: PERFECT_SCORE,
            13: 165,
        }

        with patch(
            "strategies.play_round",
            side_effect=lambda chooser, seed: scores_by_seed[seed],
        ) as mock_play_round:
            wins = count_perfect_finishes(
                choose_first_valid,
                attempts=4,
                first_seed=10,
            )

        self.assertEqual(2, wins)
        self.assertEqual(
            [
                call(choose_first_valid, seed=10),
                call(choose_first_valid, seed=11),
                call(choose_first_valid, seed=12),
                call(choose_first_valid, seed=13),
            ],
            mock_play_round.call_args_list,
        )

    def test_zero_attempts_returns_zero(self):
        with patch("strategies.play_round") as mock_play_round:
            wins = count_perfect_finishes(
                choose_first_valid,
                attempts=0,
                first_seed=5,
            )

        self.assertEqual(0, wins)
        mock_play_round.assert_not_called()


if __name__ == "__main__":
    unittest.main()
