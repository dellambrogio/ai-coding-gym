from __future__ import annotations

from typing import Sequence, Set


def check_valid_subset(testcase, words: Sequence[str], chosen: Set[str]) -> None:
    testcase.assertTrue(chosen.issubset(set(words)),
                        msg="Chosen subset must come from input words")

    taken: set[str] = set()
    for w in chosen:
        testcase.assertEqual(
            len(w),
            len(set(w)),
            msg=f"Word {w!r} contains duplicate characters within itself",
        )
        for ch in w:
            testcase.assertNotIn(
                ch,
                taken,
                msg=f"Character {ch!r} is reused across selected words",
            )
            taken.add(ch)


def tally_distinct_chars(chosen: Set[str]) -> int:
    taken: set[str] = set()
    for w in chosen:
        taken |= set(w)
    return len(taken)
