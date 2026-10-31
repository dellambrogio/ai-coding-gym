from __future__ import annotations

import unittest

from compiler_optimizer import extract_time_and_mem_cost
from tests.test_helpers import case_path


class TestPart2BasicAnalyzer(unittest.TestCase):
    def test_instruction1(self):
        self.assertEqual(
            (4, 2),
            extract_time_and_mem_cost(case_path("instruction1.txt")),
        )

    def test_instruction2(self):
        self.assertEqual(
            (18, 2),
            extract_time_and_mem_cost(case_path("instruction2.txt")),
        )

    def test_instruction3(self):
        self.assertEqual(
            (16, 1),
            extract_time_and_mem_cost(case_path("instruction3.txt")),
        )


if __name__ == "__main__":
    unittest.main()
