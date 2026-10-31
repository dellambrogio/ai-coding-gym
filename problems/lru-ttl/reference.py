import heapq
import time
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity, clock=time.monotonic):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.capacity = capacity
        self.clock = clock
        self.data = OrderedDict()  # key -> (value, expires_at or None)
        self.expiries = []  # min-heap of (expires_at, key); stale items skipped

    def _expired(self, expires_at):
        return expires_at is not None and self.clock() >= expires_at

    def get(self, key):
        if key not in self.data:
            return None
        value, exp = self.data[key]
        if self._expired(exp):
            del self.data[key]
            return None
        self.data.move_to_end(key)
        return value

    def put(self, key, value, ttl=None):
        if ttl is not None and ttl <= 0:
            raise ValueError("ttl must be > 0")
        exp = None if ttl is None else self.clock() + ttl
        if key in self.data:
            self.data[key] = (value, exp)
            self.data.move_to_end(key)
            if exp is not None:
                heapq.heappush(self.expiries, (exp, key))
            return
        if len(self.data) >= self.capacity:
            while self.expiries and self.expiries[0][0] <= self.clock():
                e, k = heapq.heappop(self.expiries)
                if k in self.data and self.data[k][1] == e:
                    del self.data[k]
            if len(self.data) >= self.capacity:
                self.data.popitem(last=False)
        self.data[key] = (value, exp)
        if exp is not None:
            heapq.heappush(self.expiries, (exp, key))

    def delete(self, key):
        if key not in self.data:
            return False
        _, exp = self.data.pop(key)
        return not self._expired(exp)

    def __len__(self):
        return sum(1 for _, e in self.data.values() if not self._expired(e))
