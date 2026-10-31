from __future__ import annotations

import unittest

from heap_utils import CrawlTask, higher_priority


class TestPart1HeapTieBreak(unittest.TestCase):
    def test_earlier_sequence_wins_when_priority_matches(self):
        earlier = CrawlTask("a", "https://a.example", 10, 0, 1)
        later = CrawlTask("b", "https://b.example", 10, 0, 2)
        self.assertTrue(higher_priority(earlier, later))
        self.assertFalse(higher_priority(later, earlier))


if __name__ == "__main__":
    unittest.main()
