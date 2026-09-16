"""Run/replay the opt-in local Toaster paired-control experiment.

python -m scripts.toaster_report NEW_RUN --toaster ../the-haunted-toaster
python -m scripts.toaster_report EXISTING_RUN
"""

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from dogram.canonical import sha256_json
from dogram.render_observation import CELL_ORDER, SAMPLER, compare_observations, observe_frames


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(file):
    return json.loads(file.read_text(encoding="utf-8"))


def digest(file):
    result = sha256()
    with file.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def verified_artifact(root, entry):
    name = entry["path"]
    require(isinstance(name, str) and Path(name).name == name and "\\" not in name, "artifact must be a sibling filename")
    file = (root / name).resolve()
    require(file.parent == root.resolve() and file.is_file(), "artifact must stay inside the run directory")
    require(digest(file) == entry["sha256"], f"artifact hash mismatch: {name}")
    return file


def without_axes(score):
    common = deepcopy(score)
    del common["motion"]["grammar"]
    del common["camera"]["grammar"]
    return common


def validate_plan(plan):
    require(plan["schema"] == "dogram.toaster-plan/v0", "unsupported plan schema")
    require(plan["sampler"] == SAMPLER, "unsupported or changed sampler")
    require(plan["axes"] == {"a": {"path": "motion.grammar", "levels": ["still", "drift"]},
                             "b": {"path": "camera.grammar", "levels": ["locked", "orbit"]}}, "unsupported axes")
    require(set(plan["cells"]) == set(CELL_ORDER), "incomplete planned rectangle")
    require(plan["toaster"]["clean"] is True, "Toaster code must be attributable to a clean checkout")
    base = without_axes(plan["cells"]["00"]["score"])
    for key in CELL_ORDER:
        score = plan["cells"][key]["score"]
        require(without_axes(score) == base, "undeclared score drift")
        require(score["seed"] == plan["experiment_id"], "seed mismatch")
        require(score["temporalDensity"] == "frozen", "patch-producing mode is not admitted")
        require(score["motion"]["grammar"] == ("still", "drift")[int(key[0])], "wrong motion cell")
        require(score["camera"]["grammar"] == ("locked", "orbit")[int(key[1])], "wrong camera cell")


def analyze_run(root):
    root = Path(root).resolve()
    plan = read_json(root / "plan.json")
    manifest = read_json(root / "render-manifest.json")
    validate_plan(plan)
    plan_hash = digest(root / "plan.json")
    require(manifest["schema"] == "dogram.toaster-render-manifest/v0", "unsupported manifest schema")
    require(manifest["plan_sha256"] == plan_hash, "plan changed after rendering")
    require(set(manifest["cells"]) == set(CELL_ORDER), "incomplete rendered rectangle")
    verified_artifact(root, plan["source"])
    observations = {}
    render_evidence = {}
    for key in CELL_ORDER:
        entries = manifest["cells"][key]
        require(set(entries) == {"video", "receipt", "score", "timeline", "frames"}, "incomplete artifact set")
        files = {name: verified_artifact(root, entry) for name, entry in entries.items()}
        receipt, score, timeline = (read_json(files[name]) for name in ("receipt", "score", "timeline"))
        expected = plan["cells"][key]
        require(receipt["schema"] == "full-measure.video-receipt.v1", "unsupported Toaster receipt")
        require(receipt["validation"]["accepted"] is True, "failed render is not an observation")
        require(receipt["source"]["sha256"] == plan["source"]["sha256"], "source differs across cells")
        require(receipt["output"]["sha256"] == entries["video"]["sha256"], "video differs from receipt")
        require(receipt["build"]["commit"] == plan["toaster"]["commit"] and receipt["build"]["dirty"] is False, "Toaster build differs from plan")
        require(score == expected["score"], "accepted score differs from plan")
        require(receipt["canonicalExecution"]["scoreAddress"] == timeline["scoreAddress"] == expected["score_address"], "score binding mismatch")
        require(receipt["canonicalExecution"]["timelineHash"] == timeline["timelineHash"] == expected["timeline_hash"], "timeline binding mismatch")
        require(timeline["patches"] == [], "unexpected resolver patches")
        body = {k: v for k, v in timeline.items() if k not in ("canonicalJson", "timelineHash")}
        require(json.loads(timeline["canonicalJson"]) == body, "timeline canonical body mismatch")
        require(sha256(("HauntedToaster-ResolvedTimeline-v1|" + timeline["canonicalJson"]).encode()).hexdigest() == expected["timeline_hash"], "timeline digest mismatch")
        for dimension, field in (("width", "width"), ("height", "height"), ("fps", "framesPerSecond")):
            require(receipt["render"][field] == plan["render_config"][dimension], "render geometry differs from plan")
        require(receipt["render"]["transportEncoding"]["profileId"] == plan["render_config"]["outputProfileId"], "transport differs from plan")
        require(files["frames"].stat().st_size <= 200 * SAMPLER["width"] * SAMPLER["height"], "sample exceeds bounded 30-second experiment")
        observations[key] = observe_frames(files["frames"].read_bytes())
        render_evidence[key] = {
            "artifacts": entries,
            "score_address": expected["score_address"], "timeline_hash": expected["timeline_hash"],
            "typography": receipt["treatment"].get("typography"),
            "visual_compiler": receipt["render"]["visualCompiler"],
        }
    comparisons = compare_observations(observations, plan["experiment_id"], "motion.grammar", "camera.grammar")
    return {
        "schema": "dogram.toaster-observation/v0", "status": "OK", "authority_boundary": "comparison-only",
        "plan_sha256": plan_hash, "manifest_sha256": digest(root / "render-manifest.json"),
        "experiment_id": plan["experiment_id"], "source_kind": plan["source_kind"], "toaster": plan["toaster"],
        "sampler": SAMPLER, "render_evidence": render_evidence, "observations": observations,
        "comparisons": comparisons,
        "limitations": [
            "Measures decoded delivery pixels, including compression and score-seeded typography, not isolated optical motion.",
            "Coverage is visitation of 256 declared left/right mean-luma bin pairs, not coverage of all images or artistic novelty.",
            "A sampled period requires two repetitions and agreement across every retained sample; sampling/quantization may hide motion.",
            "No sampled period means none witnessed in this finite window; it does not establish nonperiodicity.",
            "One seed and one source are a bounded specimen, not a general effect, causal verdict or preference ranking.",
            "Hashes bind retained artifacts; they do not authenticate their author or independently prove decoder execution.",
        ],
    }


