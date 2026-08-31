import json
import pathlib
import unittest

from dogram.canonical import canonical_json_bytes
from dogram.gate import GateLimits
from dogram.omega import OmegaConfig, run_omega_cycle
from dogram.program import decode_program
from dogram.registry import build_bootstrap_registry
from dogram.vm import VMConfig


ROOT = pathlib.Path(__file__).parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "omega"


def load_program(name):
    return decode_program(json.loads((FIXTURES / name).read_text()))


def default_inputs():
    return {
        "payload": {"value": {"kind": "integer", "value": 42}},
        "diagnostic": ["a", "b", "c"],
    }


def run_fixture(name="positive-program.json", *, target="diagnostic", proposal_id="proposal-omega", inputs=None, config=None):
    return run_omega_cycle(
        load_program(name),
        default_inputs() if inputs is None else inputs,
        target,
        proposal_id,
        build_bootstrap_registry(),
        config,
    )


class OmegaTests(unittest.TestCase):
    def test_positive_cycle_executes_reifies_meta_gates_executes_and_matches(self):
        result = run_fixture()
        self.assertEqual(result.status, "OK")
        self.assertIsNone(result.reason_code)
        receipt = result.receipt
        self.assertEqual(receipt["schema"], "dogram.omega-cycle-receipt/v0")
        self.assertEqual(receipt["gate"]["status"], "ADMIT")
        self.assertIsNone(receipt["comparison"]["first_difference"])
        self.assertNotEqual(
            receipt["program_before"]["program_digest"],
            receipt["program_after"]["program_digest"],
        )
        self.assertEqual(receipt["execution_before"]["result"], receipt["execution_after"]["result"])

    def test_execution_changed_control_preserves_result_but_changes_history(self):
        result = run_fixture(proposal_id="proposal-execution-changed")
        self.assertEqual(result.status, "OK")
        receipt = result.receipt
        self.assertEqual(receipt["execution_before"]["result"], receipt["execution_after"]["result"])
        self.assertNotEqual(receipt["execution_before_digest"], receipt["execution_after_digest"])
        self.assertNotEqual(receipt["execution_before"]["step_trace"], receipt["execution_after"]["step_trace"])
        self.assertNotEqual(receipt["execution_before"]["fuel_remaining"], receipt["execution_after"]["fuel_remaining"])
        self.assertEqual(
            receipt["execution_before"]["consumed_input_addresses"],
            [["payload"], ["diagnostic"]],
        )
        self.assertEqual(
            receipt["execution_after"]["consumed_input_addresses"],
            [["payload"]],
        )

    def test_absent_declared_target_refuses_in_meta_and_never_reaches_gate(self):
        result = run_fixture(target=None)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "META_EXECUTION_REFUSED"))
        self.assertEqual(result.receipt["meta_execution"]["status"], "REFUSE")
        self.assertIsNone(result.receipt["gate"])
        self.assertIsNone(result.receipt["execution_after"])

    def test_missing_target_is_gate_refusal_and_never_executes_candidate(self):
        result = run_fixture(target="absent")
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "TARGET_NOT_FOUND"))
        self.assertEqual(result.receipt["gate"]["status"], "REFUSE")
        self.assertIsNone(result.receipt["execution_after"])

    def test_dangling_step_is_gate_refusal(self):
        result = run_fixture("dangling-step-program.json")
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "DANGLING_STEP_REFERENCE"))
        self.assertIsNone(result.receipt["execution_after"])

    def test_dangling_result_is_gate_refusal(self):
        result = run_fixture("dangling-result-program.json")
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "DANGLING_RESULT_REFERENCE"))
        self.assertIsNone(result.receipt["execution_after"])

    def test_reification_capability_leak_stops_before_meta(self):
        inputs = default_inputs()
        inputs["capability"] = lambda: None
        result = run_fixture(inputs=inputs)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "REIFICATION_REFUSED"))
        self.assertIsNone(result.receipt["meta_execution"])
        self.assertIsNone(result.receipt["gate"])
        self.assertIsNone(result.receipt["execution_after"])

    def test_candidate_step_limit_is_structural_gate_refusal(self):
        config = OmegaConfig(gate_limits=GateLimits(max_program_steps=0))
        result = run_fixture(config=config)
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "PROGRAM_TOO_LARGE"))
        self.assertIsNone(result.receipt["execution_after"])

    def test_identical_cycles_are_byte_stable(self):
        first = run_fixture(proposal_id="proposal-stable")
        second = run_fixture(proposal_id="proposal-stable")
        self.assertEqual(canonical_json_bytes(first.receipt), canonical_json_bytes(second.receipt))

    def test_meta_is_exactly_one_execution_phase(self):
        result = run_fixture()
        self.assertEqual(result.status, "OK")
        self.assertEqual(result.receipt["meta_rounds"], 1)
        self.assertEqual(result.receipt["meta_execution"]["status"], "OK")


if __name__ == "__main__":
    unittest.main()
