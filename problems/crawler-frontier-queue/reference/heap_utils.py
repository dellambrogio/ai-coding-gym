from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CrawlTask:
    task_id: str
    url: str
    priority: int
    available_at: int
    sequence: int
    attempt: int = 0


def higher_priority(left: CrawlTask, right: CrawlTask) -> bool:
    if left.priority != right.priority:
        return left.priority > right.priority
    return left.sequence < right.sequence


def sift_up(heap: list[CrawlTask], index: int) -> None:
    child = index
    while child > 0:
        parent = (child - 1) // 2
        if higher_priority(heap[child], heap[parent]):
            heap[child], heap[parent] = heap[parent], heap[child]
            child = parent
        else:
            break


def sift_down(heap: list[CrawlTask], index: int) -> None:
    parent = index
    length = len(heap)

    while True:
        left = 2 * parent + 1
        right = left + 1
        best = parent

        if left < length and higher_priority(heap[left], heap[best]):
            best = left
        if right < length and higher_priority(heap[right], heap[best]):
            best = right

        if best == parent:
            return

        heap[parent], heap[best] = heap[best], heap[parent]
        parent = best
