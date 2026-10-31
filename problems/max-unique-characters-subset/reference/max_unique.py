from __future__ import annotations

from typing import Sequence, Set

from subset_utils import contains_repeated_chars


def maximize_unique_characters(words: Sequence[str]) -> Set[str]:
    """Branch and bound over character bitmasks, longest words first."""
    for w in words:
        if not isinstance(w, str):
            raise TypeError(f"expected str, got {type(w).__name__}")

    alphabet = {ch: i for i, ch in enumerate(sorted(set("".join(words))))}
    masks: dict[int, str] = {}
    for w in words:
        if w and not contains_repeated_chars(w):
            mask = 0
            for ch in w:
                mask |= 1 << alphabet[ch]
            masks.setdefault(mask, w)
    items = sorted(masks.items(), key=lambda item: -len(item[1]))

    # suffix_union[i]: every character still reachable from items[i:].
    suffix_union = [0] * (len(items) + 1)
    for i in range(len(items) - 1, -1, -1):
        suffix_union[i] = suffix_union[i + 1] | items[i][0]

    best_mask, best_words = 0, []
    chosen: list[str] = []

    def search(i: int, used: int) -> None:
        nonlocal best_mask, best_words
        if used.bit_count() > best_mask.bit_count():
            best_mask, best_words = used, list(chosen)
        if i == len(items) or (used | suffix_union[i]).bit_count() <= best_mask.bit_count():
            return
        mask, w = items[i]
        if not used & mask:
            chosen.append(w)
            search(i + 1, used | mask)
            chosen.pop()
        search(i + 1, used)

    search(0, 0)
    return set(best_words)
