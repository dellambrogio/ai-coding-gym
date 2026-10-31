## Part 3: Durations

- `add_task(name, deps=(), duration=1)`: each task takes `duration` time units (`>= 0`; raise `ValueError` if negative).
- With unlimited workers, a task starts as soon as all its dependencies have finished.
- `earliest_start(name) -> int`: when the task can start.
- `total_time() -> int`: when the last task finishes (`0` for an empty graph).
- Both raise `ValueError` on a cycle and `KeyError` on a missing dependency.
