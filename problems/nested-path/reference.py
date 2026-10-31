import re

TOKEN = re.compile(r"(\.)?([A-Za-z_][A-Za-z0-9_]*|\*)|\[(-?\d+|\*)\]")
MISSING = object()


def parse(path, wildcards=False):
    tokens, pos = [], 0
    while pos < len(path):
        m = TOKEN.match(path, pos)
        if not m:
            raise ValueError(f"invalid path: {path!r}")
        dot, key, idx = m.groups()
        if key is not None and bool(dot) == (pos == 0):
            raise ValueError(f"invalid path: {path!r}")
        if key is not None:
            tokens.append(("key", None if key == "*" else key))
        else:
            tokens.append(("idx", None if idx == "*" else int(idx)))
        pos = m.end()
    if not wildcards and any(v is None for _, v in tokens):
        raise ValueError("wildcards not allowed here")
    return tokens


def _step(node, kind, v):
    if kind == "key":
        return node.get(v, MISSING) if isinstance(node, dict) else MISSING
    if isinstance(node, list) and -len(node) <= v < len(node):
        return node[v]
    return MISSING


def get(data, path, default=None):
    node = data
    for kind, v in parse(path):
        node = _step(node, kind, v)
        if node is MISSING:
            return default
    return node


def set_path(data, path, value):
    tokens = parse(path)
    if not tokens:
        raise ValueError("empty path")
    node = data
    for i, (kind, v) in enumerate(tokens):
        last = i == len(tokens) - 1
        new = value if last else ([] if tokens[i + 1][0] == "idx" else {})
        if kind == "key":
            if not isinstance(node, dict):
                raise TypeError(f"key {v!r} on {type(node).__name__}")
            if last or v not in node:
                node[v] = new
            node = node[v]
        else:
            if not isinstance(node, list):
                raise TypeError(f"index {v} on {type(node).__name__}")
            if v == len(node):
                node.append(new)
            elif -len(node) <= v < len(node):
                if last:
                    node[v] = new
            else:
                raise IndexError(v)
            node = node[v]


def get_all(data, path):
    nodes = [data]
    for kind, v in parse(path, wildcards=True):
        nxt = []
        for n in nodes:
            if v is None:
                if kind == "key" and isinstance(n, dict):
                    nxt.extend(n.values())
                elif kind == "idx" and isinstance(n, list):
                    nxt.extend(n)
            else:
                r = _step(n, kind, v)
                if r is not MISSING:
                    nxt.append(r)
        nodes = nxt
    return nodes
