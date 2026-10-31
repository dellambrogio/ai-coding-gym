class Splitter:
    def __init__(self):
        self.bal = {}

    def _add(self, name, delta):
        self.bal[name] = self.bal.get(name, 0) + delta

    def add_expense(self, payer, amount, participants, shares=None):
        if amount <= 0 or not participants or len(set(participants)) != len(participants):
            raise ValueError("invalid expense")
        if shares is None:
            shares = [1] * len(participants)
        if len(shares) != len(participants) or any(s <= 0 for s in shares):
            raise ValueError("invalid shares")
        total = sum(shares)
        owed = {p: amount * s // total for p, s in zip(participants, shares)}
        leftover = amount - sum(owed.values())
        order = sorted(zip(participants, shares), key=lambda ps: (-(amount * ps[1] % total), ps[0]))
        for p, _ in order[:leftover]:
            owed[p] += 1
        self._add(payer, amount)
        for p, o in owed.items():
            self._add(p, -o)

    def add_payment(self, sender, receiver, amount):
        if amount <= 0 or sender == receiver:
            raise ValueError("invalid payment")
        self._add(sender, amount)
        self._add(receiver, -amount)

    def balances(self):
        return dict(self.bal)

    def settle(self):
        bal = {k: v for k, v in self.bal.items() if v}
        out = []
        while bal:
            debtor = min(bal, key=lambda k: (bal[k], k))
            creditor = min(bal, key=lambda k: (-bal[k], k))
            amt = min(-bal[debtor], bal[creditor])
            out.append((debtor, creditor, amt))
            for k, d in ((debtor, amt), (creditor, -amt)):
                bal[k] += d
                if not bal[k]:
                    del bal[k]
        return out
