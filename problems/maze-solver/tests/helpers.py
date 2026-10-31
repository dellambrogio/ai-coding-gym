from __future__ import annotations

from typing import FrozenSet, Iterable, List

from maze import Maze, Position


def _is_key(cell: str) -> bool:
    return len(cell) == 1 and "a" <= cell <= "z"


def _is_door(cell: str) -> bool:
    return len(cell) == 1 and "A" <= cell <= "Z" and cell not in ("S", "E")


def _collect_key(keys: FrozenSet[str], cell: str) -> FrozenSet[str]:
    if _is_key(cell):
        return frozenset(set(keys) | {cell})
    return keys


def _can_step(
    grid: List[str],
    from_pos: Position,
    to_pos: Position,
    keys: FrozenSet[str],
) -> bool:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    if not (0 <= to_pos.row < rows and 0 <= to_pos.col < cols):
        return False

    if abs(from_pos.row - to_pos.row) + abs(from_pos.col - to_pos.col) != 1:
        return False

    from_cell = grid[from_pos.row][from_pos.col]
    to_cell = grid[to_pos.row][to_pos.col]

    if to_cell == "#":
        return False

    # Directional passages:
    # - Entering '>' is only valid from the left.
    # - Leaving '>' is only valid to the right.
    # - Entering '<' is only valid from the right.
    # - Leaving '<' is only valid to the left.
    if from_cell == ">" and not (
        to_pos.row == from_pos.row and to_pos.col == from_pos.col + 1
    ):
        return False

    if from_cell == "<" and not (
        to_pos.row == from_pos.row and to_pos.col == from_pos.col - 1
    ):
        return False

    if to_cell == ">" and not (
        from_pos.row == to_pos.row and from_pos.col == to_pos.col - 1
    ):
        return False

    if to_cell == "<" and not (
        from_pos.row == to_pos.row and from_pos.col == to_pos.col + 1
    ):
        return False

    if _is_door(to_cell) and to_cell.lower() not in keys:
        return False

    return True


def assert_valid_path(testcase, maze: Maze, path) -> None:
    testcase.assertIsNotNone(path, "Expected a valid path, got None.")
    testcase.assertGreater(len(path), 0, "Path must not be empty.")
    testcase.assertEqual(path[0], maze.get_start(), "Path must start at S.")
    testcase.assertEqual(path[-1], maze.get_end(), "Path must end at E.")

    grid = maze.render()
    keys: FrozenSet[str] = frozenset()
    keys = _collect_key(keys, grid[path[0].row][path[0].col])

    for from_pos, to_pos in zip(path, path[1:]):
        testcase.assertTrue(
            _can_step(grid, from_pos, to_pos, keys),
            f"Illegal step: {from_pos} -> {to_pos} with keys={sorted(keys)}",
        )
        keys = _collect_key(keys, grid[to_pos.row][to_pos.col])
