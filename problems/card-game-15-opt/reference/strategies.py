from __future__ import annotations

from functools import lru_cache
from typing import List, Optional, Sequence

from engine import PERFECT_SCORE, RoundState, all_playable_groups, apply_pick, encode_state, play_round
from pieces import Piece


def choose_first_valid(
    visible: Sequence[Piece],
    reserve: Sequence[Piece],
) -> Optional[List[Piece]]:
    groups = all_playable_groups(visible)
    return groups[0] if groups else None


def count_perfect_finishes(
    chooser,
    attempts: int = 100,
    first_seed: int = 0,
) -> int:
    return sum(
        play_round(chooser, seed=seed) == PERFECT_SCORE
        for seed in range(first_seed, first_seed + attempts)
    )


@lru_cache(maxsize=None)
def _best_points(state_key) -> int:
    """Most points still reachable from this table and reserve."""
    visible, reserve = state_key
    best = 0
    for group in all_playable_groups(visible):
        state = RoundState(visible=list(visible), reserve=list(reserve))
        apply_pick(state, group)
        best = max(best, state.points + _best_points(encode_state(state.visible, state.reserve)))
    return best


def choose_best_outcome(
    visible: Sequence[Piece],
    reserve: Sequence[Piece],
) -> Optional[List[Piece]]:
    """Exhaustive search with memoization: the pick that leads to the highest final score."""
    best_group, best = None, -1
    for group in all_playable_groups(visible):
        state = RoundState(visible=list(visible), reserve=list(reserve))
        apply_pick(state, group)
        points = state.points + _best_points(encode_state(state.visible, state.reserve))
        if points > best:
            best_group, best = group, points
    return best_group
