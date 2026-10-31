## Part 4: Thread-safe get-or-put

Implement `ThreadSafeLruCache.get_or_put(key, factory)`: return the cached value, or call `factory()`, store and return its result. When several threads miss the same key at once, `factory` must run only once and every thread gets the same value.

Tests: `tests/test_part4_thread_safe_get_or_put.py`
