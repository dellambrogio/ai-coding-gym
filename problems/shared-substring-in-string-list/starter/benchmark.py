"""Benchmark harness comparing the containment strategies.

The dataset is generated from a fixed seed, so every run measures the
same workload. Strategies that are still unimplemented are reported as
skipped instead of failing the whole harness, keeping the benchmark
runnable at every stage of the project.
"""

from __future__ import annotations

import random
import time
from typing import Callable

from substring_finder import (
    find_contained_string,
    find_shortest_contained_string,
    find_contained_string_trie,
)

STRATEGIES: list[tuple[str, Callable[[list[str]], str | None]]] = [
    ("pairwise", find_contained_string),
    ("shortest", find_shortest_contained_string),
    ("trie scan", find_contained_string_trie),
]


def build_dataset(seed: int = 20260609, count: int = 80, length: int = 12) -> list[str]:
    """Build a deterministic dataset with planted containment pairs."""
    rng = random.Random(seed)
    letters = "abcdefghijklmnopqrstuvwxyz"
    words = [
        "".join(rng.choice(letters) for _ in range(length)) for _ in range(count)
    ]
    # Plant containments: short chunks cut out of existing words are
    # guaranteed to occur inside their donors.
    for _ in range(count // 4):
        donor = rng.choice(words)
        start = rng.randrange(0, len(donor) - 2)
        words.append(donor[start : start + 3])
    rng.shuffle(words)
    return words


def run_benchmark(dataset: list[str], repeat: int = 3) -> list[dict]:
    """Time every implemented strategy; skip the ones still guarded."""
    results: list[dict] = []
    for name, strategy in STRATEGIES:
        try:
            strategy(dataset[:1])
        except NotImplementedError:
            results.append(
                {"strategy": name, "implemented": False, "elapsed_ms": 0.0, "answer": None}
            )
            continue
        best: float | None = None
        answer: str | None = None
        for _ in range(repeat):
            started = time.perf_counter()
            answer = strategy(dataset)
            elapsed = time.perf_counter() - started
            best = elapsed if best is None else min(best, elapsed)
        results.append(
            {
                "strategy": name,
                "implemented": True,
                "elapsed_ms": best * 1000.0,
                "answer": answer,
            }
        )
    return results


def main() -> None:
    dataset = build_dataset()
    print(f"dataset: {len(dataset)} strings")
    for row in run_benchmark(dataset):
        if not row["implemented"]:
            print(f"{row['strategy']:<14} skipped (not implemented yet)")
        else:
            print(
                f"{row['strategy']:<14} {row['elapsed_ms']:8.2f} ms"
                f"  answer={row['answer']!r}"
            )


if __name__ == "__main__":
    main()
