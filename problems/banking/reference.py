class Bank:
    def __init__(self):
        self.bal = {}
        self.spent = {}
        self.frozen = set()

    @staticmethod
    def _check(amount):
        if amount <= 0:
            raise ValueError("amount must be > 0")

    def _usable(self, *ids):
        return all(i in self.bal and i not in self.frozen for i in ids)

    def create_account(self, account_id):
        if account_id in self.bal:
            return False
        self.bal[account_id] = 0
        self.spent[account_id] = 0
        return True

    def get_balance(self, account_id):
        return self.bal.get(account_id)

    def deposit(self, account_id, amount):
        self._check(amount)
        if not self._usable(account_id):
            return None
        self.bal[account_id] += amount
        return self.bal[account_id]

    def withdraw(self, account_id, amount):
        self._check(amount)
        if not self._usable(account_id) or self.bal[account_id] < amount:
            return None
        self.bal[account_id] -= amount
        self.spent[account_id] += amount
        return self.bal[account_id]

    def transfer(self, src, dst, amount):
        self._check(amount)
        if src == dst or not self._usable(src, dst) or self.bal[src] < amount:
            return None
        self.bal[src] -= amount
        self.bal[dst] += amount
        self.spent[src] += amount
        return self.bal[src]

    def top_spenders(self, n):
        return sorted(self.spent.items(), key=lambda kv: (-kv[1], kv[0]))[:n]

    def merge_accounts(self, target, source):
        if target == source or not self._usable(target, source):
            return False
        self.bal[target] += self.bal.pop(source)
        self.spent[target] += self.spent.pop(source)
        return True

    def freeze(self, account_id):
        if account_id not in self.bal:
            return False
        self.frozen.add(account_id)
        return True

    def unfreeze(self, account_id):
        if account_id not in self.bal:
            return False
        self.frozen.discard(account_id)
        return True
