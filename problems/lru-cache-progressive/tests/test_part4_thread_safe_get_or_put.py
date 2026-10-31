from __future__ import annotations

import threading
import time
import unittest

from lru_cache import ThreadSafeLruCache


class TestPart4ThreadSafeGetOrPut(unittest.TestCase):
    def test_factory_runs_once_for_concurrent_miss(self):
        cache = ThreadSafeLruCache[str, str](capacity=2)
        calls = {"count": 0}
        results: list[str] = []

        def factory() -> str:
            calls["count"] += 1
            time.sleep(0.01)
            return "value"

        def worker() -> None:
            results.append(cache.get_or_put("token", factory))

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(calls["count"], 1)
        self.assertEqual(results, ["value"] * 5)
        self.assertEqual(cache.keys_mru_to_lru(), ["token"])


if __name__ == "__main__":
    unittest.main()
