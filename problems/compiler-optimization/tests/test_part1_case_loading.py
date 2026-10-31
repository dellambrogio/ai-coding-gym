from __future__ import annotations

import unittest

from optimizer_utils import load_instruction_case
from tests.test_helpers import case_path


class TestPart1CaseLoading(unittest.TestCase):
    def test_reads_per_file_operator_costs(self):
        cost_model, expected, program = load_instruction_case(
            case_path("instruction2.txt"))

        self.assertEqual({"+": 2, "-": 2, "*": 7, "/": 9}, cost_model)
        self.assertEqual((18, 2), expected)
        self.assertEqual(
            [
                "res1 = var1 * var2",
                "res2 = var3 / var4",
                "res = res1 + res2",
            ],
            program,
        )

    def test_reads_multi_digit_metadata_values(self):
        cost_model, expected, _ = load_instruction_case(
            case_path("instruction6.txt"))

        self.assertEqual({"+": 2, "-": 3, "*": 11, "/": 17}, cost_model)
        self.assertEqual((11, 1), expected)

    def test_ignores_comments_and_blank_lines_in_program_body(self):
        _, _, program = load_instruction_case(case_path("instruction7.txt"))

        self.assertEqual(
            [
                "res1 = 10 * var2",
                "res2 = var3 * 100 - var4",
                "res3 = res1 / 1",
                "dead = 9 / 3",
                "res = res2 + res3 + 0",
            ],
            program,
        )


if __name__ == "__main__":
    unittest.main()
