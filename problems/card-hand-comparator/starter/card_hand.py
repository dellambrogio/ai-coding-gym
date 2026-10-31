from __future__ import annotations

from typing import Sequence

from hand_utils import HandSummary


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
    raise NotImplementedError("Not implemented yet.")


def score_hand(hand: Sequence[str], evaluators: Sequence[HandCategoryEvaluator] | None = None) -> tuple[int, tuple[int, ...]]:
    _ = hand
    _ = evaluators
    raise NotImplementedError("Not implemented yet.")


def compare_with_evaluators(
    hand1: Sequence[str],
    hand2: Sequence[str],
    evaluators: Sequence[HandCategoryEvaluator],
) -> str:
    _ = hand1
    _ = hand2
    _ = evaluators
    raise NotImplementedError("Not implemented yet.")


def compare_hands(hand1: Sequence[str], hand2: Sequence[str]) -> str:
    _ = hand1
    _ = hand2
    raise NotImplementedError("Not implemented yet.")


def compare_partial_hands(
    hand1: Sequence[str],
    hand2: Sequence[str],
    hand_size: int = HAND_SIZE,
) -> str:
    _ = hand1
    _ = hand2
    _ = hand_size
    raise NotImplementedError("Not implemented yet.")
