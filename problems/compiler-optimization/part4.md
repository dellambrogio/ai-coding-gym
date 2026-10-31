## Part 4: Constant folding

Simplify before computing the cost:

- operations on constants only are computed at compile time (`tmp = 8 + 2` costs nothing), and the constants propagate into later instructions;
- identities cost nothing: `x + 0`, `0 + x`, `x - 0`, `x * 1`, `1 * x`, `x / 1` are `x`; `x * 0` is `0`;
- an instruction that reduces to a constant or a single variable is just a new name for it: no time, no memory.

Tests: `tests/test_part4_constant_folding.py`
