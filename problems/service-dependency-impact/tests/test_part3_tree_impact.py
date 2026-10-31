from __future__ import annotations

import unittest

from service_dependency import find_tree_affected_services


def sample_spec() -> dict[str, dict[str, list[str]]]:
    return {
        "extract": {
            "reads_from": ["/warehouse/raw/orders"],
            "writes_to": ["/warehouse/stage/orders"],
        },
        "audit": {
            "reads_from": ["/warehouse/raw/orders/archive"],
            "writes_to": ["/warehouse/reports/audit"],
        },
        "users": {
            "reads_from": ["/warehouse/raw/users"],
            "writes_to": ["/warehouse/stage/users"],
        },
    }


class TestPart3TreeImpact(unittest.TestCase):
    def test_deleted_parent_path_affects_descendants(self):
        affected = find_tree_affected_services(
            sample_spec(), ["/warehouse/raw/orders"])
        self.assertEqual(affected, ["audit", "extract"])

    def test_sibling_subtree_is_not_affected(self):
        affected = find_tree_affected_services(
            sample_spec(), ["/warehouse/raw/orders"])
        self.assertNotIn("users", affected)

    def test_multiple_deleted_roots_union_results(self):
        affected = find_tree_affected_services(
            sample_spec(),
            ["/warehouse/raw/orders", "/warehouse/raw/users"],
        )
        self.assertEqual(affected, ["audit", "extract", "users"])


if __name__ == "__main__":
    unittest.main()
