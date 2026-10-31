## Part 3: Evaluate a strategy

Implement `count_perfect_finishes(chooser, attempts=100, first_seed=0)`: play `attempts` rounds with `engine.play_round(chooser, seed=s)` for seeds `first_seed, first_seed + 1, ...` and return how many rounds scored `PERFECT_SCORE`. Call `play_round` through the name imported in `strategies.py`, so tests can replace it.

Tests: `tests/test_part3_evaluation.py`
