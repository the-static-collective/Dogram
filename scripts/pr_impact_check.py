from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from dogram.repo_impact import build_repo_impact, render_impact_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two repository trees with Dogram Impact Receipt.")
    parser.add_argument("baseline")
    parser.add_argument("candidate")
    parser.add_argument("--output", default="pr-impact.json")
    args = parser.parse_args()

    impact = build_repo_impact(Path(args.baseline), Path(args.candidate))
    Path(args.output).write_text(json.dumps(impact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = render_impact_markdown(impact)
    print(summary, end="")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with Path(summary_path).open("a", encoding="utf-8") as handle:
            handle.write(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
