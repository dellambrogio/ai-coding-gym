class Editor:
    def __init__(self):
        self.text = ""
        self.cursor = 0
        self.sel = None
        self.clipboard = ""
        self.undo_stack = []  # (before, after) snapshots of (text, cursor)
        self.redo_stack = []

    def _apply(self, start, end, insert):
        before = (self.text, self.cursor)
        self.text = self.text[:start] + insert + self.text[end:]
        self.cursor = start + len(insert)
        self.sel = None
        self.undo_stack.append((before, (self.text, self.cursor)))
        self.redo_stack.clear()

    def type(self, s):
        if self.sel:
            self._apply(*self.sel, s)
        elif s:
            self._apply(self.cursor, self.cursor, s)

    def backspace(self, n=1):
        if self.sel:
            self._apply(*self.sel, "")
        elif n > 0 and self.cursor > 0:
            self._apply(max(0, self.cursor - n), self.cursor, "")

    def move(self, pos):
        self.cursor = max(0, min(pos, len(self.text)))
        self.sel = None

    def undo(self):
        if not self.undo_stack:
            return False
        before, after = self.undo_stack.pop()
        self.redo_stack.append((before, after))
        self.text, self.cursor = before
        self.sel = None
        return True

    def redo(self):
        if not self.redo_stack:
            return False
        before, after = self.redo_stack.pop()
        self.undo_stack.append((before, after))
        self.text, self.cursor = after
        self.sel = None
        return True

    def select(self, start, end):
        clamp = lambda p: max(0, min(p, len(self.text)))
        a, b = sorted((clamp(start), clamp(end)))
        self.sel = (a, b) if a < b else None
        self.cursor = b

    def copy(self):
        if not self.sel:
            return ""
        self.clipboard = self.text[self.sel[0]:self.sel[1]]
        return self.clipboard

    def cut(self):
        s = self.copy()
        if self.sel:
            self._apply(*self.sel, "")
        return s

    def paste(self):
        self.type(self.clipboard)
