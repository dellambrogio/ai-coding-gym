## Part 3: Subtree impact

Implement `find_tree_affected_services(spec, deleted_paths)`: deleting a path also deletes everything under it, so a service is affected if it uses a deleted path or a descendant of one. Return sorted ids.

Tests: `tests/test_part3_tree_impact.py`
