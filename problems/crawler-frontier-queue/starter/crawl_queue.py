from __future__ import annotations

from heap_utils import CrawlTask, higher_priority, sift_down, sift_up


class CrawlQueue:
    def __init__(self) -> None:
        self._heap: list[CrawlTask] = []
        self._next_sequence = 0

    def size(self) -> int:
        return len(self._heap)

    def push(self, task_id: str, url: str, priority: int, available_at: int = 0) -> CrawlTask:
        raise NotImplementedError("push() not implemented yet.")

    def pop(self) -> CrawlTask | None:
        raise NotImplementedError("pop() not implemented yet.")

    def _remove_at(self, index: int) -> CrawlTask:
        removed = self._heap[index]
        last = self._heap.pop()
        if index < len(self._heap):
            self._heap[index] = last
            parent = (index - 1) // 2
            if index > 0 and higher_priority(self._heap[index], self._heap[parent]):
                sift_up(self._heap, index)
            else:
                sift_down(self._heap, index)
        return removed

    def pop_ready(self, now: int) -> CrawlTask | None:
        raise NotImplementedError("pop_ready() not implemented yet.")

    def next_ready_time(self) -> int | None:
        raise NotImplementedError("next_ready_time() not implemented yet.")

    def requeue_after_failure(
        self,
        task: CrawlTask,
        now: int,
        cooldown: int,
        penalty: int = 1,
    ) -> CrawlTask:
        raise NotImplementedError(
            "requeue_after_failure() not implemented yet.")
