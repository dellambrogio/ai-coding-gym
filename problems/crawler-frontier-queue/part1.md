## Part 1: Tie-break

A web crawler keeps its pending fetches in a priority queue: a hand-written binary max-heap in `heap_utils.py`, used by `CrawlQueue` in `crawl_queue.py`. Each `CrawlTask` has a priority (higher first) and a `sequence` number in push order.

When priorities are equal, the task pushed first must come out first. `higher_priority` gets the tie-break wrong: fix it.

Tests: `tests/test_part1_heap_tiebreak.py`
