import math
import re
from collections import Counter
from datetime import datetime

METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}
LATENCY = re.compile(r"(\d+)ms")


def parse_ts(s):
    if not s.endswith("Z"):
        raise ValueError(s)
    return datetime.fromisoformat(s[:-1] + "+00:00")


class LogAnalyzer:
    def __init__(self):
        self.entries = []  # (ts, method, path, status, latency)
        self.malformed = 0

    def add(self, line):
        parts = line.split()
        try:
            if len(parts) != 5:
                raise ValueError
            ts, method, path, status, latency = parts
            ts = parse_ts(ts)
            status = int(status)
            m = LATENCY.fullmatch(latency)
            if method not in METHODS or not path.startswith("/") or not 100 <= status <= 599 or not m:
                raise ValueError
        except ValueError:
            self.malformed += 1
            return False
        self.entries.append((ts, method, path.split("?", 1)[0], status, int(m.group(1))))
        return True

    def count_by_status(self):
        return dict(Counter(e[3] for e in self.entries))

    def top_paths(self, n):
        counts = Counter(e[2] for e in self.entries)
        return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]

    def p95_latency(self, path_prefix=""):
        lat = sorted(e[4] for e in self.entries if e[2].startswith(path_prefix))
        if not lat:
            return None
        return lat[math.ceil(0.95 * len(lat)) - 1]

    def errors_per_minute(self, start, end):
        lo, hi = parse_ts(start), parse_ts(end)
        out = Counter(e[0].strftime("%Y-%m-%dT%H:%M") for e in self.entries if e[3] >= 500 and lo <= e[0] < hi)
        return dict(out)
