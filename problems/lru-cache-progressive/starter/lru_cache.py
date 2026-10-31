from __future__ import annotations

import threading
from typing import Callable, Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class LruCache(Generic[K, V]):
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._values: dict[K, V] = {}
        self._order: list[K] = []

    def _touch(self, key: K) -> None:
        if key in self._order:
            self._order.remove(key)
        self._order.append(key)

    def get(self, key: K, default: V | None = None) -> V | None:
        if key not in self._values:
            return default
        return self._values[key]

    def put(self, key: K, value: V) -> None:
        self._values[key] = value
        self._touch(key)

    def resize(self, new_capacity: int) -> None:
        raise NotImplementedError("resize() not implemented yet.")

    def keys_mru_to_lru(self) -> list[K]:
        return list(reversed(self._order))

    def peek_lru_key(self) -> K | None:
        if not self._order:
            return None
        return self._order[0]


class ThreadSafeLruCache(LruCache[K, V]):
    def __init__(self, capacity: int) -> None:
        super().__init__(capacity)
        self._lock = threading.Lock()

    def get_or_put(self, key: K, factory: Callable[[], V]) -> V:
        raise NotImplementedError("get_or_put() not implemented yet.")
