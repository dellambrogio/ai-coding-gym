from __future__ import annotations

import unittest

from service_dependency import find_directly_affected_services


def sample_spec() -> dict[str, dict[str, list[str]]]:
    return {
        "extract": {
            "reads_from": ["/warehouse/raw/orders"],
            "writes_to": ["/warehouse/stage/orders"],
        },
        "features": {
            "reads_from": ["/warehouse/stage/orders"],
            "writes_to": ["/warehouse/features/orders"],
        },
        "audit": {
            "reads_from": ["/warehouse/raw/orders/archive"],
            "writes_to": ["/warehouse/reports/audit"],
        },
        "cleanup": {
            "reads_from": ["/warehouse/reports/audit"],
            "writes_to": ["/warehouse/trash"],
        },
    }


class TestPart2DirectImpact(unittest.TestCase):
    def test_matches_exact_deleted_read_path(self):
        affected = find_directly_affected_services(
            sample_spec(), ["/warehouse/raw/orders"])
        self.assertEqual(affected, ["extract"])

    def test_matches_exact_deleted_write_path(self):
        affected = find_directly_affected_services(
            sample_spec(), ["warehouse/trash/"])
        self.assertEqual(affected, ["cleanup"])

    def test_does_not_treat_descendant_as_exact_match(self):
        affected = find_directly_affected_services(
            sample_spec(), ["/warehouse/raw/orders"])
        self.assertNotIn("audit", affected)


if __name__ == "__main__":
    unittest.main()
