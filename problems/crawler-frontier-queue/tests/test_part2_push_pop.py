from __future__ import annotations

import unittest

from crawl_queue import CrawlQueue


class TestPart2PushPop(unittest.TestCase):
    def test_pop_returns_highest_priority_first(self):
        queue = CrawlQueue()
        queue.push("low", "https://low.example", priority=1)
        queue.push("high", "https://high.example", priority=5)
        queue.push("mid", "https://mid.example", priority=3)

        self.assertEqual(queue.pop().task_id, "high")
        self.assertEqual(queue.pop().task_id, "mid")
        self.assertEqual(queue.pop().task_id, "low")
        self.assertIsNone(queue.pop())

    def test_same_priority_uses_insertion_order(self):
        queue = CrawlQueue()
        queue.push("first", "https://1.example", priority=2)
        queue.push("second", "https://2.example", priority=2)

        self.assertEqual(queue.pop().task_id, "first")
        self.assertEqual(queue.pop().task_id, "second")


if __name__ == "__main__":
    unittest.main()
