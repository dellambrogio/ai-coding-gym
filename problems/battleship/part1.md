## Part 1: Board bugs

A small Battleship engine: `board.py` (ships, shots), `fleet.py` (ship definitions), `solver.py` (to implement), `main.py` (runs the solver).

The board tests in `tests/test_part1_board.py` fail. Find and fix the bugs in `Board`: `place_ship(ship, row, col, horizontal)` places a ship on consecutive cells to the right (horizontal) or downwards (vertical); `check_shot(row, col)` returns `MISS`, `HIT`, or `SUNK` when the shot hits the last unhit cell of a ship.

Tests: `tests/test_part1_board.py`
