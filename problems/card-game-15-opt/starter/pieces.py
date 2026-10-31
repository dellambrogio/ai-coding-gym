from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Mark(Enum):
    SUN = "sun"
    MOON = "moon"
    STAR = "star"
    CLOUD = "cloud"


@dataclass(frozen=True)
class Piece:
    amount: int
    mark: Mark

    def __post_init__(self) -> None:
        if not 1 <= self.amount <= 9:
            raise ValueError("amount must be between 1 and 9 inclusive")
