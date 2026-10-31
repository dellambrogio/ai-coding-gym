## Part 3: Weighted splits

`add_expense(payer, amount, participants, shares=None)`: `shares` is a list of positive integers, one per participant (`ValueError` otherwise). Each participant owes `amount * share / total_shares`, rounded down; the leftover cents go one each to the participants with the largest fractional parts (the remainder of `amount * share % total_shares`), ties alphabetically. Without `shares`, everyone has share 1, which gives the same result as part 1.
