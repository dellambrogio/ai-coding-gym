## Part 1: Validate suggestions

A social network (`social_graph.py`) where friendships are undirected. `recommenders.py` suggests new friends.

`is_valid_suggestion(network, target, suggested)` is true when the target exists and every suggestion is an existing user who is not the target, not already a friend, and not repeated. One of these checks is missing: fix it.

Tests: `tests/test_part1_validation.py`
