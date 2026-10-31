from __future__ import annotations

import unittest

from lru_cache import LruCache


class TestPart2CapacityEviction(unittest.TestCase):
    def test_evicts_least_recently_used_key(self):
        cache = LruCache[str, int](capacity=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")
        cache.put("c", 3)

        self.assertIsNone(cache.get("b"))
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("c"), 3)

    def test_updating_existing_key_does_not_evict_other_entries(self):
        cache = LruCache[str, int](capacity=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("a", 10)

        self.assertEqual(cache.get("a"), 10)
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.keys_mru_to_lru(), ["b", "a"])


if __name__ == "__main__":
    unittest.main()
