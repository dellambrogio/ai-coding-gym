import heapq


class TaskGraph:
    def __init__(self):
        self.deps = {}
        self.duration = {}

    def add_task(self, name, deps=(), duration=1):
        if name in self.deps:
            raise ValueError(f"duplicate task {name}")
        if duration < 0:
            raise ValueError("duration must be >= 0")
        self.deps[name] = list(deps)
        self.duration[name] = duration

    def _check(self):
        for ds in self.deps.values():
            for d in ds:
                if d not in self.deps:
                    raise KeyError(d)

    def order(self):
        self._check()
        indeg = {t: len(set(ds)) for t, ds in self.deps.items()}
        users = {t: [] for t in self.deps}
        for t, ds in self.deps.items():
            for d in set(ds):
                users[d].append(t)
        ready = [t for t, n in indeg.items() if n == 0]
        heapq.heapify(ready)
        out = []
        while ready:
            t = heapq.heappop(ready)
            out.append(t)
            for u in users[t]:
                indeg[u] -= 1
                if indeg[u] == 0:
                    heapq.heappush(ready, u)
        if len(out) != len(self.deps):
            raise ValueError("cycle")
        return out

    def find_cycle(self):
        self._check()
        state, stack = {}, []

        def dfs(t):
            state[t] = 1
            stack.append(t)
            for d in self.deps[t]:
                if state.get(d) == 1:
                    return stack[stack.index(d):] + [d]
                if d not in state:
                    found = dfs(d)
                    if found:
                        return found
            state[t] = 2
            stack.pop()
            return None

        for t in sorted(self.deps):
            if t not in state:
                found = dfs(t)
                if found:
                    return found
        return None

    def _starts(self):
        start = {}
        for t in self.order():
            start[t] = max((start[d] + self.duration[d] for d in self.deps[t]), default=0)
        return start

    def earliest_start(self, name):
        return self._starts()[name]

    def total_time(self):
        start = self._starts()
        return max((start[t] + self.duration[t] for t in start), default=0)
