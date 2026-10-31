from __future__ import annotations

from typing import Sequence, Set, Tuple


def contains_repeated_chars(word: str) -> bool:
    return len(word) != len(set(word))


def count_distinct_chars(chosen: Set[str]) -> int:
    taken: set[str] = set()
    for w in chosen:
        taken |= set(w)
    return len(taken)


def validate_selection(words: Sequence[str], chosen: Set[str]) -> Tuple[bool, int]:
    if not chosen.issubset(set(words)):
        return False, 0

    taken: set[str] = set()
    coverage = 0

    for w in chosen:
        if contains_repeated_chars(w) or taken & set(w):
            return False, 0

        taken |= set(w)
        coverage += len(w)

    return True, coverage
