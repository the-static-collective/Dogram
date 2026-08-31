import json
import pathlib
import unittest

from dogram.program import decode_program
from dogram.proposal import decode_proposal
from dogram.registry import build_bootstrap_registry
from dogram.vm import execute_program


ROOT = pathlib.Path(__file__).parents[1]
PROGRAM_PATH = ROOT / "dogram" / "stdlib" / "meta_remove_declared_step.mathal.json"
PROGRAM_DIGEST = "sha256:" + "a" * 64
EXECUTION_DIGEST = "sha256:" + "b" * 64


def load_program():
    return decode_program(json.loads(PROGRAM_PATH.read_text()))


class MetaMathalTests(unittest.TestCase):
    def test_native_meta_mathal_constructs_only_declared_remove_step_proposal(self):
        inputs = {
            "program_data": {
                "schema": "dogram.program-data/v0",
                "program": {},
                "program_digest": PROGRAM_DIGEST,
            },
            "execution_data": {"schema": "dogram.execution-data/v0"},
            "execution_digest": EXECUTION_DIGEST,
            "declared_target_step": "diagnostic",
            "proposal_id": "proposal-meta",
        }
        execution = execute_program(load_program(), inputs, build_bootstrap_registry())

        self.assertEqual(execution.status, "OK")
        self.assertEqual(execution.step_trace, ())
        self.assertEqual(execution.fuel_remaining, 1000)
        proposal = decode_proposal(execution.result)
        self.assertEqual(proposal.proposal_id, "proposal-meta")
        self.assertEqual(proposal.base_program_digest, PROGRAM_DIGEST)
        self.assertEqual(proposal.base_execution_digest, EXECUTION_DIGEST)
        self.assertEqual(proposal.step_id, "diagnostic")
        self.assertEqual(
            execution.consumed_input_addresses,
            (
                ("proposal_id",),
                ("program_data", "program_digest"),
                ("execution_digest",),
                ("declared_target_step",),
            ),
        )

    def test_missing_declared_target_refuses_inside_meta_vm(self):
        inputs = {
            "program_data": {
                "schema": "dogram.program-data/v0",
                "program": {},
                "program_digest": PROGRAM_DIGEST,
            },
            "execution_data": {"schema": "dogram.execution-data/v0"},
            "execution_digest": EXECUTION_DIGEST,
            "proposal_id": "proposal-meta",
        }
        execution = execute_program(load_program(), inputs, build_bootstrap_registry())
        self.assertEqual((execution.status, execution.reason_code), ("REFUSE", "ADDRESS_NOT_FOUND"))


if __name__ == "__main__":
    unittest.main()
