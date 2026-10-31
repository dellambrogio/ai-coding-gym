import bisect

AGGS = {
    "sum": lambda xs: sum(xs),
    "count": len,
    "avg": lambda xs: sum(xs) / len(xs) if xs else None,
    "min": lambda xs: min(xs) if xs else None,
    "max": lambda xs: max(xs) if xs else None,
}


class Metrics:
    def __init__(self, retention=None):
        self.retention = retention
        self.series = {}  # name -> (sorted timestamps, values in the same order)
        self.latest = {}

    def record(self, name, ts, value):
        times, values = self.series.setdefault(name, ([], []))
        if self.retention is not None:
            latest = max(self.latest.get(name, ts), ts)
            self.latest[name] = latest
            cutoff = latest - self.retention
            if ts < cutoff:
                return False
            drop = bisect.bisect_left(times, cutoff)
            del times[:drop], values[:drop]
        i = bisect.bisect_right(times, ts)
        times.insert(i, ts)
        values.insert(i, value)
        return True

    def _values(self, name, start, end):
        times, values = self.series.get(name, ([], []))
        return values[bisect.bisect_left(times, start):bisect.bisect_left(times, end)]

    def query(self, name, start, end, agg):
        if agg not in AGGS:
            raise ValueError(f"unknown agg {agg}")
        return AGGS[agg](self._values(name, start, end))

    def downsample(self, name, start, end, step, agg):
        if step <= 0 or agg not in AGGS:
            raise ValueError("bad step or agg")
        out = []
        for b in range(start, end, step):
            xs = self._values(name, b, min(b + step, end))
            if xs:
                out.append((b, AGGS[agg](xs)))
        return out
