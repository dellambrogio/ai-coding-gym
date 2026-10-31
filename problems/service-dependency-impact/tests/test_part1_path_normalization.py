from __future__ import annotations

import unittest

from path_utils import is_same_or_ancestor, normalize_path


class TestPart1PathNormalization(unittest.TestCase):
    def test_collapses_repeated_slashes_and_trailing_slash(self):
        self.assertEqual(normalize_path(
            "//warehouse///raw/orders/"), "/warehouse/raw/orders")

    def test_preserves_root_path(self):
        self.assertEqual(normalize_path("/"), "/")

    def test_ancestor_check_uses_normalized_paths(self):
        self.assertTrue(is_same_or_ancestor(
            "//warehouse/raw/", "/warehouse/raw/orders"))
        self.assertFalse(is_same_or_ancestor(
            "/warehouse/raw/orders", "/warehouse/raw/users"))


if __name__ == "__main__":
    unittest.main()
