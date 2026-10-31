## Part 3: Selection and clipboard

- `select(start, end)`: select `text[start:end]` (clamp both; swap if `start > end`). An empty range means no selection. The cursor moves to the end of the selection.
- `move`, `undo` and `redo` clear the selection, as does any edit.
- With a selection, `type(s)` replaces it and `backspace()` deletes it (ignoring `n`). Each is a single undoable edit.
- `copy() -> str`: return the selected text and store it in the clipboard. With no selection, return `""` and leave the clipboard unchanged.
- `cut() -> str`: copy, then delete the selection (one undoable edit).
- `paste()`: `type(clipboard)`.
