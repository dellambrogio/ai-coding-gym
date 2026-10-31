from __future__ import annotations

from typing import List, Optional, Sequence

from pieces import Piece


def choose_first_valid(
    visible: Sequence[Piece],
    reserve: Sequence[Piece],
) -> Optional[List[Piece]]:
    raise NotImplementedError("choose_first_valid() not implemented yet.")


def count_perfect_finishes(
    chooser,
    attempts: int = 100,
    first_seed: int = 0,
) -> int:
    raise NotImplementedError("count_perfect_finishes() not implemented yet.")


def choose_best_outcome(
    visible: Sequence[Piece],
    reserve: Sequence[Piece],
) -> Optional[List[Piece]]:
    raise NotImplementedError("choose_best_outcome() not implemented yet.")
