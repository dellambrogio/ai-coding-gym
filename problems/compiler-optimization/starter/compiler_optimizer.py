from __future__ import annotations

from optimizer_utils import load_instruction_case


def extract_time_and_mem_cost(instruction_file: str) -> tuple[int, int]:
    _cost_model, _expected, _program = load_instruction_case(instruction_file)
    raise NotImplementedError
