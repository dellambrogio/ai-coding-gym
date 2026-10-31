## Part 1: Legal picks

A solitaire card game: 36 cards (values 1-9 in four marks), 16 face up. Each turn the player picks three face-up cards that sum to 15; they're removed, the player scores 15 points, and the table is refilled from the reserve. The round ends when no triple sums to 15. Clearing all 36 cards scores 180 (`PERFECT_SCORE`).

`engine.is_legal_pick(visible, picked)` accepts picks it shouldn't. A pick is legal only if it has three distinct cards that are all on the table and sum to 15. Fix it.

Tests: `tests/test_part1_legality.py`
