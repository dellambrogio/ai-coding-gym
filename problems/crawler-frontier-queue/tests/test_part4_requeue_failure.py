from __future__ import annotations

import unittest

from crawl_queue import CrawlQueue


class TestPart4RequeueFailure(unittest.TestCase):
    def test_requeue_updates_attempt_priority_and_ready_time(self):
        queue = CrawlQueue()
        original = queue.push("page", "https://page.example", priority=4)
        task = queue.pop()

        requeued = queue.requeue_after_failure(
            task, now=10, cooldown=25, penalty=2)

        self.assertEqual(requeued.task_id, original.task_id)
        self.assertEqual(requeued.attempt, 1)
        self.assertEqual(requeued.priority, 2)
        self.assertEqual(requeued.available_at, 35)
        self.assertEqual(queue.next_ready_time(), 35)
        self.assertEqual(queue.pop_ready(35).task_id, "page")


if __name__ == "__main__":
    unittest.main()
