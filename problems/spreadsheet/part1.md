## Part 1: Cells and formulas

In `solution.py`, implement `class Sheet`. Cells are named `A1` to `Z99`: one capital letter, then a row from 1 to 99 (no leading zero).

- `set(cell: str, value)`: `value` is an `int`, a `float`, or a formula string starting with `=`, like `"=A1+B2*2"` or `"=(A1-3)/C7"`. Formulas use numbers, cell names, `+ - * /`, unary minus and parentheses.
- `get(cell: str) -> int | float`: the cell's value. Empty cells are `0`. Formulas are evaluated with the current values of the cells they reference.
- Raise `ValueError` for an invalid cell name, a value of another type, or a formula with invalid syntax (checked in `set`). Division by zero raises `ZeroDivisionError` from `get`.

Use normal precedence (`*` and `/` before `+` and `-`). Don't use Python's `eval` on the raw formula.
