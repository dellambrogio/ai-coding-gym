from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


RANK_TO_VALUE = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}
VALID_SUITS = {"H", "D", "C", "S"}
FULL_DECK = tuple(
    f"{rank}{suit}" for rank in RANK_TO_VALUE for suit in ("H", "D", "C", "S"))


@dataclass(frozen=True)
class Card:
    rank: int
    suit: str
    text: str


@dataclass(frozen=True)
class HandSummary:
    cards: tuple[Card, ...]
    sorted_ranks_desc: tuple[int, ...]
    rank_counts: tuple[tuple[int, int], ...]


def parse_card(card_text: str) -> Card:
    if len(card_text) < 2:
        raise ValueError(f"invalid card: {card_text!r}")

    suit = card_text[-1].upper()
    rank_text = card_text[0].upper()

    if suit not in VALID_SUITS:
        raise ValueError(f"invalid suit: {card_text!r}")
    if rank_text not in RANK_TO_VALUE:
        raise ValueError(f"invalid rank: {card_text!r}")

    return Card(rank=RANK_TO_VALUE[rank_text], suit=suit, text=f"{rank_text}{suit}")


def summarize_hand(hand: list[str]) -> HandSummary:
    cards = tuple(parse_card(card_text) for card_text in hand)
    normalized = [card.text for card in cards]
    if len(set(normalized)) != len(normalized):
        raise ValueError("duplicate cards are not allowed")

    rank_counter = Counter(card.rank for card in cards)
    rank_counts = tuple(sorted(rank_counter.items(),
                        key=lambda item: (-item[1], -item[0])))
    sorted_ranks_desc = tuple(
        sorted((card.rank for card in cards), reverse=True))
    return HandSummary(cards=cards, sorted_ranks_desc=sorted_ranks_desc, rank_counts=rank_counts)
