from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from .canonical import canonical_json_bytes
from .engine import evaluate_specimen
from .receipt import canonical_receipt_bytes


def _transport_refusal(raw: str, reason_code: str, residual: str) -> dict:
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return {
        "schema": "dogram.receipt/v0",
        "specimen_id": None,
        "operator": "transport",
        "operator_version": 0,
        "input_digest": f"sha256:{digest}",
        "status": "REFUSE",
        "reason_code": reason_code,
        "consumed_inputs": [],
        "result": None,
        "residuals": [residual],
        "warnings": [],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m dogram.cli")
    parser.add_argument("path", nargs="?", default="-")
    args = parser.parse_args(argv)
    try:
        raw = sys.stdin.read() if args.path == "-" else Path(args.path).read_text(encoding="utf-8")
    except OSError as exc:
        receipt = _transport_refusal(args.path, "TRANSPORT_ERROR", str(exc))
        sys.stdout.buffer.write(canonical_json_bytes(receipt) + b"\n")
        return 2
    try:
        specimen = json.loads(raw)
    except json.JSONDecodeError as exc:
        receipt = _transport_refusal(raw, "INVALID_JSON", f"line {exc.lineno} column {exc.colno}")
        sys.stdout.buffer.write(canonical_json_bytes(receipt) + b"\n")
        return 2
    receipt = evaluate_specimen(specimen)
    sys.stdout.buffer.write(canonical_receipt_bytes(receipt) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
