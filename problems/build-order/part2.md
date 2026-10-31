## Part 2: Cycles

- `order()` raises `ValueError` if the dependencies contain a cycle.
- `find_cycle() -> list[str] | None`: return one cycle as `[t1, t2, ..., tk, t1]`, where each task's successor in the list is one of its dependencies. Return `None` if there is no cycle. A task that depends on itself is the cycle `[t, t]`.
