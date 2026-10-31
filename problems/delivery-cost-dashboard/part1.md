## Part 1: Cost precision

A dashboard for a delivery company that pays drivers by the hour. Times are in seconds; money is in US dollars, stored internally as integer cents.

`calculate_delivery_cost_cents(rate, start, end)` truncates the duration to whole hours, so a 90-minute delivery at $10/h costs $10 instead of $15. Charge the exact duration, to the second, rounded to the nearest cent.

Tests: `tests/test_part1_precision.py`
