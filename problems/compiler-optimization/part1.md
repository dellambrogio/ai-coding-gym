## Part 1: Load a case

Each test case in `tests/data/` is a small straight-line program, with a header of comments:

```
# COST + 2          cost of each operator for this file
# COST * 7
# EXPECTED_TIME 18  the expected answer
# EXPECTED_MEM 2

res1 = var1 * var2
res = res1 + res2
```

`optimizer_utils.load_instruction_case(path)` returns `(cost_model, (expected_time, expected_mem), program_lines)`, but it ignores the `COST` lines and misreads some expected values. Fix it.

Tests: `tests/test_part1_case_loading.py`
