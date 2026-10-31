from __future__ import annotations

from typing import Dict, List, Optional

from maze import Maze, Position


class Solver:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    @staticmethod
    def _reconstruct_path(
        parents: Dict[Position, Optional[Position]],
        end: Position,
    ) -> List[Position]:
        path: List[Position] = []
        current: Optional[Position] = end

        while current is not None:
            path.append(current)
            current = parents[current]

        path.reverse()
        return path

    def solve(self) -> Optional[List[Position]]:
        raise NotImplementedError("Solver.solve() not implemented yet.")
