import unittest

from mazes import (
    get_directional_blocked_entry_maze,
    get_directional_blocked_exit_maze,
    get_directional_passage_maze,
)
from solver import Solver
from tests.helpers import assert_valid_path


class Part3DirectionalTests(unittest.TestCase):
    def test_solver_handles_a_valid_directional_passage(self) -> None:
        maze = get_directional_passage_maze()
        path = Solver(maze).solve()
        assert_valid_path(self, maze, path)

    def test_solver_rejects_wrong_entry_into_left_only_cell(self) -> None:
        maze = get_directional_blocked_entry_maze()
        path = Solver(maze).solve()
        self.assertIsNone(path)

    def test_solver_rejects_wrong_exit_from_right_only_cell(self) -> None:
        maze = get_directional_blocked_exit_maze()
        path = Solver(maze).solve()
        self.assertIsNone(path)


if __name__ == "__main__":
    unittest.main()
