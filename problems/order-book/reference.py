import heapq
import itertools
from collections import defaultdict


class OrderBook:
    def __init__(self):
        self.heaps = {"buy": [], "sell": []}  # buy: (-price, id), sell: (price, id)
        self.orders = {}  # id -> [side, price, qty] (resting only)
        self.ids = itertools.count(1)

    def _top(self, side):
        h = self.heaps[side]
        while h and h[0][1] not in self.orders:
            heapq.heappop(h)
        return h[0] if h else None

    def best_bid(self):
        t = self._top("buy")
        return -t[0] if t else None

    def best_ask(self):
        t = self._top("sell")
        return t[0] if t else None

    def place(self, side, price, qty):
        if side not in ("buy", "sell"):
            raise ValueError("side must be buy or sell")
        if not isinstance(qty, int) or qty <= 0 or (price is not None and (not isinstance(price, int) or price <= 0)):
            raise ValueError("price and qty must be positive integers")
        oid = next(self.ids)
        other = "sell" if side == "buy" else "buy"
        trades = []
        while qty > 0:
            top = self._top(other)
            if not top:
                break
            rid = top[1]
            rprice = self.orders[rid][1]
            if price is not None and (rprice > price if side == "buy" else rprice < price):
                break
            fill = min(qty, self.orders[rid][2])
            trades.append((oid, rid, rprice, fill) if side == "buy" else (rid, oid, rprice, fill))
            qty -= fill
            self.orders[rid][2] -= fill
            if self.orders[rid][2] == 0:
                del self.orders[rid]
        if qty > 0 and price is not None:
            self.orders[oid] = [side, price, qty]
            heapq.heappush(self.heaps[side], (-price if side == "buy" else price, oid))
        return oid, trades

    def cancel(self, order_id):
        return self.orders.pop(order_id, None) is not None

    def depth(self, side, levels):
        agg = defaultdict(int)
        for s, p, q in self.orders.values():
            if s == side:
                agg[p] += q
        return sorted(agg.items(), reverse=(side == "buy"))[:levels]
