import json, subprocess, sys, tempfile, unittest
from pathlib import Path
SPEC={"schema":"dogram.specimen/v0","specimen_id":"cli","operator":"delta","operator_version":1,"inputs":{"boundary_order":["A"],"left":{"A":{"kind":"integer","value":1}},"right":{"A":{"kind":"integer","value":2}}},"assumptions":[],"metadata":{}}
class CliTests(unittest.TestCase):
    def run_cli(self,args,input_text=None): return subprocess.run([sys.executable,'-m','dogram.cli',*args],input=input_text,text=True,capture_output=True,cwd=Path(__file__).parent.parent)
    def test_stdin_and_file_match(self):
        text=json.dumps(SPEC); a=self.run_cli([],text); self.assertEqual(a.returncode,0)
        with tempfile.NamedTemporaryFile('w+',delete=False) as f: f.write(text); p=f.name
        b=self.run_cli([p]); self.assertEqual(b.returncode,0); self.assertEqual(a.stdout,b.stdout)
    def test_identical_runs_byte_stable(self):
        text=json.dumps(SPEC); self.assertEqual(self.run_cli([],text).stdout,self.run_cli([],text).stdout)
    def test_invalid_json_is_structured_exit_2(self):
        r=self.run_cli([],'{bad'); self.assertEqual(r.returncode,2); self.assertEqual(json.loads(r.stdout)['reason_code'],'INVALID_JSON')
