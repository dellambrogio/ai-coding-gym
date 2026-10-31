from __future__ import annotations


def assert_outcome(testcase, actual: str, expected: str) -> None:
    testcase.assertEqual(expected, actual)
