import bisect
import heapq


def _near(prefix, word, typos):
    prev = list(range(len(word) + 1))
    for i, c in enumerate(prefix, 1):
        cur = [i] + [0] * len(word)
        for j, d in enumerate(word, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (c != d))
        prev = cur
    return min(prev) <= typos


class Autocomplete:
    def __init__(self):
        self.score = {}
        self.words = []  # sorted

    def add(self, word, weight=1):
        if weight <= 0:
            raise ValueError("weight must be > 0")
        w = word.lower()
        if w not in self.score:
            bisect.insort(self.words, w)
            self.score[w] = 0
        self.score[w] += weight

    def remove(self, word):
        w = word.lower()
        if w not in self.score:
            return False
        del self.score[w]
        del self.words[bisect.bisect_left(self.words, w)]
        return True

    def suggest(self, prefix, k=5, typos=0):
        p = prefix.lower()
        lo = bisect.bisect_left(self.words, p)
        hi = bisect.bisect_left(self.words, p + "\U0010ffff")
        rank = lambda w: (-self.score[w], w)
        exact = self.words[lo:hi]
        out = heapq.nsmallest(k, exact, key=rank)
        if typos and len(out) < k:
            fuzzy = [w for w in self.words[:lo] + self.words[hi:] if _near(p, w, typos)]
            out += heapq.nsmallest(k - len(out), fuzzy, key=rank)
        return out
