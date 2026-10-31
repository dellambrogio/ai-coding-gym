from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Person:
    user_id: str
    connections: set[str] = field(default_factory=set)

    def connect(self, other_id: str) -> None:
        self.connections.add(other_id)


class Network:
    def __init__(self) -> None:
        self._people: dict[str, Person] = {}

    def add_person(self, user_id: str) -> None:
        if user_id not in self._people:
            self._people[user_id] = Person(user_id=user_id)

    def add_friendship(self, a: str, b: str) -> None:
        if a == b:
            raise ValueError("self friendship is not allowed")

        self.add_person(a)
        self.add_person(b)

        self._people[a].connect(b)
        self._people[b].connect(a)

    def get_person(self, user_id: str) -> Person:
        if user_id not in self._people:
            raise KeyError(f"unknown user: {user_id}")
        return self._people[user_id]

    def all_user_ids(self) -> list[str]:
        return sorted(self._people.keys())

    def has_user(self, user_id: str) -> bool:
        return user_id in self._people
