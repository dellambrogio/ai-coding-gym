import unittest

from mazes import (
    get_door_without_key_maze,
    get_key_backtrack_maze,
    get_key_door_maze,
)
from solver import Solver
from tests.helpers import assert_valid_path


class Part4KeysAndDoorsTests(unittest.TestCase):
    def test_solver_cannot_walk_through_a_locked_door_without_key(self) -> None:
        maze = get_door_without_key_maze()
        path = Solver(maze).solve()
        self.assertIsNone(path)

    def test_solver_collects_the_key_before_opening_the_door(self) -> None:
        maze = get_key_door_maze()
        path = Solver(maze).solve()
        assert_valid_path(self, maze, path)

    def test_solver_can_revisit_positions_after_collecting_a_key(self) -> None:
        maze = get_key_backtrack_maze()
        path = Solver(maze).solve()
        assert_valid_path(self, maze, path)


if __name__ == "__main__":
    unittest.main()
