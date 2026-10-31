## Part 2: Undo and redo

- `undo() -> bool`: revert the last edit (`type` or `backspace` that changed the text). Restore both the text and the cursor to what they were just before that edit. Return `False` if there's nothing to undo.
- `redo() -> bool`: re-apply the last undone edit, with the cursor where it was right after that edit. Return `False` if there's nothing to redo.
- Any new edit clears the redo history. Cursor moves are not edits and can't be undone. Edits that change nothing (typing `""`, backspace at position 0) are not recorded.
