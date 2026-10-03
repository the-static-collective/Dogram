#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

from dogram.generation_delta import (
    GenerationDeltaError,
    canonical_receipt,
    compare_generation,
)


def main() -> int:
    raw = sys.stdin.read()
    try:
        request = json.loads(raw)
        receipt = compare_generation(request)
    except (json.JSONDecodeError, GenerationDeltaError, ValueError) as exc:
        sys.stderr.write(json.dumps({
            "error": str(exc),
            "specimen": "GENERATION-DELTA-001",
        }, sort_keys=True) + "\n")
        return 2
    sys.stdout.buffer.write(canonical_receipt(receipt) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
