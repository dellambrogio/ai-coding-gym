import unittest

from maze import Position
from mazes import get_render_maze


class Part1RenderingTests(unittest.TestCase):
    def test_render_with_path_preserves_start_and_end(self) -> None:
        maze = get_render_maze()
        path = [
            Position(1, 1),
            Position(1, 2),
            Position(1, 3),
            Position(2, 3),
            Position(3, 3),
        ]

        rendered = maze.render_with_path(path)

        self.assertEqual(rendered[1][1], "S")
        self.assertEqual(rendered[3][3], "E")

    def test_render_with_path_marks_open_cells(self) -> None:
        maze = get_render_maze()
        path = [
            Position(1, 1),
            Position(1, 2),
            Position(1, 3),
            Position(2, 3),
            Position(3, 3),
        ]

        rendered = maze.render_with_path(path)

        expected = [
            "#####",
            "#S**#",
            "#.#*#",
            "#..E#",
            "#####",
        ]
        self.assertEqual(rendered, expected)


if __name__ == "__main__":
    unittest.main()
