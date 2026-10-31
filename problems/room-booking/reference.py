class Calendar:
    def __init__(self, rooms=1):
        if rooms < 1:
            raise ValueError("rooms must be >= 1")
        self.rooms = rooms
        self.bookings = []

    def _max_overlap(self, bookings, lo, hi):
        events = []
        for s, e in bookings:
            if s < hi and lo < e:
                events += [(max(s, lo), 1), (min(e, hi), -1)]
        events.sort()  # at equal times, ends (-1) come before starts
        cur = best = 0
        for _, d in events:
            cur += d
            best = max(best, cur)
        return best

    def book(self, start, end):
        if start >= end:
            raise ValueError("start must be < end")
        if self._max_overlap(self.bookings + [(start, end)], start, end) > self.rooms:
            return False
        self.bookings.append((start, end))
        return True

    def cancel(self, start, end):
        if (start, end) in self.bookings:
            self.bookings.remove((start, end))
            return True
        return False

    def free_slots(self, day_start, day_end, min_length=1):
        points = sorted({day_start, day_end, *(t for b in self.bookings for t in b if day_start < t < day_end)})
        slots = []
        for a, b in zip(points, points[1:]):
            busy = sum(1 for s, e in self.bookings if s <= a and b <= e)
            if busy < self.rooms:
                if slots and slots[-1][1] == a:
                    slots[-1] = (slots[-1][0], b)
                else:
                    slots.append((a, b))
        return [s for s in slots if s[1] - s[0] >= min_length]
