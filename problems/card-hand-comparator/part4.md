## Part 4: Extensible evaluators

Implement `compare_with_evaluators(hand1, hand2, evaluators)`: compare hands using any list of `HandCategoryEvaluator`s, so a new category (e.g. "all red cards" with `category_rank = 100`) can be added without changing the comparator. A hand's score is the best score among the evaluators that match it.

Tests: `tests/test_part4_extensible_design.py`
