## Part 2: Ranges and dependents

- Formulas may call `SUM`, `MIN` and `MAX`. Arguments are expressions or ranges like `A1:B3` (the rectangle between two corners, in any order; empty cells count as `0`). Example: `"=SUM(A1:A3, 10) * MAX(B1, B2)"`.
- `dependents(cell) -> list[str]`: every cell whose value depends on `cell`, directly or indirectly, sorted by column letter and then row number (`A2` before `A10`).
