from __future__ import annotations

import unittest

from lru_cache import LruCache


class TestPart1RecencyBug(unittest.TestCase):
    def test_get_refreshes_recently_used_key(self):
        cache = LruCache[str, int](capacity=3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)

        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.keys_mru_to_lru(), ["a", "c", "b"])


if __name__ == "__main__":
    unittest.main()
