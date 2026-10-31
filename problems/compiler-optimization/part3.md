## Part 3: Dead code

Instructions whose result `res` doesn't depend on, directly or through other temporaries, are never executed: they cost no time and no memory.

Tests: `tests/test_part3_dead_code.py`
