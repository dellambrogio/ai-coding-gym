## Part 2: Push and pop

Implement `push(task_id, url, priority, available_at=0) -> CrawlTask` (assigns the next sequence number) and `pop() -> CrawlTask | None` (highest priority, then first pushed; `None` when empty), using the heap helpers.

Tests: `tests/test_part2_push_pop.py`
