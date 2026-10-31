## Part 3: Typo tolerance

`suggest(prefix, k=5, typos=0)`: with `typos=1`, also suggest words whose beginning is within **one edit** of `prefix` (one character inserted, deleted or replaced). Formally, a word matches if some prefix of the word has Levenshtein distance `<= typos` from `prefix`.

Exact prefix matches come first (by score, then alphabetically), followed by the typo matches (by score, then alphabetically), up to `k` total. `typos=0` behaves as before.
