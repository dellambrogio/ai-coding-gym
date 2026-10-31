## Part 1: Paths

Services read from and write to storage paths such as `/warehouse/raw/orders`. Before deleting paths, we want to know which services break.

`path_utils.normalize_path` should produce a canonical path (leading `/`, no repeated or trailing slash), but it turns the root `/` into an empty string. Fix it, and check `is_same_or_ancestor`.

Tests: `tests/test_part1_path_normalization.py`
