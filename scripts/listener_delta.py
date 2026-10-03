#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

from dogram.listener_delta import ListenerDeltaError, compare_listener_responses


def main() -> int:
    try:
        request = json.loads(sys.stdin.read())
        receipt = compare_listener_responses(request)
    except (json.JSONDecodeError, ListenerDeltaError, ValueError) as exc:
        sys.stderr.write(json.dumps({
            "error": str(exc),
            "specimen": "LISTENER-DELTA-001",
        }, sort_keys=True) + "\n")
        return 2
    sys.stdout.write(
        json.dumps(
            receipt,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
