"""Replay a declared trail with no network, geolocation or system-clock lookup.

Usage:
    python -m scripts.trail_timestamp tests/fixtures/trail_timestamp/trail-022100-git-001.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from dogram.trail_timestamp import create_trail


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay a declared Earth/sky UTC event trail")
    parser.add_argument("specimen", type=Path, help="JSON event/observer/sky fixture")
    args = parser.parse_args()
    data = json.loads(args.specimen.read_text(encoding="utf-8"))
    print(json.dumps(create_trail(data), indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
