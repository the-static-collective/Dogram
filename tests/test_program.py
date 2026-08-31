import unittest

from dogram.program import ProgramDecodeError, decode_program, program_digest


class ProgramTests(unittest.TestCase):
    def test_key_order_does_not_change_program_digest(self):
        a = {
            "schema": "dogram.program/v0",
            "program_id": "test/identity",
            "program_version": 1,
            "steps": [
                {
                    "id": "s1",
                    "op": "core.same@1",
                    "args": [{"literal": 1}, {"literal": 1}],
                }
            ],
            "result": {"ref": "step", "step": "s1"},
        }
        b = {
            "result": a["result"],
            "steps": a["steps"],
            "program_version": 1,
            "program_id": "test/identity",
            "schema": "dogram.program/v0",
        }
        self.assertEqual(
            program_digest(decode_program(a)),
            program_digest(decode_program(b)),
        )

    def test_duplicate_step_ids_refuse(self):
        spec = {
            "schema": "dogram.program/v0",
            "program_id": "bad/dup",
            "program_version": 1,
            "steps": [
                {"id": "s1", "op": "core.same@1", "args": []},
                {"id": "s1", "op": "core.same@1", "args": []},
            ],
            "result": {"literal": None},
        }
        with self.assertRaises(ProgramDecodeError) as ctx:
            decode_program(spec)
        self.assertEqual(ctx.exception.reason_code, "DUPLICATE_STEP_ID")

    def test_forward_step_reference_refuses(self):
        spec = {
            "schema": "dogram.program/v0",
            "program_id": "bad/forward",
            "program_version": 1,
            "steps": [
                {
                    "id": "s1",
                    "op": "core.same@1",
                    "args": [{"ref": "step", "step": "s2"}, {"literal": 1}],
                },
                {"id": "s2", "op": "core.same@1", "args": []},
            ],
            "result": {"ref": "step", "step": "s1"},
        }
        with self.assertRaises(ProgramDecodeError) as ctx:
            decode_program(spec)
        self.assertEqual(ctx.exception.reason_code, "CYCLIC_OR_FORWARD_REFERENCE")

    def test_non_json_literal_refuses_before_execution(self):
        spec = {
            "schema": "dogram.program/v0",
            "program_id": "bad/host-object",
            "program_version": 1,
            "steps": [
                {
                    "id": "s1",
                    "op": "core.same@1",
                    "args": [{"literal": object()}, {"literal": None}],
                }
            ],
            "result": {"ref": "step", "step": "s1"},
        }
        with self.assertRaises(ProgramDecodeError) as ctx:
            decode_program(spec)
        self.assertEqual(ctx.exception.reason_code, "NON_CANONICAL_DATA")


if __name__ == "__main__":
    unittest.main()
