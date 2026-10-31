## Part 1: Order the tasks

In `solution.py`, implement `class TaskGraph`:

- `add_task(name: str, deps=())`: add a task that depends on the tasks named in `deps`. Dependencies may be added later than the task that needs them. Raise `ValueError` if `name` was already added.
- `order() -> list[str]`: all tasks in an order where every task comes after its dependencies. When several tasks are ready at once, take them in alphabetical order (so the result is unique). Raise `KeyError` if some dependency was never added.

You may assume there are no cycles in this part.
