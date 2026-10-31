from __future__ import annotations

import os


def case_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), "data", filename)
