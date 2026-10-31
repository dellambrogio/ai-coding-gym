from __future__ import annotations

from typing import Dict, List, Tuple


DEFAULT_COSTS: Dict[str, int] = {
    "+": 1,
    "-": 1,
    "*": 5,
    "/": 5,
}


def load_instruction_case(instruction_file: str) -> Tuple[Dict[str, int], tuple[int, int], List[str]]:
    cost_model = dict(DEFAULT_COSTS)
    expected_time = 0
    expected_mem = 0
    program: List[str] = []

    with open(instruction_file, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue

            if line.startswith("# COST"):
                _, _, op, cost = line.split()
                cost_model[op] = int(cost)
                continue

            if line.startswith("# EXPECTED_TIME"):
                expected_time = int(line.split()[-1])
                continue

            if line.startswith("# EXPECTED_MEM"):
                expected_mem = int(line.split()[-1])
                continue

            if line.startswith("#"):
                continue

            program.append(line)

    return cost_model, (expected_time, expected_mem), program
