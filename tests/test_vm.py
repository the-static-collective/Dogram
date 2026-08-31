import unittest

from dogram.canonical import canonical_json_bytes
from dogram.program import decode_program
from dogram.registry import build_bootstrap_registry
from dogram.vm import VMConfig, execute_program


def program_with_step(op, args, *, result=None):
    return decode_program(
        {
            "schema": "dogram.program/v0",
            "program_id": "test/program",
            "program_version": 1,
            "steps": [{"id": "s1", "op": op, "args": args}],
            "result": result or {"ref": "step", "step": "s1"},
        }
    )


class VMTests(unittest.TestCase):
    def test_executes_one_step_and_traces_automatically(self):
        program = program_with_step(
            "core.same@1",
            [{"literal": 7}, {"literal": 7}],
        )
        result = execute_program(
            program,
            {},
            build_bootstrap_registry(),
            VMConfig(max_exec_steps=2),
        )
        self.assertEqual(result.status, "OK")
        self.assertIs(result.result, True)
        self.assertEqual(result.step_trace[0].step_id, "s1")
        self.assertEqual(result.fuel_remaining, 1)

    def test_unknown_operation_refuses(self):
        program = program_with_step("host.eval@1", [])
        result = execute_program(program, {}, build_bootstrap_registry())
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "UNKNOWN_OPERATION"))

    def test_fuel_exhaustion_refuses_before_dispatch(self):
        program = program_with_step("core.same@1", [{"literal": 1}, {"literal": 1}])
        result = execute_program(
            program,
            {},
            build_bootstrap_registry(),
            VMConfig(max_exec_steps=0),
        )
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "FUEL_EXHAUSTED"))
        self.assertEqual(result.step_trace, ())

    def test_bad_input_path_refuses(self):
        program = program_with_step(
            "core.same@1",
            [{"ref": "input", "path": ["missing"]}, {"literal": 1}],
        )
        result = execute_program(program, {}, build_bootstrap_registry())
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "ADDRESS_NOT_FOUND"))

    def test_intrinsic_refusal_is_preserved(self):
        program = program_with_step("core.select_first@1", [{"literal": []}])
        result = execute_program(program, {}, build_bootstrap_registry())
        self.assertEqual((result.status, result.reason_code), ("REFUSE", "EMPTY_SEQUENCE"))
        self.assertEqual(result.fuel_remaining, 999)

    def test_identical_execution_payloads_are_byte_stable(self):
        program = program_with_step(
            "core.same@1",
            [{"literal": {"b": 2, "a": 1}}, {"literal": {"a": 1, "b": 2}}],
        )
        first = execute_program(program, {}, build_bootstrap_registry())
        second = execute_program(program, {}, build_bootstrap_registry())
        self.assertEqual(
            canonical_json_bytes(first.to_data()),
            canonical_json_bytes(second.to_data()),
        )


if __name__ == "__main__":
    unittest.main()
