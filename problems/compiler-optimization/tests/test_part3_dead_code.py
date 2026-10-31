from __future__ import annotations

import unittest

from compiler_optimizer import extract_time_and_mem_cost
from tests.test_helpers import case_path


class TestPart3DeadCode(unittest.TestCase):
    def test_eliminates_dead_instruction_chain(self):
        self.assertEqual(
            (3, 1),
            extract_time_and_mem_cost(case_path("instruction4.txt")),
        )

    def test_releases_temporaries_after_last_use(self):
        self.assertEqual(
            (20, 1),
            extract_time_and_mem_cost(case_path("instruction5.txt")),
        )


if __name__ == "__main__":
    unittest.main()
