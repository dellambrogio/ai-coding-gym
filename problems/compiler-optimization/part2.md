## Part 2: Time and memory

Implement `extract_time_and_mem_cost(path) -> (time, mem)` for a program whose result is the variable `res`. Expressions use `+ - * /` with the usual precedence, variables and integer constants.

- **time**: sum of the operator costs of every operation executed.
- **mem**: the largest number of temporaries (variables assigned in the program) alive at the same time. A temporary is alive from its assignment until the instruction that uses it for the last time; that instruction can reuse its memory for its own result. Inputs such as `var1` are free.

Tests: `tests/test_part2_basic_analyzer.py`
