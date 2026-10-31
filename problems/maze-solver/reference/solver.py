from __future__ import annotations

from collections import deque
from typing import Dict, FrozenSet, List, Optional, Tuple

from maze import Maze, Position

State = Tuple[Position, FrozenSet[str]]


class Solver:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    @staticmethod
    def _reconstruct_path(
        parents: Dict[State, Optional[State]],
        end: State,
    ) -> List[Position]:
        path: List[Position] = []
        current: Optional[State] = end

        while current is not None:
            path.append(current[0])
            current = parents[current]

        path.reverse()
        return path

    def solve(self) -> Optional[List[Position]]:
        """BFS over (position, keys held): a shortest path, or None."""
        start = self.maze.get_start()
        first: State = (start, self.maze.collect_key(frozenset(), start))
        parents: Dict[State, Optional[State]] = {first: None}
        queue = deque([first])
        while queue:
            state = queue.popleft()
            pos, keys = state
            if pos == self.maze.get_end():
                return self._reconstruct_path(parents, state)
            for nxt in self.maze.get_neighbors(pos, keys):
                nxt_state = (nxt, self.maze.collect_key(keys, nxt))
                if nxt_state not in parents:
                    parents[nxt_state] = state
                    queue.append(nxt_state)
        return None
