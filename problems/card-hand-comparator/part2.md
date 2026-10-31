## Part 2: Compare complete hands

Implement `build_default_evaluators()`, `score_hand(hand, evaluators=None)` and `compare_hands(hand1, hand2)` for 5-card hands. Return `PLAYER1`, `PLAYER2` or `TIE`.

Categories, from strongest: four of a kind, full house, three of a kind, two pair, one pair, high card (no straights or flushes). A higher category wins; within a category, compare the tuple each evaluator returns (e.g. pair rank, then kickers). Identical scores are a tie.

Tests: `tests/test_part2_complete_hands.py`
