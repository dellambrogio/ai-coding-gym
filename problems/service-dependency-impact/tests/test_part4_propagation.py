from __future__ import annotations

import unittest

from service_dependency import build_impact_chains


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
        "ranker": {
            "reads_from": ["/warehouse/features/orders"],
            "writes_to": ["/warehouse/output/rankings"],
        },
        "notifications": {
            "reads_from": ["/warehouse/output/rankings"],
            "writes_to": ["/warehouse/notifications"],
        },
        "audit": {
            "reads_from": ["/warehouse/raw/orders/archive"],
            "writes_to": ["/warehouse/reports/audit"],
        },
    }


class TestPart4Propagation(unittest.TestCase):
    def test_propagates_through_downstream_services(self):
        report = build_impact_chains(sample_spec(), ["/warehouse/raw/orders"])
        self.assertEqual(
            report,
            {
                "/warehouse/raw/orders": [
                    "audit",
                    "extract",
                    "features",
                    "ranker",
                    "notifications",
                ]
            },
        )

    def test_each_deleted_root_gets_its_own_report(self):
        report = build_impact_chains(
            sample_spec(),
            ["/warehouse/raw/orders", "/warehouse/output/rankings"],
        )
        self.assertEqual(
            report["/warehouse/output/rankings"], ["notifications", "ranker"])


if __name__ == "__main__":
    unittest.main()
