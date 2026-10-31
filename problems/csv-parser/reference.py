import re


def parse_csv(text):
    rows, row, field = [], [], []
    in_quotes = dirty = False
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if in_quotes:
            if c == '"':
                if i + 1 < n and text[i + 1] == '"':
                    field.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                field.append(c)
        elif c == '"' and not field:
            in_quotes = dirty = True
        elif c == ",":
            row.append("".join(field))
            field, dirty = [], True
        elif c == "\n" or (c == "\r" and i + 1 < n and text[i + 1] == "\n"):
            if c == "\r":
                i += 1
            if dirty or field:
                row.append("".join(field))
                rows.append(row)
            row, field, dirty = [], [], False
        else:
            field.append(c)
            dirty = True
        i += 1
    if in_quotes:
        raise ValueError("unterminated quoted field")
    if dirty or field:
        row.append("".join(field))
        rows.append(row)
    return rows


def convert(v):
    if v == "":
        return None
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d*\.\d+", v):
        return float(v)
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    return v


def read_records(text):
    rows = parse_csv(text)
    if not rows:
        return []
    header = rows[0]
    if len(set(header)) != len(header):
        raise ValueError("duplicate header")
    out = []
    for r in rows[1:]:
        if len(r) != len(header):
            raise ValueError("wrong number of fields")
        out.append({h: convert(v) for h, v in zip(header, r)})
    return out


OPS = {
    "sum": lambda xs: sum(xs),
    "count": len,
    "avg": lambda xs: sum(xs) / len(xs) if xs else None,
    "min": lambda xs: min(xs) if xs else None,
    "max": lambda xs: max(xs) if xs else None,
}


def group_by(records, key, aggs):
    for op in aggs.values():
        if op not in OPS:
            raise ValueError(f"unknown op {op}")
    groups = {}
    for r in records:
        if r.get(key) is not None:
            groups.setdefault(r[key], []).append(r)
    out = []
    for k in sorted(groups):
        row = {key: k}
        for col, op in aggs.items():
            row[f"{col}_{op}"] = OPS[op]([r[col] for r in groups[k] if r.get(col) is not None])
        out.append(row)
    return out
