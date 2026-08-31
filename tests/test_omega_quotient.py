import json
import pathlib
import unittest

from dogram.canonical import canonical_json_bytes
from dogram.execution_cut import make_execution_cut, typed_footprint_residual
from dogram.omega import OmegaConfig
from dogram.omega_quotient import TargetFamily, compare_execution_cuts, run_omega_quotient
from dogram.program import decode_program
from dogram.registry import build_bootstrap_registry
from dogram.vm import VMConfig


ROOT = pathlib.Path(__file__).parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "omega"


def load_program(name="positive-program.json"):
    return decode_program(json.loads((FIXTURES / name).read_text()))


def default_inputs():
    return {
        "payload": {"value": {"kind": "integer", "value": 42}},
        "diagnostic": ["a", "b", "c"],
    }


def result_target(*, predeclared=True):
    return TargetFamily(
        id="T_result",
        probes=("result",),
        declared_before_comparison=predeclared,
    )


def run_positive(*, target=None, proposal_id="proposal-omega-quotient"):
    return run_omega_quotient(
        program=load_program(),
        inputs=default_inputs(),
        declared_target_step="diagnostic",
        proposal_id=proposal_id,
        target=result_target() if target is None else target,
        registry=build_bootstrap_registry(),
        config=OmegaConfig(exec_config=VMConfig(max_exec_steps=10)),
    )


def execution_data(
    *,
    input_digest="sha256:world",
    result=7,
    addresses=None,
    trace=None,
    fuel_remaining=8,
):
    return {
        "schema": "dogram.execution-data/v0",
        "program_digest": "sha256:program",
        "input_digest": input_digest,
        "status": "OK",
        "result": result,
        "reason_code": None,
        "residuals": [],
        "step_trace": [] if trace is None else trace,
        "consumed_input_addresses": [] if addresses is None else addresses,
        "fuel_remaining": fuel_remaining,
    }


