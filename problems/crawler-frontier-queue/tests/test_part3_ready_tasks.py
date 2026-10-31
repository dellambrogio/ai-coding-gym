from __future__ import annotations

import unittest

from crawl_queue import CrawlQueue


class TestPart3ReadyTasks(unittest.TestCase):
    def test_pop_ready_skips_unready_root(self):
        queue = CrawlQueue()
        queue.push("later", "https://later.example",
                   priority=10, available_at=50)
        queue.push("ready", "https://ready.example",
                   priority=5, available_at=0)

        self.assertEqual(queue.pop_ready(0).task_id, "ready")
        self.assertEqual(queue.next_ready_time(), 50)

    def test_returns_none_when_nothing_is_ready(self):
        queue = CrawlQueue()
        queue.push("later", "https://later.example",
                   priority=10, available_at=50)
        self.assertIsNone(queue.pop_ready(10))
        self.assertEqual(queue.next_ready_time(), 50)


if __name__ == "__main__":
    unittest.main()
