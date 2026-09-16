from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.anti_collapse_reachability import analyze_collapse


FIXTURE = Path(__file__).parent / "fixtures" / "anti_collapse_reachability_001.json"


def _summary(result):
    return {
        "lawful_quotient": result.lawful_quotient,
        "factorization_witness_present": result.factorization_witness is not None,
        "collapse_classes": [list(block) for block in result.collapse_classes],
        "preserved_distinctions": [list(pair) for pair in result.preserved_distinctions],
        "lost_distinctions": [list(pair) for pair in result.lost_distinctions],
    }


class AntiCollapseReachabilityFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_bool_int_specimen_matches_frozen_receipt(self) -> None:
        result = analyze_collapse(
            states=("int:1", "bool:true", "int:0", "bool:false"),
            rich_projection=(("int", 1), ("bool", True), ("int", 0), ("bool", False)),
            collapsed_projection=(1, True, 0, False),
        )
        self.assertEqual(_summary(result), self.fixture["bool_int"])

    def test_typed_address_specimen_matches_frozen_receipt(self) -> None:
        result = analyze_collapse(
            states=("spine@A", "braid@A", "spine@B"),
            rich_projection=(("A", "spine"), ("A", "braid"), ("B", "spine")),
            collapsed_projection=("A", "A", "B"),
        )
        self.assertEqual(_summary(result), self.fixture["typed_address"])


if __name__ == "__main__":
    unittest.main()
