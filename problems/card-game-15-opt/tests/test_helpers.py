from __future__ import annotations

from pieces import Mark, Piece


def p(amount: int, mark: Mark) -> Piece:
    return Piece(amount, mark)
