from __future__ import annotations

import unittest

from lru_cache import LruCache


class TestPart3Resize(unittest.TestCase):
    def test_shrinking_cache_keeps_most_recent_entries(self):
        cache = LruCache[str, int](capacity=4)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.put("d", 4)
        cache.get("b")
        cache.get("d")

        cache.resize(2)

        self.assertEqual(cache.keys_mru_to_lru(), ["d", "b"])
        self.assertIsNone(cache.get("a"))
        self.assertIsNone(cache.get("c"))

    def test_rejects_invalid_capacity(self):
        cache = LruCache[str, int](capacity=2)
        with self.assertRaises(ValueError):
            cache.resize(0)


if __name__ == "__main__":
    unittest.main()
