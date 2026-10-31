## Part 1: Rendering

A grid maze: `#` wall, `.` open, `S` start, `E` end. `maze.py` holds the grid and movement rules, `mazes.py` some sample mazes, `solver.py` the solver to implement, `main.py` runs it.

`render_with_path(path)` marks the path with `*`, but it overwrites `S` and `E`. Keep them.

Tests: `tests/test_part1_rendering.py`
