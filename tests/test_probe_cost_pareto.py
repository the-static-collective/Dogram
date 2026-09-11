from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.probe_cost_pareto import analyze_probe_costs, dominates


FIXTURE = Path(__file__).parent / "fixtures" / "probe_cost_pareto_001.json"


class ProbeCostParetoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.states = tuple(cls.fixture["states"])
        cls.probes = {name: tuple(outputs) for name, outputs in cls.fixture["probes"].items()}
        cls.costs = cls.fixture["costs"]

    def test_frozen_family_separates_information_cost_and_pareto_orders(self) -> None:
        result = analyze_probe_costs(
            self.states,
            self.probes,
            self.costs,
            tuple(self.fixture["target_pair"]),
        )

        self.assertEqual(list(result.separating_probes), self.fixture["separating_probes"])
        self.assertEqual(
            list(result.information_minimal_separators),
            self.fixture["information_minimal_separators"],
        )
        self.assertEqual(list(result.cost_minimal_separators), self.fixture["cost_minimal_separators"])
        self.assertEqual(list(result.pareto_separators), self.fixture["pareto_separators"])

    def test_more_informative_can_be_cheaper_and_dominate_an_information_minimal_probe(self) -> None:
        self.assertTrue(
            dominates(
                self.probes["joint"], self.costs["joint"],
                self.probes["vertical"], self.costs["vertical"],
            )
        )

        result = analyze_probe_costs(self.states, self.probes, self.costs, ("a", "d"))
        self.assertIn("vertical", result.information_minimal_separators)
        self.assertNotIn("vertical", result.pareto_separators)
        self.assertIn("joint", result.pareto_separators)

    def test_pareto_frontier_can_retain_incomparable_separators(self) -> None:
        self.assertFalse(
            dominates(
                self.probes["joint"], self.costs["joint"],
                self.probes["diagonal"], self.costs["diagonal"],
            )
        )
        self.assertFalse(
            dominates(
                self.probes["diagonal"], self.costs["diagonal"],
                self.probes["joint"], self.costs["joint"],
            )
        )

        result = analyze_probe_costs(self.states, self.probes, self.costs, ("a", "d"))
        self.assertEqual(result.pareto_separators, ("diagonal", "joint"))

    def test_validation_rejects_missing_negative_or_nonfinite_costs(self) -> None:
        with self.assertRaises(ValueError):
            analyze_probe_costs(("a", "b"), {"p": (0, 1)}, {}, ("a", "b"))
        with self.assertRaises(ValueError):
            analyze_probe_costs(("a", "b"), {"p": (0, 1)}, {"p": -1}, ("a", "b"))
        with self.assertRaises(ValueError):
            analyze_probe_costs(("a", "b"), {"p": (0, 1)}, {"p": float("inf")}, ("a", "b"))


if __name__ == "__main__":
    unittest.main()
