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


def _affected(
    services: list[ServiceConfig],
    deleted_paths: list[str],
    matches,
) -> list[str]:
    deleted = [normalize_path(path) for path in deleted_paths]
    return sorted(
        service.service_id
        for service in services
        if any(matches(root, path) for root in deleted for path in service.reads_from + service.writes_to)
    )


def find_directly_affected_services(
    spec: dict[str, dict[str, list[str]]],
    deleted_paths: list[str],
) -> list[str]:
    return _affected(load_services(spec), deleted_paths, lambda root, path: root == path)


def find_tree_affected_services(
    spec: dict[str, dict[str, list[str]]],
    deleted_paths: list[str],
) -> list[str]:
    return _affected(load_services(spec), deleted_paths, is_same_or_ancestor)


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
    """Per deleted path: the services it hits directly (sorted), then downstream readers level by level."""
    services = load_services(spec)
    graph = build_dependency_graph(services)
    report: dict[str, list[str]] = {}
    for root in deleted_paths:
        level = find_tree_affected_services(spec, [root])
        seen = set(level)
        chain: list[str] = []
        queue = deque([level])
        while queue:
            level = queue.popleft()
            chain += level
            nxt = sorted({n for s in level for n in graph[s]} - seen)
            seen |= set(nxt)
            if nxt:
                queue.append(nxt)
        report[normalize_path(root)] = chain
    return report
