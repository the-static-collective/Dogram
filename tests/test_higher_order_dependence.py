from __future__ import annotations

import json
from pathlib import Path
import unittest

from dogram.matroid_circuit import VectorMatroidInputError, analyze_vector_matroid


FIXTURE = Path(__file__).parent / "fixtures" / "higher_order_dependence_001.json"


class HigherOrderDependenceTests(unittest.TestCase):
    def setUp(self) -> None:
        payload = json.loads(FIXTURE.read_text())
        self.fixture = payload
        self.dependent = analyze_vector_matroid(payload["dependent_specimen"]["vectors"])
        self.free = analyze_vector_matroid(payload["free_control"]["vectors"])

    def test_same_pairwise_rank_surface_can_hide_triple_dependence(self) -> None:
        labels = tuple(self.fixture["labels"])
        for label in labels:
            self.assertEqual(self.dependent.rank((label,)), 1)
            self.assertEqual(self.free.rank((label,)), 1)

        for pair in (("a", "b"), ("a", "c"), ("b", "c")):
            self.assertEqual(self.dependent.rank(pair), 2)
            self.assertEqual(self.free.rank(pair), 2)

        self.assertEqual(self.dependent.rank(labels), 2)
        self.assertEqual(self.free.rank(labels), 3)

    def test_minimal_dependent_set_is_receipted_as_a_circuit(self) -> None:
        self.assertEqual(self.dependent.circuits, (("a", "b", "c"),))
        self.assertEqual(self.dependent.rank_defect(("a", "b", "c")), 1)
        self.assertEqual(self.free.circuits, ())
        self.assertEqual(self.free.rank_defect(("a", "b", "c")), 0)

    def test_receipt_preserves_ambient_dimension_and_refuses_bad_inputs(self) -> None:
        self.assertEqual(
            self.dependent.to_data(),
            {
                "ambient_dimension": 3,
                "labels": ["a", "b", "c"],
                "full_rank": 2,
                "full_rank_defect": 1,
                "circuits": [["a", "b", "c"]],
            },
        )

        with self.assertRaises(VectorMatroidInputError):
            analyze_vector_matroid({})
        with self.assertRaises(VectorMatroidInputError):
            analyze_vector_matroid({"a": (1, 0), "b": (0, 1, 0)})
        with self.assertRaises(VectorMatroidInputError):
            analyze_vector_matroid({"a": (0, 0, 0)})


if __name__ == "__main__":
    unittest.main()
