from __future__ import annotations


def assert_money_equal(testcase, actual: float, expected: float) -> None:
    testcase.assertAlmostEqual(actual, expected, places=2)
