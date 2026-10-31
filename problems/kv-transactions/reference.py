from collections import Counter

_MISSING = object()


class KVStore:
    def __init__(self):
        self.data = {}
        self.counts = Counter()
        self.undo = []  # stack of dicts: key -> previous value (or _MISSING)

    def _write(self, key, value):
        old = self.data.get(key, _MISSING)
        if self.undo and key not in self.undo[-1]:
            self.undo[-1][key] = old
        if old is not _MISSING:
            self.counts[old] -= 1
        if value is _MISSING:
            self.data.pop(key, None)
        else:
            self.data[key] = value
            self.counts[value] += 1

    def set(self, key, value):
        self._write(key, value)

    def get(self, key):
        return self.data.get(key)

    def delete(self, key):
        if key not in self.data:
            return False
        self._write(key, _MISSING)
        return True

    def count(self, value):
        return self.counts[value]

    def begin(self):
        self.undo.append({})

    def commit(self):
        if not self.undo:
            raise RuntimeError("no transaction")
        top = self.undo.pop()
        if self.undo:
            for k, old in top.items():
                self.undo[-1].setdefault(k, old)

    def rollback(self):
        if not self.undo:
            raise RuntimeError("no transaction")
        top = self.undo.pop()
        for k, old in top.items():
            cur = self.data.get(k, _MISSING)
            if cur is not _MISSING:
                self.counts[cur] -= 1
            if old is _MISSING:
                self.data.pop(k, None)
            else:
                self.data[k] = old
                self.counts[old] += 1

    def keys_with_prefix(self, prefix):
        return sorted(k for k in self.data if k.startswith(prefix))
