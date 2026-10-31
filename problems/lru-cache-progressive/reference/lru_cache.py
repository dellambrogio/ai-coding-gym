from __future__ import annotations

import threading
from collections import OrderedDict
from typing import Callable, Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class LruCache(Generic[K, V]):
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._values: OrderedDict[K, V] = OrderedDict()  # LRU first

    def get(self, key: K, default: V | None = None) -> V | None:
        if key not in self._values:
            return default
        self._values.move_to_end(key)
        return self._values[key]

    def put(self, key: K, value: V) -> None:
        self._values[key] = value
        self._values.move_to_end(key)
        self._evict()

    def resize(self, new_capacity: int) -> None:
        if new_capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = new_capacity
        self._evict()

    def _evict(self) -> None:
        while len(self._values) > self.capacity:
            self._values.popitem(last=False)

    def keys_mru_to_lru(self) -> list[K]:
        return list(reversed(self._values))

    def peek_lru_key(self) -> K | None:
        return next(iter(self._values), None)


class ThreadSafeLruCache(LruCache[K, V]):
    def __init__(self, capacity: int) -> None:
        super().__init__(capacity)
        self._lock = threading.RLock()

    def get(self, key: K, default: V | None = None) -> V | None:
        with self._lock:
            return super().get(key, default)

    def put(self, key: K, value: V) -> None:
        with self._lock:
            super().put(key, value)

    def resize(self, new_capacity: int) -> None:
        with self._lock:
            super().resize(new_capacity)

    def get_or_put(self, key: K, factory: Callable[[], V]) -> V:
        with self._lock:
            if key in self._values:
                return super().get(key)
            value = factory()
            super().put(key, value)
            return value
