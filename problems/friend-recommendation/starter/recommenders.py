from __future__ import annotations

import random
from typing import Optional

from social_graph import Network


def is_valid_suggestion(network: Network, target_user: str, suggested_users: list[str]) -> bool:
    if not network.has_user(target_user):
        return False

    target = network.get_person(target_user)
    seen: set[str] = set()

    for candidate in suggested_users:
        if not network.has_user(candidate):
            return False
        if candidate in seen:
            return False
        if candidate in target.connections:
            return False
        seen.add(candidate)

    return True


def pick_random_suggestion(
    network: Network,
    target_user: str,
    rng: random.Random | None = None,
) -> Optional[str]:
    raise NotImplementedError("pick_random_suggestion() not implemented yet.")


def recommendation_score(
    network: Network,
    target_user: str,
    candidate_user: str,
) -> int:
    raise NotImplementedError("recommendation_score() not implemented yet.")


def pick_best_suggestion(
    network: Network,
    target_user: str,
) -> Optional[str]:
    raise NotImplementedError("pick_best_suggestion() not implemented yet.")
