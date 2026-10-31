from __future__ import annotations


def normalize_path(path: str) -> str:
    raw = path.strip()
    if not raw:
        return "/"
    if not raw.startswith("/"):
        raw = "/" + raw
    while "//" in raw:
        raw = raw.replace("//", "/")
    if raw.endswith("/"):
        raw = raw[:-1]
    return raw


def is_same_or_ancestor(ancestor: str, path: str) -> bool:
    normalized_ancestor = normalize_path(ancestor)
    normalized_path = normalize_path(path)

    if normalized_ancestor == normalized_path:
        return True

    if normalized_ancestor == "/":
        return normalized_path.startswith("/")

    return normalized_path.startswith(normalized_ancestor + "/")
