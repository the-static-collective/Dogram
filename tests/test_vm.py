import unittest

from dogram.program import decode_program
from dogram.registry import build_bootstrap_registry
from dogram.vm import VMConfig, execute_program


class VMTests(unittest.TestCase):
    def test_executes_one_step_and_traces_automatically(self):
        program = decode_program(
            {
                "schema": "dogram.program/v0",
                "program_id": "test/same",
                "program_version": 1,
                "steps": [
                    {
                        "id": "s1",
                        "op": "core.same@1",
                        "args": [{"literal": 7}, {"literal": 7}],
                    }
                ],
                "result": {"ref": "step", "step": "s1"},
            }
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


if __name__ == "__main__":
    unittest.main()