def display_scalar(value):
    return str(value["value"]) if value["kind"] == "integer" else f"{value['numerator']}/{value['denominator']}"


def markdown(report):
    rows = ["# Toaster paired-render observation", "", f"Experiment: `{report['experiment_id']}`", "",
            "| Cell | Frames | Unique quantized frames | Visited luma states / 256 | Sampled period |",
            "| --- | ---: | ---: | ---: | ---: |"]
    for key in CELL_ORDER:
        obs = report["observations"][key]
        rows.append(f"| {key} | {obs['frame_count']} | {obs['unique_quantized_frames']} | {len(obs['visited_split_luma_states'])} | {obs['smallest_sampled_period'] or 'not witnessed'} |")
    rows += ["", "00 = still/locked; 01 = still/orbit; 10 = drift/locked; 11 = drift/orbit.", "",
             "Mixed differences use `11 - 10 - 01 + 00` on each declared metric:", ""]
    for name, comparison in report["comparisons"].items():
        result = comparison["receipt"]["result"]
        rows.append(f"- `{name}`: **{display_scalar(result['mixed_delta'])}**")
    rows += ["", *[f"- {item}" for item in report["limitations"]], ""]
    return "\n".join(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--toaster", type=Path, help="render a new four-cell run using this clean local checkout")
    parser.add_argument("--audio", type=Path, help="optional 1–30 second audio excerpt; default is a 4-second synthetic control")
    parser.add_argument("--seed", default="dogram-toaster-pair-001")
    args = parser.parse_args()
    if args.audio and not args.toaster:
        parser.error("--audio requires --toaster")
    if args.toaster:
        command = ["node", str(Path(__file__).with_name("toaster_experiment.cjs")), "--toaster", str(args.toaster.resolve()),
                   "--out", str(args.run.resolve()), "--seed", args.seed]
        if args.audio:
            command += ["--audio", str(args.audio.resolve())]
        subprocess.run(command, check=True)
    report = analyze_run(args.run)
    report["analysis_code"] = {str(file.relative_to(Path(__file__).resolve().parents[1])): digest(file)
                               for file in (Path(__file__).resolve(), Path(__file__).resolve().parents[1] / "dogram/render_observation.py")}
    report["report_digest"] = sha256_json(report)
    # Analysis never overwrites prior reports. Replays print the deterministic result.
    target = args.run / "report.json"
    encoded = json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if target.exists():
        require(target.read_text(encoding="utf-8") == encoded, "existing report differs; retain it and use analyze_run() to inspect the delta")
    else:
        with target.open("x", encoding="utf-8") as stream:
            stream.write(encoded)
        with (args.run / "report.md").open("x", encoding="utf-8") as stream:
            stream.write(markdown(report))
    print(markdown(report), end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        print(f"REFUSE: {error}", file=sys.stderr)
        raise SystemExit(1)
