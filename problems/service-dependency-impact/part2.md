## Part 2: Direct impact

Implement `find_directly_affected_services(spec, deleted_paths)`: the sorted ids of services that read from or write to exactly one of the deleted paths (after normalization). `spec` maps a service id to `{"reads_from": [...], "writes_to": [...]}`.

Tests: `tests/test_part2_direct_impact.py`
