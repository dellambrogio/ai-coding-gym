from __future__ import annotations

import unittest

from expense_rules import amount_exceeds


class TestPart1Amounts(unittest.TestCase):
    def test_amounts_are_compared_numerically(self):
        self.assertTrue(amount_exceeds("100.00", 75))

    def test_small_amounts_do_not_exceed_large_thresholds(self):
        self.assertFalse(amount_exceeds("7.00", 75))


if __name__ == "__main__":
    unittest.main()
