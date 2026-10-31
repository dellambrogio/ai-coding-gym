"""You'll implement this."""

from itertools import product
from typing import List, Optional, Set, Tuple

from board import Board, ShotResult
from fleet import Ship, get_test_fleet

Cell = Tuple[int, int]


class Solver:
    """Sinks all ships on a Battleship board.

    Probability density: every turn, count the placements of each ship still
    afloat that are consistent with what we know, and shoot the cell most
    placements cover. Placements through unsunk hits are weighted heavily, so
    the solver finishes a ship once it finds one.
    """

    def __init__(self, board: Board, fleet: Optional[List[Ship]] = None):
        self.board = board
        self.fleet = fleet or get_test_fleet()
        self.shots: List[Tuple[int, int]] = []

    def solve(self) -> None:
        n = self.board.grid_size
        afloat = sorted(ship.size for ship in self.fleet)
        misses: Set[Cell] = set()
        hits: Set[Cell] = set()  # hits on ships not sunk yet
        sunk: Set[Cell] = set()
        while not self.board.all_sunk():
            target = self._best_cell(n, afloat, misses, hits, sunk)
            self.shots.append(target)
            result = self.board.check_shot(*target)
            if result == ShotResult.MISS:
                misses.add(target)
                continue
            hits.add(target)
            if result == ShotResult.SUNK:
                # The board doesn't say which ship sank: guess the longest straight
                # run of hits through this cell, and the largest ship that fits it.
                run = self._run_through(target, hits)
                size = next((s for s in reversed(afloat) if s <= len(run)), afloat[0])
                afloat.remove(size)
                sunk |= run
                hits -= run

    def get_shots(self) -> List[Tuple[int, int]]:
        return self.shots

    @staticmethod
    def _run_through(cell: Cell, hits: Set[Cell]) -> Set[Cell]:
        best = {cell}
        for dr, dc in ((0, 1), (1, 0)):
            run = {cell}
            for sign in (1, -1):
                r, c = cell[0] + sign * dr, cell[1] + sign * dc
                while (r, c) in hits:
                    run.add((r, c))
                    r, c = r + sign * dr, c + sign * dc
            if len(run) > len(best):
                best = run
        return best

    def _best_cell(self, n, afloat, misses, hits, sunk) -> Cell:
        blocked = misses | sunk
        shot = misses | sunk | hits
        score = {}
        for size in afloat:
            for r, c, horizontal in product(range(n), range(n), (True, False)):
                cells = [(r, c + i) if horizontal else (r + i, c) for i in range(size)]
                if any(not (0 <= x < n and 0 <= y < n) or (x, y) in blocked for x, y in cells):
                    continue
                weight = 1 + 100 * sum(cell in hits for cell in cells)
                for cell in cells:
                    if cell not in shot:
                        score[cell] = score.get(cell, 0) + weight
        if not score:
            if sunk:  # a guess about which cells sank was wrong: forget the guesses
                return self._best_cell(n, afloat, misses, hits | sunk, set())
            return next(cell for cell in product(range(n), range(n)) if cell not in shot)
        return max(score, key=lambda cell: (score[cell], -cell[0], -cell[1]))
