## Part 1: Brute force

Given a list of non-empty strings, find one that contains another member of the list (at a different position) as a substring. Matching is case-sensitive, and identical strings at different positions contain each other. The module docstring in `substring_finder.py` has the full contract; `benchmark.py` times the strategies.

Implement `find_contained_string(strings)` by checking every pair: return any valid container, or `None`.

Tests: `tests/test_part1_brute_force.py`
