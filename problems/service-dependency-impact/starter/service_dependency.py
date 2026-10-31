from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from path_utils import is_same_or_ancestor, normalize_path


@dataclass(frozen=True)
class ServiceConfig:
    service_id: str
    reads_from: tuple[str, ...]
    writes_to: tuple[str, ...]


def load_services(spec: dict[str, dict[str, list[str]]]) -> list[ServiceConfig]:
    services: list[ServiceConfig] = []

    for service_id in sorted(spec.keys()):
        config = spec[service_id]
        reads = tuple(normalize_path(path)
                      for path in config.get("reads_from", []))
        writes = tuple(normalize_path(path)
                       for path in config.get("writes_to", []))
        services.append(ServiceConfig(service_id=service_id,
                        reads_from=reads, writes_to=writes))

    return services


def find_directly_affected_services(
    spec: dict[str, dict[str, list[str]]],
    deleted_paths: list[str],
) -> list[str]:
    raise NotImplementedError(
        "find_directly_affected_services() not implemented yet.")


def find_tree_affected_services(
    spec: dict[str, dict[str, list[str]]],
    deleted_paths: list[str],
) -> list[str]:
    raise NotImplementedError(
        "find_tree_affected_services() not implemented yet.")


def build_dependency_graph(
    services: list[ServiceConfig],
) -> dict[str, list[str]]:
    writers_by_path: dict[str, list[str]] = {}
    service_by_id = {service.service_id: service for service in services}

    for service in services:
        for path in service.writes_to:
            writers_by_path.setdefault(path, []).append(service.service_id)

    adjacency: dict[str, set[str]] = {
        service.service_id: set() for service in services}

    for service in services:
        for path in service.reads_from:
            for writer_id in writers_by_path.get(path, []):
                if writer_id != service.service_id:
                    adjacency[writer_id].add(service.service_id)

    return {
        service_id: sorted(neighbors)
        for service_id, neighbors in adjacency.items()
        if service_id in service_by_id
    }


def build_impact_chains(
    spec: dict[str, dict[str, list[str]]],
    deleted_paths: list[str],
) -> dict[str, list[str]]:
    raise NotImplementedError("build_impact_chains() not implemented yet.")
