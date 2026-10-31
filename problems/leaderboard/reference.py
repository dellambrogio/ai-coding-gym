import bisect


class Leaderboard:
    def __init__(self):
        self.scores = {}
        self.order = []  # sorted list of (-score, player)

    def add_score(self, player, points):
        if points <= 0:
            raise ValueError("points must be > 0")
        old = self.scores.get(player)
        if old is not None:
            del self.order[bisect.bisect_left(self.order, (-old, player))]
        new = (old or 0) + points
        self.scores[player] = new
        bisect.insort(self.order, (-new, player))

    def score(self, player):
        return self.scores.get(player, 0)

    def top(self, k):
        return [(p, -s) for s, p in self.order[:k]]

    def rank(self, player):
        if player not in self.scores:
            return None
        return bisect.bisect_left(self.order, -self.scores[player], key=lambda x: x[0]) + 1

    def reset(self, player):
        if player not in self.scores:
            return False
        del self.order[bisect.bisect_left(self.order, (-self.scores.pop(player), player))]
        return True

    def count_in_range(self, lo, hi):
        key = lambda x: x[0]
        return max(0, bisect.bisect_right(self.order, -lo, key=key) - bisect.bisect_left(self.order, -hi, key=key))
