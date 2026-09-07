from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.probe_partition_refinement import analyze_probe_family, factorization_map, probe_refines


FIXTURE = Path(__file__).parent / "fixtures" / "probe_partition_refinement_001.json"


class ProbePartitionRefinementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.states = tuple(cls.fixture["states"])
        cls.probes = {name: tuple(outputs) for name, outputs in cls.fixture["probes"].items()}

    def test_frozen_family_recovers_partition_poset_and_minimal_separators(self) -> None:
        result = analyze_probe_family(
            self.states,
            self.probes,
            tuple(self.fixture["target_pair"]),
        )

        self.assertEqual(
            {name: [list(block) for block in blocks] for name, blocks in result.partitions.items()},
            self.fixture["partitions"],
        )
        self.assertEqual([list(edge) for edge in result.cover_relations], self.fixture["cover_relations"])
        self.assertEqual(list(result.separating_probes), self.fixture["separating_probes"])
        self.assertEqual(list(result.minimal_separators), self.fixture["minimal_separators"])

    def test_incomparable_probes_can_both_be_minimal_separators(self) -> None:
        vertical = self.probes["vertical"]
        diagonal = self.probes["diagonal"]
        joint = self.probes["joint"]

        self.assertFalse(probe_refines(vertical, diagonal))
        self.assertFalse(probe_refines(diagonal, vertical))
        self.assertTrue(probe_refines(joint, vertical))
        self.assertTrue(probe_refines(joint, diagonal))

        result = analyze_probe_family(self.states, self.probes, ("a", "d"))
        self.assertEqual(result.minimal_separators, ("vertical", "diagonal"))

    def test_refinement_is_equivalent_to_a_deterministic_factorization_witness(self) -> None:
        expected = self.fixture["factorizations"]
        pairs = (
            ("vertical", "coarse"),
            ("diagonal", "coarse"),
            ("joint", "vertical"),
            ("joint", "diagonal"),
        )
        for stronger, weaker in pairs:
            witness = factorization_map(self.probes[stronger], self.probes[weaker])
            self.assertEqual(dict(witness), expected[f"{stronger}->{weaker}"])

        self.assertIsNone(factorization_map(self.probes["vertical"], self.probes["diagonal"]))
        self.assertIsNone(factorization_map(self.probes["diagonal"], self.probes["vertical"]))

    def test_family_validation_rejects_length_mismatch_and_unknown_target(self) -> None:
        with self.assertRaises(ValueError):
            analyze_probe_family(("a", "b"), {"bad": (0,)}, ("a", "b"))
        with self.assertRaises(ValueError):
            analyze_probe_family(("a", "b"), {"ok": (0, 1)}, ("a", "z"))


if __name__ == "__main__":
    unittest.main()
