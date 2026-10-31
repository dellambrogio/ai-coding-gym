from __future__ import annotations

import unittest

from compiler_optimizer import extract_time_and_mem_cost
from tests.test_helpers import case_path


class TestPart4ConstantFolding(unittest.TestCase):
    def test_constant_folding_and_propagation(self):
        self.assertEqual(
            (11, 1),
            extract_time_and_mem_cost(case_path("instruction6.txt")),
        )

    def test_mixed_precedence_and_simplification(self):
        self.assertEqual(
            (38, 2),
            extract_time_and_mem_cost(case_path("instruction7.txt")),
        )


if __name__ == "__main__":
    unittest.main()
