"""Part 2: Solver sinks every ship."""

import random
import unittest

from board import Board
from fleet import get_test_fleet
from solver import Solver


class SolverTest(unittest.TestCase):

    def test_should_sink_all_ships(self) -> None:
        board = Board(grid_size=6)
        fleet = get_test_fleet()
        board.place_ship(fleet[0], row=0, col=0, horizontal=True)
        board.place_ship(fleet[1], row=3, col=0, horizontal=True)
        solver = Solver(board)
        solver.solve()
        self.assertTrue(board.all_sunk(), "didn't sink all ships")
        self.assertEqual(
            len(solver.get_shots()),
            board.total_shots(),
            "shot count mismatch"
        )
        self.assertLess(board.total_shots(), 36, "too many shots on a 6x6 board")


if __name__ == "__main__":
    unittest.main()
