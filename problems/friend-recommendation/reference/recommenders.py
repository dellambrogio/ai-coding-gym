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
        if candidate == target_user:
            return False
        if candidate in seen:
            return False
        if candidate in target.connections:
            return False
        seen.add(candidate)

    return True


def _candidates(network: Network, target_user: str) -> list[str]:
    return [u for u in network.all_user_ids() if is_valid_suggestion(network, target_user, [u])]


def pick_random_suggestion(
    network: Network,
    target_user: str,
    rng: random.Random | None = None,
) -> Optional[str]:
    candidates = _candidates(network, target_user)
    if not candidates:
        return None
    return (rng or random.Random()).choice(candidates)


def recommendation_score(
    network: Network,
    target_user: str,
    candidate_user: str,
) -> int:
    if not is_valid_suggestion(network, target_user, [candidate_user]):
        return 0
    mine = network.get_person(target_user).connections
    theirs = network.get_person(candidate_user).connections
    return len(mine & theirs)


def pick_best_suggestion(
    network: Network,
    target_user: str,
) -> Optional[str]:
    candidates = _candidates(network, target_user)
    if not candidates:
        return None
    return min(candidates, key=lambda u: (-recommendation_score(network, target_user, u), u))
