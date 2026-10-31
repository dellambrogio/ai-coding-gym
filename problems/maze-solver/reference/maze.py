from __future__ import annotations

from enum import Enum
from typing import FrozenSet, List, NamedTuple, Optional, Sequence


class Position(NamedTuple):
    row: int
    col: int


class CellType(str, Enum):
    WALL = "#"
    OPEN = "."
    START = "S"
    END = "E"
    PATH = "*"
    RIGHT_ONLY = ">"
    LEFT_ONLY = "<"


class Maze:
    def __init__(self, grid: Sequence[str]) -> None:
        if not grid:
            raise ValueError("Maze grid cannot be empty.")

        row_lengths = {len(row) for row in grid}
        if len(row_lengths) != 1:
            raise ValueError("Maze grid must be rectangular.")

        self._grid: List[List[str]] = [list(row) for row in grid]
        self._rows = len(self._grid)
        self._cols = len(self._grid[0])
        self._start = self._find_cell(CellType.START.value)
        self._end = self._find_cell(CellType.END.value)

    def _find_cell(self, cell: str) -> Position:
        for row in range(self._rows):
            for col in range(self._cols):
                if self._grid[row][col] == cell:
                    return Position(row, col)
        raise ValueError(f"No {cell!r} cell found in maze.")

    def get_start(self) -> Position:
        return self._start

    def get_end(self) -> Position:
        return self._end

    def get_cell(self, pos: Position) -> str:
        return self._grid[pos.row][pos.col]

    def render(self) -> List[str]:
        return ["".join(row) for row in self._grid]

    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.row < self._rows and 0 <= pos.col < self._cols

    def is_key_cell(self, cell: str) -> bool:
        return len(cell) == 1 and "a" <= cell <= "z"

    def is_door_cell(self, cell: str) -> bool:
        return (
            len(cell) == 1
            and "A" <= cell <= "Z"
            and cell not in (CellType.START.value, CellType.END.value)
        )

    def collect_key(
        self, keys: FrozenSet[str], pos: Position
    ) -> FrozenSet[str]:
        cell = self.get_cell(pos)
        if self.is_key_cell(cell):
            return frozenset(set(keys) | {cell})
        return keys

    def is_valid_move(
        self,
        from_pos: Position,
        to_pos: Position,
        keys: Optional[FrozenSet[str]] = None,
    ) -> bool:
        if keys is None:
            keys = frozenset()

        if not self.in_bounds(to_pos):
            return False

        to_cell = self.get_cell(to_pos)
        if to_cell == CellType.WALL.value:
            return False

        # One-way cells: enter and leave '>' moving right, '<' moving left.
        d_col = to_pos.col - from_pos.col
        moving_right = to_pos.row == from_pos.row and d_col == 1
        moving_left = to_pos.row == from_pos.row and d_col == -1
        for cell in (self.get_cell(from_pos), to_cell):
            if cell == CellType.RIGHT_ONLY.value and not moving_right:
                return False
            if cell == CellType.LEFT_ONLY.value and not moving_left:
                return False

        if self.is_door_cell(to_cell) and to_cell.lower() not in keys:
            return False

        return True

    def get_neighbors(
        self, pos: Position, keys: Optional[FrozenSet[str]] = None
    ) -> List[Position]:
        if keys is None:
            keys = frozenset()

        neighbors: List[Position] = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nxt = Position(pos.row + dr, pos.col + dc)
            if self.is_valid_move(pos, nxt, keys):
                neighbors.append(nxt)
        return neighbors

    def render_with_path(self, path: List[Position]) -> List[str]:
        result = [row[:] for row in self._grid]

        for pos in path:
            cell = result[pos.row][pos.col]
            if cell in (CellType.OPEN.value, CellType.PATH.value):
                result[pos.row][pos.col] = CellType.PATH.value

        return ["".join(row) for row in result]

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols
