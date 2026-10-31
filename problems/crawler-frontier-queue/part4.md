## Part 4: Retry after failure

Implement `requeue_after_failure(task, now, cooldown, penalty=1) -> CrawlTask`: put a failed task back with the same id and URL, `attempt + 1`, priority lowered by `penalty`, available at `now + cooldown`, and a new sequence number.

Tests: `tests/test_part4_requeue_failure.py`
