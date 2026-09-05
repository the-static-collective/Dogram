from __future__ import annotations

import json
import unittest
from pathlib import Path

from dogram.mathband import ProbeObservation, evaluate_bridge


FIXTURE = Path(__file__).parent / "fixtures" / "mathband_incubator_001.json"


def _complex_quarter_turn(pair: tuple[int, int]) -> tuple[int, int]:
    a, b = pair
    return (-b, a)


def _complex_apply_n(pair: tuple[int, int], turns: int) -> tuple[int, int]:
    result = pair
    for _ in range(turns):
        result = _complex_quarter_turn(result)
    return result


def _matrix_apply(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    pair: tuple[int, int],
) -> tuple[int, int]:
    (m00, m01), (m10, m11) = matrix
    a, b = pair
    return (m00 * a + m01 * b, m10 * a + m11 * b)


def _matrix_apply_n(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    pair: tuple[int, int],
    turns: int,
) -> tuple[int, int]:
    result = pair
    for _ in range(turns):
        result = _matrix_apply(matrix, result)
    return result


def _norm_sq(pair: tuple[int, int]) -> int:
    a, b = pair
    return a * a + b * b


def _semantic_signature(receipt) -> tuple[tuple[str, object, object], ...]:
    return tuple(sorted((outcome.status, outcome.left, outcome.right) for outcome in receipt.outcomes))


class MathBandTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.calibration = cls.fixture["calibration"]
        cls.matrix = tuple(tuple(row) for row in cls.calibration["rotation_matrix"])
        cls.pairs = tuple(tuple(pair) for pair in cls.calibration["pairs"])

    def _exact_probes(self) -> tuple[ProbeObservation, ...]:
        return tuple(
            ProbeObservation(
                name=f"quarter_turn:{pair[0]},{pair[1]}",
                left=_complex_quarter_turn(pair),
                right=_matrix_apply(self.matrix, pair),
                comparison="exact",
                must_preserve=True,
                decisive=True,
            )
            for pair in self.pairs
        )

    def test_exact_complex_matrix_calibration_preserves_all_probes(self) -> None:
        receipt = evaluate_bridge(
            bridge_ref=self.calibration["bridge_ref"],
            voice_a_ref=self.calibration["voice_a_ref"],
            voice_b_ref=self.calibration["voice_b_ref"],
            required_assumptions=tuple(self.calibration["required_assumptions"]),
            provided_assumptions=tuple(self.calibration["required_assumptions"]),
            probes=self._exact_probes(),
        )

        self.assertEqual({outcome.status for outcome in receipt.outcomes}, {"PRESERVED"})
        self.assertEqual(receipt.first_decisive_probe, None)
        self.assertEqual(receipt.exactness, "exact")
        self.assertEqual(receipt.refusals, ())

    def test_rename_bat_preserves_semantics_under_reordering_and_renaming(self) -> None:
        baseline = evaluate_bridge(
            bridge_ref=self.calibration["bridge_ref"],
            voice_a_ref=self.calibration["voice_a_ref"],
            voice_b_ref=self.calibration["voice_b_ref"],
            required_assumptions=tuple(self.calibration["required_assumptions"]),
            provided_assumptions=tuple(self.calibration["required_assumptions"]),
            probes=self._exact_probes(),
        )
        renamed = tuple(
            ProbeObservation(
                name=f"{self.calibration['rename_prefix']}:{index}",
                left=probe.left,
                right=probe.right,
                comparison="exact",
                must_preserve=True,
                decisive=True,
            )
            for index, probe in enumerate(reversed(self._exact_probes()))
        )
        attacked = evaluate_bridge(
            bridge_ref=self.calibration["bridge_ref"],
            voice_a_ref="voice-a-renamed",
            voice_b_ref="voice-b-renamed",
            required_assumptions=tuple(self.calibration["required_assumptions"]),
            provided_assumptions=tuple(self.calibration["required_assumptions"]),
            probes=renamed,
        )

        self.assertEqual(_semantic_signature(attacked), _semantic_signature(baseline))
        self.assertEqual(attacked.first_decisive_probe, None)

    def test_gauge_bat_preserves_relation_and_receipts_common_scale(self) -> None:
        scale = self.calibration["scale_factor"]
        scaled_pairs = tuple((a * scale, b * scale) for a, b in self.pairs)
        probes = tuple(
            ProbeObservation(
                name=f"scaled:{a},{b}",
                left=_complex_quarter_turn((a, b)),
                right=_matrix_apply(self.matrix, (a, b)),
                comparison="exact",
                must_preserve=True,
                decisive=True,
            )
            for a, b in scaled_pairs
        )

        receipt = evaluate_bridge(
            bridge_ref=self.calibration["bridge_ref"],
            voice_a_ref=self.calibration["voice_a_ref"],
            voice_b_ref=self.calibration["voice_b_ref"],
            required_assumptions=tuple(self.calibration["required_assumptions"]),
            provided_assumptions=tuple(self.calibration["required_assumptions"]),
            probes=probes,
            declared_transforms=(self.calibration["gauge_transform"],),
        )

        self.assertEqual({outcome.status for outcome in receipt.outcomes}, {"PRESERVED"})
        self.assertEqual(receipt.declared_transforms, ("common_integer_scale:7",))
        self.assertEqual(receipt.exactness, "exact")

    def test_domain_bat_keeps_outside_domain_unmapped(self) -> None:
        inside = tuple(self.fixture["domain_bat"]["inside_pair"])
        probes = (
            ProbeObservation(
                "inside-domain",
                _complex_quarter_turn(inside),
                _matrix_apply(self.matrix, inside),
                decisive=True,
            ),
            ProbeObservation(
                "outside-domain",
                None,
                None,
                left_defined=False,
                right_defined=False,
            ),
        )
        receipt = evaluate_bridge(
            bridge_ref="restricted-quarter-turn",
            voice_a_ref=self.calibration["voice_a_ref"],
            voice_b_ref=self.calibration["voice_b_ref"],
            required_assumptions=("domain=nonzero_pairs",),
            provided_assumptions=("domain=nonzero_pairs",),
            probes=probes,
        )

        self.assertEqual(receipt.outcomes[0].status, "PRESERVED")
        self.assertEqual(receipt.outcomes[1].status, "UNMAPPED")

    def test_extra_voice_bat_preserves_unmatched_structure(self) -> None:
        receipt = evaluate_bridge(
            bridge_ref=self.calibration["bridge_ref"],
            voice_a_ref=self.calibration["voice_a_ref"],
            voice_b_ref=self.calibration["voice_b_ref"],
            required_assumptions=tuple(self.calibration["required_assumptions"]),
            provided_assumptions=tuple(self.calibration["required_assumptions"]),
            probes=self._exact_probes(),
            extra_a=tuple(self.fixture["extra_voice_bat"]["voice_a_extra"]),
            extra_b=tuple(self.fixture["extra_voice_bat"]["voice_b_extra"]),
        )

        self.assertEqual(receipt.extra_a, ())
        self.assertEqual(receipt.extra_b, ("independent_conjugation_operation",))

    def test_missing_required_assumption_refuses_without_grading_probes(self) -> None:
        receipt = evaluate_bridge(
            bridge_ref=self.calibration["bridge_ref"],
            voice_a_ref=self.calibration["voice_a_ref"],
            voice_b_ref=self.calibration["voice_b_ref"],
            required_assumptions=("complex_pair_identification", "quarter_turn_action"),
            provided_assumptions=("complex_pair_identification",),
            probes=self._exact_probes(),
        )

        self.assertEqual(receipt.exactness, "refused")
        self.assertEqual(receipt.outcomes, ())
        self.assertEqual(receipt.refusals, ("missing assumption: quarter_turn_action",))


if __name__ == "__main__":
    unittest.main()