class OmegaQuotientTests(unittest.TestCase):
    def test_positive_pair_preserves_target_and_receipts_changed_contact_surface(self):
        result = run_positive()
        self.assertEqual((result.status, result.reason_code), ("OK", None))

        receipt = result.receipt
        self.assertEqual(receipt["schema"], "dogram.omega-quotient/v0")
        self.assertEqual(receipt["target_verdict"], "EQUIVALENT_UNDER_T")
        self.assertEqual(receipt["target_family"]["id"], "T_result")
        self.assertTrue(receipt["target_family"]["declared_before_comparison"])

        before = receipt["baseline"]["execution_cut"]
        after = receipt["candidate"]["execution_cut"]
        self.assertEqual(before["input_digest"], after["input_digest"])
        self.assertEqual(before["result"], after["result"])
        self.assertNotEqual(
            receipt["baseline"]["execution_digest"],
            receipt["candidate"]["execution_digest"],
        )

        residual = receipt["footprint_residual"]
        self.assertEqual(
            residual["consumed_input_addresses"],
            {
                "before": [["payload"], ["diagnostic"]],
                "after": [["payload"]],
            },
        )
        self.assertEqual(
            [entry["step_id"] for entry in residual["step_trace"]["before"]],
            ["value", "diagnostic"],
        )
        self.assertEqual(
            [entry["step_id"] for entry in residual["step_trace"]["after"]],
            ["value"],
        )
        self.assertEqual(
            residual["fuel"],
            {
                "initial": 10,
                "before_remaining": 8,
                "after_remaining": 9,
            },
        )
        self.assertIn("global_equivalence", receipt["does_not_establish"])
        self.assertIn("authority", receipt["does_not_establish"])

    def test_target_chosen_after_comparison_refuses_before_running_cycle(self):
        result = run_positive(target=result_target(predeclared=False))
        self.assertEqual(
            (result.status, result.reason_code),
            ("REFUSE", "TARGET_NOT_PREDECLARED"),
        )
        self.assertIsNone(result.receipt["omega_cycle"])

    def test_input_drift_refuses_controlled_comparison(self):
        before = make_execution_cut(execution_data(input_digest="sha256:world-a"), fuel_initial=10)
        after = make_execution_cut(execution_data(input_digest="sha256:world-b"), fuel_initial=10)
        comparison = compare_execution_cuts(before, after, result_target())
        self.assertEqual(
            (comparison.status, comparison.reason_code),
            ("REFUSE", "INPUT_CUT_MISMATCH"),
        )
        self.assertIsNone(comparison.target_verdict)

    def test_order_erasure_control_preserves_sequence_difference(self):
        left_trace = [
            {"step_id": "a", "op": "core.get@1"},
            {"step_id": "b", "op": "core.same@1"},
        ]
        right_trace = list(reversed(left_trace))
        before = make_execution_cut(execution_data(trace=left_trace), fuel_initial=10)
        after = make_execution_cut(execution_data(trace=right_trace), fuel_initial=10)

        residual = typed_footprint_residual(before, after)
        self.assertEqual(residual["step_trace"]["before"], left_trace)
        self.assertEqual(residual["step_trace"]["after"], right_trace)
        self.assertNotEqual(residual["step_trace"]["before"], residual["step_trace"]["after"])

    def test_same_result_different_history_is_not_promoted_to_global_equivalence(self):
        result = run_positive(proposal_id="proposal-result-only-overreach")
        self.assertEqual(result.status, "OK")
        receipt = result.receipt
        self.assertEqual(receipt["target_verdict"], "EQUIVALENT_UNDER_T")
        self.assertNotEqual(
            receipt["baseline"]["execution_cut"]["step_trace"],
            receipt["candidate"]["execution_cut"]["step_trace"],
        )
        self.assertIn("global_equivalence", receipt["does_not_establish"])
        self.assertNotIn("GLOBALLY_EQUIVALENT", canonical_json_bytes(receipt).decode())

    def test_structural_admission_cannot_force_target_equivalence(self):
        trace_target = TargetFamily(
            id="T_step_trace",
            probes=("step_trace",),
            declared_before_comparison=True,
        )
        result = run_positive(
            target=trace_target,
            proposal_id="proposal-gate-target-separation",
        )

        self.assertEqual(result.status, "OK")
        self.assertEqual(result.receipt["omega_cycle"]["gate"]["status"], "ADMIT")
        self.assertEqual(result.receipt["target_verdict"], "DIFFERENT_UNDER_T")
        self.assertNotEqual(
            result.receipt["baseline"]["execution_cut"]["step_trace"],
            result.receipt["candidate"]["execution_cut"]["step_trace"],
        )

    def test_unpinned_runtime_drift_is_held_outside_claim_boundary(self):
        before = make_execution_cut(execution_data(), fuel_initial=10)
        after = make_execution_cut(execution_data(), fuel_initial=10)
        comparison = compare_execution_cuts(
            before,
            after,
            result_target(),
            same_runtime_invocation=False,
        )
        self.assertEqual(
            (comparison.status, comparison.reason_code),
            ("HOLD", "RUNTIME_BODY_UNPINNED"),
        )
        self.assertIsNone(comparison.target_verdict)

    def test_unsupported_probe_refuses_without_inventing_semantics(self):
        before = make_execution_cut(execution_data(), fuel_initial=10)
        after = make_execution_cut(execution_data(), fuel_initial=10)
        target = TargetFamily("T_ambient", ("meaning",), True)
        comparison = compare_execution_cuts(before, after, target)
        self.assertEqual(
            (comparison.status, comparison.reason_code),
            ("REFUSE", "UNSUPPORTED_TARGET_PROBE"),
        )

    def test_identical_paired_experiments_are_byte_stable(self):
        first = run_positive(proposal_id="proposal-stable-quotient")
        second = run_positive(proposal_id="proposal-stable-quotient")
        self.assertEqual(first.status, "OK")
        self.assertEqual(second.status, "OK")
        self.assertEqual(canonical_json_bytes(first.receipt), canonical_json_bytes(second.receipt))


if __name__ == "__main__":
    unittest.main()
