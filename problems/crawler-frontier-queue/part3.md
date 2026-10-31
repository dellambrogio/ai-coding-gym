## Part 3: Ready tasks

A task can't be fetched before its `available_at` time. Implement `pop_ready(now)`: remove and return the best task with `available_at <= now`, even if a better task that isn't ready sits at the root; `None` if nothing is ready. Implement `next_ready_time()`: the smallest `available_at` in the queue, or `None` if it's empty. `_remove_at(index)` may help.

Tests: `tests/test_part3_ready_tasks.py`
