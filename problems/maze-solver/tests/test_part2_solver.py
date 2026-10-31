import unittest

from mazes import (
    get_anywhere_start_end_maze,
    get_blocked_maze,
    get_small_maze,
)
from solver import Solver
from tests.helpers import assert_valid_path


class Part2SolverTests(unittest.TestCase):
    def test_solver_finds_a_valid_path_in_small_maze(self) -> None:
        maze = get_small_maze()
        path = Solver(maze).solve()
        assert_valid_path(self, maze, path)

    def test_solver_returns_none_when_no_path_exists(self) -> None:
        maze = get_blocked_maze()
        path = Solver(maze).solve()
        self.assertIsNone(path)

    def test_solver_uses_the_actual_start_and_end_positions(self) -> None:
        maze = get_anywhere_start_end_maze()
        path = Solver(maze).solve()
        assert_valid_path(self, maze, path)


if __name__ == "__main__":
    unittest.main()
