import re

CELL = re.compile(r"[A-Z](?:[1-9]|[1-9][0-9])")
TOKEN = re.compile(r"\s*(?:(\d+(?:\.\d+)?|\.\d+)|([A-Z][0-9]+(?::[A-Z][0-9]+)?)|(SUM|MIN|MAX)|([-+*/(),]))")


def check_cell(cell):
    if not isinstance(cell, str) or not CELL.fullmatch(cell):
        raise ValueError(f"invalid cell {cell!r}")


def expand(a, b):
    check_cell(a)
    check_cell(b)
    c1, c2 = sorted((a[0], b[0]))
    r1, r2 = sorted((int(a[1:]), int(b[1:])))
    return [f"{chr(c)}{r}" for c in range(ord(c1), ord(c2) + 1) for r in range(r1, r2 + 1)]


def flatten(args):
    for a in args:
        if isinstance(a, list):
            yield from a
        else:
            yield a


def sort_key(cell):
    return cell[0], int(cell[1:])


class Sheet:
    def __init__(self):
        self.cells = {}  # cell -> (value or None, compiled code or None, set of referenced cells)

    def _compile(self, formula):
        expr, pos, py, refs = formula[1:], 0, [], set()
        while pos < len(expr):
            m = TOKEN.match(expr, pos)
            if not m or m.end() == pos:
                if expr[pos:].strip() == "":
                    break
                raise ValueError(f"invalid formula {formula!r}")
            num, ref, func, op = m.groups()
            if num:
                py.append(num)
            elif ref:
                if ":" in ref:
                    cells = expand(*ref.split(":"))
                    refs.update(cells)
                    py.append(f"_r({cells!r})")
                else:
                    check_cell(ref)
                    refs.add(ref)
                    py.append(f"_c({ref!r})")
            elif func:
                py.append(func)
            else:
                py.append(op)
            pos = m.end()
        try:
            code = compile(" ".join(py), "<formula>", "eval")
        except SyntaxError:
            raise ValueError(f"invalid formula {formula!r}") from None
        return code, refs

    def _reaches(self, start_refs, target):
        stack, seen = list(start_refs), set()
        while stack:
            c = stack.pop()
            if c == target:
                return True
            if c not in seen:
                seen.add(c)
                stack.extend(self.cells.get(c, (None, None, set()))[2])
        return False

    def set(self, cell, value):
        check_cell(cell)
        if isinstance(value, str) and value.startswith("="):
            code, refs = self._compile(value)
            if self._reaches(refs, cell):
                raise ValueError("circular reference")
            self.cells[cell] = (None, code, refs)
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            self.cells[cell] = (value, None, set())
        else:
            raise ValueError(f"invalid value {value!r}")

    def clear(self, cell):
        check_cell(cell)
        self.cells.pop(cell, None)

    def get(self, cell):
        check_cell(cell)
        if cell not in self.cells:
            return 0
        value, code, _ = self.cells[cell]
        if code is None:
            return value
        env = {
            "_c": self.get,
            "_r": lambda cells: [self.get(c) for c in cells],
            "SUM": lambda *a: sum(flatten(a)),
            "MIN": lambda *a: min(flatten(a)),
            "MAX": lambda *a: max(flatten(a)),
        }
        return eval(code, {"__builtins__": {}}, env)

    def dependents(self, cell):
        check_cell(cell)
        out, stack = set(), [cell]
        while stack:
            c = stack.pop()
            for other, (_, _, refs) in self.cells.items():
                if c in refs and other not in out:
                    out.add(other)
                    stack.append(other)
        return sorted(out, key=sort_key)
