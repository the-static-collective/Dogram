from __future__ import annotations

import json
from pathlib import Path
import unittest

from dogram.finite_gauge_holonomy import (
    conjugacy_orbit,
    gauge_transform_edges,
    holonomy,
    permutation_group_closure,
)


def _perm(value: list[int]) -> tuple[int, ...]:
    return tuple(value)


def _edges(values: dict[str, list[int]]) -> dict[tuple[str, str], tuple[int, ...]]:
    return {
        tuple(key.split("->")): _perm(value)
        for key, value in values.items()
    }


class FiniteGaugeHolonomyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = Path(__file__).parent / "fixtures" / "finite_gauge_holonomy_001.json"
        cls.fixture = json.loads(path.read_text())
        cls.cycle = [tuple(edge) for edge in cls.fixture["cycle"]]
        cls.group = permutation_group_closure(
            [_perm(value) for value in cls.fixture["generators"]]
        )

    def test_vertex_gauge_change_conjugates_based_holonomy(self) -> None:
        base_edges = _edges(self.fixture["base_edges"])
        gauges = {
            vertex: _perm(value)
            for vertex, value in self.fixture["vertex_gauges"].items()
        }

        changed = gauge_transform_edges(base_edges, gauges)

        self.assertEqual(changed, _edges(self.fixture["expected_gauged_edges"]))

        before = holonomy(base_edges, self.cycle)
        after = holonomy(changed, self.cycle)

        self.assertEqual(before, _perm(self.fixture["expected_base_holonomy"]))
        self.assertEqual(after, _perm(self.fixture["expected_gauged_holonomy"]))
        self.assertNotEqual(before, after)
        self.assertIn(after, conjugacy_orbit(before, self.group))

    def test_different_conjugacy_class_survives_the_gauge_quotient(self) -> None:
        base_holonomy = holonomy(_edges(self.fixture["base_edges"]), self.cycle)
        hostile_holonomy = holonomy(_edges(self.fixture["hostile_edges"]), self.cycle)

        self.assertEqual(
            hostile_holonomy,
            _perm(self.fixture["expected_hostile_holonomy"]),
        )
        self.assertNotIn(hostile_holonomy, conjugacy_orbit(base_holonomy, self.group))
        self.assertEqual(
            len(conjugacy_orbit(base_holonomy, self.group)),
            self.fixture["expected_orbit_sizes"]["base"],
        )
        self.assertEqual(
            len(conjugacy_orbit(hostile_holonomy, self.group)),
            self.fixture["expected_orbit_sizes"]["hostile"],
        )

    def test_generated_group_is_exactly_s3(self) -> None:
        self.assertEqual(len(self.group), 6)


if __name__ == "__main__":
    unittest.main()
