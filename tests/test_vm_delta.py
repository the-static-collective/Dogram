import json
import pathlib
import unittest

from dogram.delta import evaluate_delta
from dogram.program import decode_program
from dogram.registry import build_bootstrap_registry
from dogram.vm import execute_program


ROOT = pathlib.Path(__file__).parents[1]
PROGRAM_PATH = ROOT / "dogram" / "stdlib" / "delta.mathal.json"


def load_program():
    return decode_program(json.loads(PROGRAM_PATH.read_text()))


def load_fixture(name):
    path = ROOT / "tests" / "fixtures" / "delta" / name
    return json.loads(path.read_text())


class VMDeltaTests(unittest.TestCase):
    def test_existing_delta_fixtures_match_oracle(self):
        program = load_program()
        registry = build_bootstrap_registry()
        for name in ("exact-rational-delta.json", "first-opaque-break.json"):
            inputs = load_fixture(name)
            oracle_result, _ = evaluate_delta(inputs)
            vm = execute_program(program, inputs, registry)
            self.assertEqual(vm.status, "OK", name)
            self.assertEqual(vm.result, oracle_result, name)

    def test_all_same_trace_matches_nullable_oracle_result(self):
        inputs = {
            "boundary_order": ["A", "B"],
            "left": {
                "A": {"kind": "integer", "value": 7},
                "B": {"kind": "opaque", "value": "same"},
            },
            "right": {
                "A": {"kind": "integer", "value": 7},
                "B": {"kind": "opaque", "value": "same"},
            },
        }
        oracle_result, _ = evaluate_delta(inputs)
        vm = execute_program(load_program(), inputs, build_bootstrap_registry())
        self.assertEqual(vm.status, "OK")
        self.assertEqual(vm.result, oracle_result)
        self.assertIsNone(vm.result["first_difference"])


if __name__ == "__main__":
    unittest.main()
