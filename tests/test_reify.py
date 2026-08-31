import unittest

from dogram.canonical import canonical_json_bytes, sha256_json
from dogram.program import decode_program, encode_program, program_digest
from dogram.registry import build_bootstrap_registry
from dogram.reify import ReificationError, reify_execution, reify_program
from dogram.vm import execute_program


def simple_program():
    return decode_program(
        {
            "schema": "dogram.program/v0",
            "program_id": "test/reify",
            "program_version": 1,
            "steps": [
                {
                    "id": "same",
                    "op": "core.same@1",
                    "args": [
                        {"ref": "input", "path": ["left"]},
                        {"ref": "input", "path": ["right"]},
                    ],
                }
            ],
            "result": {"ref": "step", "step": "same"},
        }
    )


class ReifyTests(unittest.TestCase):
    def test_program_reification_is_inert_and_digest_bound(self):
        program = simple_program()
        data = reify_program(program)
        self.assertEqual(data["schema"], "dogram.program-data/v0")
        self.assertEqual(data["program"], encode_program(program))
        self.assertEqual(data["program_digest"], program_digest(program))
        canonical_json_bytes(data)

    def test_execution_reification_binds_program_input_and_runtime_receipt(self):
        program = simple_program()
        inputs = {"left": 4, "right": 4}
        execution = execute_program(program, inputs, build_bootstrap_registry())

        data, digest = reify_execution(program, inputs, execution)

        self.assertEqual(data["schema"], "dogram.execution-data/v0")
        self.assertEqual(data["program_digest"], program_digest(program))
        self.assertEqual(data["input_digest"], sha256_json(inputs))
        self.assertEqual(data["status"], "OK")
        self.assertIs(data["result"], True)
        self.assertEqual(data["consumed_input_addresses"], [["left"], ["right"]])
        self.assertEqual(digest, sha256_json(data))

    def test_identical_execution_reification_is_byte_stable(self):
        program = simple_program()
        inputs = {"right": 4, "left": 4}
        first_execution = execute_program(program, inputs, build_bootstrap_registry())
        second_execution = execute_program(program, inputs, build_bootstrap_registry())

        first_data, first_digest = reify_execution(program, inputs, first_execution)
        second_data, second_digest = reify_execution(program, inputs, second_execution)

        self.assertEqual(canonical_json_bytes(first_data), canonical_json_bytes(second_data))
        self.assertEqual(first_digest, second_digest)

    def test_reification_fails_closed_on_live_capability_in_input_state(self):
        program = simple_program()
        inputs = {"left": 4, "right": 4, "capability": lambda: None}
        execution = execute_program(program, inputs, build_bootstrap_registry())

        with self.assertRaises(ReificationError) as raised:
            reify_execution(program, inputs, execution)

        self.assertEqual(raised.exception.reason_code, "NON_CANONICAL_REIFICATION")
        self.assertNotIn("<function", raised.exception.residual)


if __name__ == "__main__":
    unittest.main()
