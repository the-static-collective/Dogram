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

    def test_false_friend_bat_cannot_outvote_decisive_failure(self) -> None:
        pair = tuple(self.fixture["false_friend_bat"]["probe_pair"])
        false_matrix = tuple(tuple(row) for row in self.fixture["false_friend_bat"]["matrix"])

        complex_once = _complex_apply_n(pair, 1)
        false_once = _matrix_apply_n(false_matrix, pair, 1)
        complex_twice = _complex_apply_n(pair, 2)
        false_twice = _matrix_apply_n(false_matrix, pair, 2)
        complex_four = _complex_apply_n(pair, 4)
        false_four = _matrix_apply_n(false_matrix, pair, 4)

        probes = (
            ProbeObservation("norm-input", _norm_sq(pair), _norm_sq(pair)),
            ProbeObservation("norm-output", _norm_sq(complex_once), _norm_sq(false_once)),
            ProbeObservation(
                "origin-fixed",
                _complex_apply_n((0, 0), 1),
                _matrix_apply_n(false_matrix, (0, 0), 1),
            ),
            ProbeObservation("four-step-return", complex_four, false_four),
            ProbeObservation(
                "two-turn-output",
                complex_twice,
                false_twice,
                decisive=True,
                must_preserve=True,
            ),
        )

        receipt = evaluate_bridge(
            bridge_ref="complex-quarter-turn__reflection-false-friend",
            voice_a_ref=self.calibration["voice_a_ref"],
            voice_b_ref="reflection-like-matrix",
            required_assumptions=("pair_identification",),
            provided_assumptions=("pair_identification",),
            probes=probes,
        )

        self.assertEqual(sum(o.status == "PRESERVED" for o in receipt.outcomes), 4)
        self.assertEqual(receipt.outcomes[-1].status, "BROKEN")
        self.assertEqual(
            receipt.first_decisive_probe,
            self.fixture["false_friend_bat"]["decisive_probe"],
        )

    def test_numeric_disagreement_within_tolerance_is_residual_not_exact(self) -> None:
        left, right, tolerance = self.fixture["residual_bat"]["within_tolerance"]
        receipt = evaluate_bridge(
            bridge_ref="approximate-control",
            voice_a_ref="numeric-a",
            voice_b_ref="numeric-b",
            required_assumptions=(),
            provided_assumptions=(),
            probes=(
                ProbeObservation(
                    "approximate-probe",
                    left,
                    right,
                    comparison="numeric",
                    tolerance=tolerance,
                    decisive=True,
                ),
            ),
        )

        self.assertEqual(receipt.outcomes[0].status, "RESIDUAL")
        self.assertAlmostEqual(receipt.outcomes[0].residual, abs(left - right))
        self.assertEqual(receipt.exactness, "approximate")
        self.assertIsNone(receipt.first_decisive_probe)

    def test_numeric_disagreement_outside_tolerance_breaks_decisive_probe(self) -> None:
        left, right, tolerance = self.fixture["residual_bat"]["outside_tolerance"]
        receipt = evaluate_bridge(
            bridge_ref="approximate-control",
            voice_a_ref="numeric-a",
            voice_b_ref="numeric-b",
            required_assumptions=(),
            provided_assumptions=(),
            probes=(
                ProbeObservation(
                    "approximate-probe",
                    left,
                    right,
                    comparison="numeric",
                    tolerance=tolerance,
                    decisive=True,
                ),
            ),
        )

        self.assertEqual(receipt.outcomes[0].status, "BROKEN")
        self.assertGreater(receipt.outcomes[0].residual, tolerance)
        self.assertEqual(receipt.first_decisive_probe, "approximate-probe")


if __name__ == "__main__":
    unittest.main()
