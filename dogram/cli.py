from __future__ import annotations
import argparse, json, sys
from .canonical import canonical_json_bytes
from .engine import evaluate_specimen
from .receipt import canonical_receipt_bytes

def _transport_refusal(code,residual):
    return {'schema':'dogram.receipt/v0','specimen_id':'transport','operator':'transport','operator_version':0,'input_digest':'sha256:unavailable','status':'REFUSE','consumed_inputs':[],'result':{},'residuals':[residual],'warnings':[],'reason_code':code}

def main(argv=None):
    p=argparse.ArgumentParser(add_help=True); p.add_argument('path',nargs='?',default='-'); ns=p.parse_args(argv)
    try:
        text=sys.stdin.read() if ns.path=='-' else open(ns.path,'r',encoding='utf-8').read()
        specimen=json.loads(text)
    except json.JSONDecodeError as e:
        sys.stdout.buffer.write(canonical_json_bytes(_transport_refusal('INVALID_JSON',f'line {e.lineno} column {e.colno}'))+b'\n'); return 2
    except OSError as e:
        sys.stdout.buffer.write(canonical_json_bytes(_transport_refusal('TRANSPORT_ERROR',str(e)))+b'\n'); return 2
    receipt=evaluate_specimen(specimen)
    sys.stdout.buffer.write(canonical_receipt_bytes(receipt)+b'\n'); return 0

if __name__=='__main__': raise SystemExit(main())
