import math
import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self, limit, window, clock=time.monotonic):
        if limit < 1 or window <= 0:
            raise ValueError("limit must be >= 1 and window > 0")
        self.limit = limit
        self.window = window
        self.clock = clock
        self.limits = {}
        self.log = defaultdict(deque)  # client -> deque[(ts, cost)]
        self.used = defaultdict(int)

    def _prune(self, client, now):
        q = self.log[client]
        while q and q[0][0] <= now - self.window:
            self.used[client] -= q.popleft()[1]

    def _limit(self, client):
        return self.limits.get(client, self.limit)

    def set_limit(self, client, limit):
        if limit < 1:
            raise ValueError("limit must be >= 1")
        self.limits[client] = limit

    def allow(self, client, cost=1):
        if cost < 1:
            raise ValueError("cost must be >= 1")
        now = self.clock()
        self._prune(client, now)
        if self.used[client] + cost > self._limit(client):
            return False
        self.log[client].append((now, cost))
        self.used[client] += cost
        return True

    def retry_after(self, client, cost=1):
        if cost < 1:
            raise ValueError("cost must be >= 1")
        limit = self._limit(client)
        if cost > limit:
            return math.inf
        now = self.clock()
        self._prune(client, now)
        used = self.used[client]
        if used + cost <= limit:
            return 0
        for ts, c in self.log[client]:
            used -= c
            if used + cost <= limit:
                return ts + self.window - now
        return 0
