import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CLITests(unittest.TestCase):
    def specimen(self):
        return {
            "schema": "dogram.specimen/v0",
            "specimen_id": "cli-1",
            "operator": "delta",
            "operator_version": 1,
            "inputs": {"boundary_order": ["x"], "left": {"x": {"kind": "integer", "value": 1}}, "right": {"x": {"kind": "integer", "value": 2}}},
            "assumptions": [],
            "metadata": {},
        }

    def run_cli(self, args, stdin=None):
        return subprocess.run([sys.executable, "-m", "dogram.cli", *args], input=stdin, text=True, capture_output=True, cwd=Path(__file__).parent.parent)

    def test_stdin_and_file_produce_same_canonical_receipt(self):
        raw = json.dumps(self.specimen())
        a = self.run_cli([], raw)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write(raw); path = f.name
        b = self.run_cli([path])
        self.assertEqual(a.returncode, 0)
        self.assertEqual(a.stdout, b.stdout)
        self.assertTrue(a.stdout.endswith("\n"))
        self.assertEqual(json.loads(a.stdout)["status"], "OK")

    def test_identical_runs_are_byte_stable(self):
        raw = json.dumps(self.specimen())
        a = self.run_cli([], raw); b = self.run_cli([], raw)
        self.assertEqual(a.stdout, b.stdout)
        self.assertNotIn("timestamp", a.stdout.lower())
        self.assertNotIn("duration", a.stdout.lower())

    def test_invalid_json_is_structured_transport_refusal(self):
        result = self.run_cli([], "{")
        self.assertEqual(result.returncode, 2)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["status"], "REFUSE")
        self.assertEqual(receipt["reason_code"], "INVALID_JSON")


if __name__ == "__main__":
    unittest.main()
