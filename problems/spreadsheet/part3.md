## Part 3: Cycles and clearing

- `set` raises `ValueError` if the new value would create a circular reference (including a cell referring to itself). The sheet must be unchanged after the error.
- `clear(cell)`: make the cell empty again.
