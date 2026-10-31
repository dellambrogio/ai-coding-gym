from __future__ import annotations

from itertools import combinations
from typing import Sequence

from hand_utils import FULL_DECK, HandSummary, parse_card, summarize_hand


PLAYER1 = "player1"
PLAYER2 = "player2"
TIE = "tie"
UNKNOWN = "unknown"
HAND_SIZE = 5


class HandCategoryEvaluator:
    category_rank: int = 0

    def evaluate(self, summary: HandSummary) -> tuple[int, tuple[int, ...]] | None:
        raise NotImplementedError


def _rank_count_map(summary: HandSummary) -> dict[int, int]:
    return dict(summary.rank_counts)


class FourOfAKindEvaluator(HandCategoryEvaluator):
    category_rank = 6

    def evaluate(self, summary: HandSummary) -> tuple[int, tuple[int, ...]] | None:
        counts = _rank_count_map(summary)
        for rank, count in counts.items():
            if count == 4:
                kicker = max(other_rank for other_rank,
                             other_count in counts.items() if other_count == 1)
                return (self.category_rank, (rank, kicker))
        return None


class FullHouseEvaluator(HandCategoryEvaluator):
    category_rank = 5

    def evaluate(self, summary: HandSummary) -> tuple[int, tuple[int, ...]] | None:
        counts = _rank_count_map(summary)
        if sorted(counts.values()) == [2, 3]:
            trip_rank = max(
                rank for rank, count in counts.items() if count == 3)
            pair_rank = max(
                rank for rank, count in counts.items() if count == 2)
            return (self.category_rank, (trip_rank, pair_rank))
        return None


class ThreeOfAKindEvaluator(HandCategoryEvaluator):
    category_rank = 4

    def evaluate(self, summary: HandSummary) -> tuple[int, tuple[int, ...]] | None:
        counts = _rank_count_map(summary)
        if sorted(counts.values()) == [1, 1, 3]:
            trip_rank = max(
                rank for rank, count in counts.items() if count == 3)
            kickers = tuple(
                sorted((rank for rank, count in counts.items() if count == 1), reverse=True))
            return (self.category_rank, (trip_rank, *kickers))
        return None


class TwoPairEvaluator(HandCategoryEvaluator):
    category_rank = 3

    def evaluate(self, summary: HandSummary) -> tuple[int, tuple[int, ...]] | None:
        counts = _rank_count_map(summary)
        if sorted(counts.values()) == [1, 2, 2]:
            pair_ranks = tuple(
                sorted((rank for rank, count in counts.items() if count == 2), reverse=True))
            kicker = max(rank for rank, count in counts.items() if count == 1)
            return (self.category_rank, (*pair_ranks, kicker))
        return None


class OnePairEvaluator(HandCategoryEvaluator):
    category_rank = 2

    def evaluate(self, summary: HandSummary) -> tuple[int, tuple[int, ...]] | None:
        counts = _rank_count_map(summary)
        if sorted(counts.values()) == [1, 1, 1, 2]:
            pair_rank = max(
                rank for rank, count in counts.items() if count == 2)
            kickers = tuple(
                sorted((rank for rank, count in counts.items() if count == 1), reverse=True))
            return (self.category_rank, (pair_rank, *kickers))
        return None


class HighCardEvaluator(HandCategoryEvaluator):
    category_rank = 1

    def evaluate(self, summary: HandSummary) -> tuple[int, tuple[int, ...]] | None:
        return (self.category_rank, summary.sorted_ranks_desc)


def build_default_evaluators() -> list[HandCategoryEvaluator]:
    return [
        FourOfAKindEvaluator(),
        FullHouseEvaluator(),
        ThreeOfAKindEvaluator(),
        TwoPairEvaluator(),
        OnePairEvaluator(),
        HighCardEvaluator(),
    ]


def score_hand(hand: Sequence[str], evaluators: Sequence[HandCategoryEvaluator] | None = None) -> tuple[int, tuple[int, ...]]:
    if len(hand) != HAND_SIZE:
        raise ValueError(f"a hand has {HAND_SIZE} cards, got {len(hand)}")
    summary = summarize_hand(list(hand))
    scores = [score for e in (evaluators or build_default_evaluators())
              if (score := e.evaluate(summary)) is not None]
    if not scores:
        raise ValueError("no evaluator matched the hand")
    return max(scores)


def _outcome(score1: tuple, score2: tuple) -> str:
    if score1 > score2:
        return PLAYER1
    if score2 > score1:
        return PLAYER2
    return TIE


def compare_with_evaluators(
    hand1: Sequence[str],
    hand2: Sequence[str],
    evaluators: Sequence[HandCategoryEvaluator],
) -> str:
    return _outcome(score_hand(hand1, evaluators), score_hand(hand2, evaluators))


def compare_hands(hand1: Sequence[str], hand2: Sequence[str]) -> str:
    return compare_with_evaluators(hand1, hand2, build_default_evaluators())


def compare_partial_hands(
    hand1: Sequence[str],
    hand2: Sequence[str],
    hand_size: int = HAND_SIZE,
) -> str:
    """The winner if every way of completing both hands from the rest of the deck agrees, else UNKNOWN."""
    used = {parse_card(c).text for c in [*hand1, *hand2]}
    if len(used) != len(hand1) + len(hand2):
        raise ValueError("duplicate cards are not allowed")
    if len(hand1) > hand_size or len(hand2) > hand_size:
        raise ValueError(f"a hand has at most {hand_size} cards")
    deck = [c for c in FULL_DECK if c not in used]
    outcomes: set[str] = set()
    for extra1 in combinations(deck, hand_size - len(hand1)):
        rest = [c for c in deck if c not in extra1]
        score1 = score_hand([*hand1, *extra1])
        for extra2 in combinations(rest, hand_size - len(hand2)):
            outcomes.add(_outcome(score1, score_hand([*hand2, *extra2])))
            if len(outcomes) > 1:
                return UNKNOWN
    return outcomes.pop()
