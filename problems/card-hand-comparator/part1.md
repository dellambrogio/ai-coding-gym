## Part 1: Card parsing

Compare poker-like hands. Cards are strings such as `"AH"`, `"10D"`, `"QS"`: rank (2-10, J, Q, K, A) followed by suit (H, D, C, S). `hand_utils.py` parses cards and summarizes hands; `card_hand.py` has one evaluator per hand category.

`parse_card` fails on some valid cards. Fix it.

Tests: `tests/test_part1_parsing.py`
