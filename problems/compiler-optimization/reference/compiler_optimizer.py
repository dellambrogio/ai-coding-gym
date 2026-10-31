from __future__ import annotations

import re
from fractions import Fraction

from optimizer_utils import load_instruction_case

RESULT = "res"
OPS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}

# An operand is a variable name (str) or a constant (Fraction).
# A tree is an operand or (op, left, right).


def parse_expression(text: str):
    """Parse `a + b * c` with the usual precedence, left-associative."""
    tokens = re.findall(r"[A-Za-z_]\w*|\d+|[-+*/]", text)
    pos = 0

    def atom():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        return Fraction(int(tok)) if tok.isdigit() else tok

    def level(ops, operand):
        nonlocal pos
        tree = operand()
        while pos < len(tokens) and tokens[pos] in ops:
            op = tokens[pos]
            pos += 1
            tree = (op, tree, operand())
        return tree

    tree = level("+-", lambda: level("*/", atom))
    if pos != len(tokens):
        raise ValueError(f"cannot parse {text!r}")
    return tree


def simplify(tree, env):
    """Constant folding/propagation and identities (x+0, x-0, x*1, x/1, x*0)."""
    if isinstance(tree, str):
        return env.get(tree, tree)
    if not isinstance(tree, tuple):
        return tree
    op, left, right = tree[0], simplify(tree[1], env), simplify(tree[2], env)
    const_l, const_r = isinstance(left, Fraction), isinstance(right, Fraction)
    if const_l and const_r and not (op == "/" and right == 0):
        return OPS[op](left, right)
    if op in "+-" and const_r and right == 0:
        return left
    if op == "+" and const_l and left == 0:
        return right
    if op in "*/" and const_r and right == 1:
        return left
    if op == "*" and const_l and left == 1:
        return right
    if op == "*" and ((const_l and left == 0) or (const_r and right == 0)):
        return Fraction(0)
    return (op, left, right)


def time_cost(tree, cost_model) -> int:
    if not isinstance(tree, tuple):
        return 0
    return cost_model[tree[0]] + time_cost(tree[1], cost_model) + time_cost(tree[2], cost_model)


def variables(tree) -> set[str]:
    if isinstance(tree, str):
        return {tree}
    if isinstance(tree, tuple):
        return variables(tree[1]) | variables(tree[2])
    return set()


def extract_time_and_mem_cost(instruction_file: str) -> tuple[int, int]:
    cost_model, _expected, program = load_instruction_case(instruction_file)

    # 1. Parse and simplify. Instructions that reduce to a constant or to another
    #    variable become aliases: no time, no memory.
    env: dict[str, object] = {}
    computed: list[tuple[str, object]] = []
    for line in program:
        target, expr = (part.strip() for part in line.split("=", 1))
        tree = simplify(parse_expression(expr), env)
        if isinstance(tree, tuple):
            computed.append((target, tree))
        else:
            env[target] = tree

    # 2. Dead code: keep only instructions that `res` depends on.
    needed = variables(env.get(RESULT, RESULT))
    live_code = []
    for target, tree in reversed(computed):
        if target in needed:
            live_code.append((target, tree))
            needed |= variables(tree)
    live_code.reverse()

    # 3. Time is the sum of operator costs; memory is the peak number of
    #    temporaries alive at once, freed after their last use.
    temps = {target for target, _ in live_code}
    last_use = {}
    for i, (_, tree) in enumerate(live_code):
        for name in variables(tree) & temps:
            last_use[name] = i
    time = mem = 0
    alive: set[str] = set()
    for i, (target, tree) in enumerate(live_code):
        time += time_cost(tree, cost_model)
        alive -= {name for name in variables(tree) if last_use.get(name) == i}
        alive.add(target)
        mem = max(mem, len(alive))
    return time, mem
