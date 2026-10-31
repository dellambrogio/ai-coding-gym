from __future__ import annotations

from dataclasses import replace

from heap_utils import CrawlTask, higher_priority, sift_down, sift_up


class CrawlQueue:
    def __init__(self) -> None:
        self._heap: list[CrawlTask] = []
        self._next_sequence = 0

    def size(self) -> int:
        return len(self._heap)

    def _add(self, task: CrawlTask) -> CrawlTask:
        self._heap.append(task)
        sift_up(self._heap, len(self._heap) - 1)
        return task

    def _sequence(self) -> int:
        self._next_sequence += 1
        return self._next_sequence

    def push(self, task_id: str, url: str, priority: int, available_at: int = 0) -> CrawlTask:
        return self._add(CrawlTask(task_id, url, priority, available_at, self._sequence()))

    def pop(self) -> CrawlTask | None:
        return self._remove_at(0) if self._heap else None

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
        best = None
        for i, task in enumerate(self._heap):
            if task.available_at <= now and (best is None or higher_priority(task, self._heap[best])):
                best = i
        return None if best is None else self._remove_at(best)

    def next_ready_time(self) -> int | None:
        return min((task.available_at for task in self._heap), default=None)

    def requeue_after_failure(
        self,
        task: CrawlTask,
        now: int,
        cooldown: int,
        penalty: int = 1,
    ) -> CrawlTask:
        return self._add(replace(
            task,
            priority=task.priority - penalty,
            available_at=now + cooldown,
            sequence=self._sequence(),
            attempt=task.attempt + 1,
        ))
