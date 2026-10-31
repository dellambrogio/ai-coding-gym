## Part 4: Better strategy

Implement `choose_best_outcome(visible, reserve)`: return a legal triple that leads to the highest final score, looking ahead at future picks and refills (the reserve order is known). Return `None` if there is no legal triple. It must never score worse than `choose_first_valid` from the same state. Search is fine at the test sizes; say how it would scale to a full round.

Tests: `tests/test_part4_improved_strategy.py`
