from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from itertools import combinations
import random
from typing import Callable, List, Optional, Sequence, Tuple

from pieces import Mark, Piece


TARGET_TOTAL = 15
OPENING_SIZE = 16
PERFECT_SCORE = 180


@dataclass
class RoundState:
    visible: List[Piece] = field(default_factory=list)
    reserve: List[Piece] = field(default_factory=list)
    points: int = 0

    def duplicate(self) -> RoundState:
        return RoundState(
            visible=list(self.visible),
            reserve=list(self.reserve),
            points=self.points,
        )


Chooser = Callable[[Sequence[Piece], Sequence[Piece]], Optional[List[Piece]]]


def build_pack() -> List[Piece]:
    pack: List[Piece] = []
    for mark in Mark:
        for amount in range(1, 10):
            pack.append(Piece(amount, mark))
    return pack


def begin_round(seed: int | None = None) -> RoundState:
    rng = random.Random(seed)
    pack = build_pack()
    rng.shuffle(pack)

    visible = pack[:OPENING_SIZE]
    reserve = pack[OPENING_SIZE:]
    return RoundState(visible=visible, reserve=reserve, points=0)


def all_playable_groups(visible: Sequence[Piece]) -> List[List[Piece]]:
    groups: List[List[Piece]] = []
    for trio in combinations(visible, 3):
        if sum(card.amount for card in trio) == TARGET_TOTAL:
            groups.append(list(trio))
    return groups


def has_any_move(visible: Sequence[Piece]) -> bool:
    return len(all_playable_groups(visible)) > 0


def is_legal_pick(visible: Sequence[Piece], picked: Sequence[Piece]) -> bool:
    if len(picked) != 3:
        return False

    if sum(card.amount for card in picked) != TARGET_TOTAL:
        return False

    return True


def remove_picked_cards(visible: List[Piece], picked: Sequence[Piece]) -> None:
    for wanted in picked:
        for idx, current in enumerate(visible):
            if current == wanted:
                visible.pop(idx)
                break
        else:
            raise ValueError(
                "attempted to remove a card that is not on the table")


def refill_visible(
    visible: List[Piece],
    reserve: List[Piece],
    target_size: int = OPENING_SIZE,
) -> None:
    while len(visible) < target_size and reserve:
        visible.append(reserve.pop(0))


def apply_pick(state: RoundState, picked: Sequence[Piece]) -> None:
    if not is_legal_pick(state.visible, picked):
        raise ValueError("illegal pick")

    remove_picked_cards(state.visible, picked)
    state.points += TARGET_TOTAL
    refill_visible(state.visible, state.reserve)


def play_round(chooser: Chooser, seed: int | None = None) -> int:
    state = begin_round(seed=seed)

    while True:
        legal_groups = all_playable_groups(state.visible)
        if not legal_groups:
            return state.points

        proposal = chooser(tuple(state.visible), tuple(state.reserve))
        if proposal is None:
            return state.points

        apply_pick(state, proposal)


def play_from_state(state: RoundState, chooser: Chooser) -> int:
    local = state.duplicate()

    while True:
        legal_groups = all_playable_groups(local.visible)
        if not legal_groups:
            return local.points

        proposal = chooser(tuple(local.visible), tuple(local.reserve))
        if proposal is None:
            return local.points

        apply_pick(local, proposal)


def encode_state(
    visible: Sequence[Piece],
    reserve: Sequence[Piece],
) -> Tuple[Tuple[Piece, ...], Tuple[Piece, ...]]:
    return tuple(visible), tuple(reserve)
