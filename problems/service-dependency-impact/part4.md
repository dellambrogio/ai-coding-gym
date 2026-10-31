## Part 4: Propagation

Implement `build_impact_chains(spec, deleted_paths)`: for each deleted path (normalized), list the affected services: first the services that use the deleted subtree (sorted), then the services that read what an affected service writes, level by level (each level sorted), each service once. `build_dependency_graph` gives writer -> reader edges.

Tests: `tests/test_part4_propagation.py`
