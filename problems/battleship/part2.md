## Part 2: Sink every ship

Implement `Solver.solve()`: shoot at the board with `board.check_shot(row, col)` until `board.all_sunk()`. The solver may only learn about ships through `check_shot`; don't read the board's private fields. Record every shot so `get_shots()` returns them in order, and don't shoot the same cell twice.

On a 6x6 board with the test fleet, the solver must win in fewer than 36 shots.

Tests: `tests/test_part2_solver.py`
