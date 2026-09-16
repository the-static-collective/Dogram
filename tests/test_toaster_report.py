from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest

from dogram.render_observation import CELL_ORDER, SAMPLER
from scripts.toaster_report import analyze_run, digest, validate_plan, verified_artifact


class ToasterReportTests(unittest.TestCase):
    """Synthetic hostile handoffs; production render proof is recorded separately."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.plan = {
            "schema": "dogram.toaster-plan/v0", "experiment_id": "test", "sampler": SAMPLER,
            "source_kind": "synthetic-test", "source": self.artifact("source.wav", b"test-audio"),
            "axes": {"a": {"path": "motion.grammar", "levels": ["still", "drift"]},
                     "b": {"path": "camera.grammar", "levels": ["locked", "orbit"]}},
            "toaster": {"commit": "test-commit", "clean": True},
            "render_config": {"width": 640, "height": 360, "fps": 24, "outputProfileId": "delivery"},
            "cells": {},
        }
        self.manifest = {"schema": "dogram.toaster-render-manifest/v0", "cells": {}}
        for key in CELL_ORDER:
            score = {"seed": "test", "temporalDensity": "frozen", "motion": {"grammar": ("still", "drift")[int(key[0])]},
                     "camera": {"grammar": ("locked", "orbit")[int(key[1])]}}
            timeline = {"scoreAddress": key, "patches": []}
            canonical = json.dumps(timeline, separators=(",", ":"), sort_keys=True)
            timeline_hash = sha256(("HauntedToaster-ResolvedTimeline-v1|" + canonical).encode()).hexdigest()
            timeline.update(timelineHash=timeline_hash, canonicalJson=canonical)
            self.plan["cells"][key] = {"score": score, "score_address": key, "timeline_hash": timeline_hash}
            video = self.artifact(f"{key}.mp4", b"synthetic-video")
            receipt = {
                "schema": "full-measure.video-receipt.v1", "validation": {"accepted": True},
                "source": {"sha256": self.plan["source"]["sha256"]}, "output": {"sha256": video["sha256"]},
                "build": {"commit": "test-commit", "dirty": False}, "treatment": {},
                "canonicalExecution": {"scoreAddress": key, "timelineHash": timeline_hash},
                "render": {"width": 640, "height": 360, "framesPerSecond": 24,
                           "transportEncoding": {"profileId": "delivery"}, "visualCompiler": {}},
            }
            self.manifest["cells"][key] = {
                "video": video, "receipt": self.artifact(f"{key}.video-receipt.json", receipt),
                "score": self.artifact(f"{key}.score.json", score), "timeline": self.artifact(f"{key}.timeline.json", timeline),
                "frames": self.artifact(f"{key}.gray", bytes(2 * 32 * 18)),
            }
        self.freeze()

    def artifact(self, name, value):
        data = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True).encode()
        (self.root / name).write_bytes(data)
        return {"path": name, "sha256": sha256(data).hexdigest()}

    def freeze(self):
        self.artifact("plan.json", self.plan)
        self.manifest["plan_sha256"] = digest(self.root / "plan.json")
        self.artifact("render-manifest.json", self.manifest)

    def change_receipt(self, mutate):
        entry = self.manifest["cells"]["11"]["receipt"]
        receipt = json.loads((self.root / entry["path"]).read_text())
        mutate(receipt)
        self.manifest["cells"]["11"]["receipt"] = self.artifact(entry["path"], receipt)
        self.freeze()

    def test_replay_is_deterministic_and_supplies_public_specimens(self):
        first = analyze_run(self.root)
        self.assertEqual(first, analyze_run(self.root))
        self.assertEqual(first["status"], "OK")
        self.assertEqual(len(first["comparisons"]), 3)
        self.assertTrue(all(c["receipt"]["operator"] == "rectangle" for c in first["comparisons"].values()))

    def test_mutated_raw_frames_refuse(self):
        (self.root / "11.gray").write_bytes(bytes([1]) * 1152)
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            analyze_run(self.root)

    def test_changed_plan_refuses(self):
        self.plan["source_kind"] = "changed"
        self.artifact("plan.json", self.plan)
        with self.assertRaisesRegex(ValueError, "plan changed"):
            analyze_run(self.root)

    def test_failed_render_refuses_even_with_recomputed_artifact_hash(self):
        self.change_receipt(lambda r: r["validation"].update(accepted=False))
        with self.assertRaisesRegex(ValueError, "failed render"):
            analyze_run(self.root)

    def test_wrong_source_refuses(self):
        self.change_receipt(lambda r: r["source"].update(sha256="wrong-source"))
        with self.assertRaisesRegex(ValueError, "source differs"):
            analyze_run(self.root)

    def test_wrong_build_and_score_bindings_refuse(self):
        self.change_receipt(lambda r: r["build"].update(dirty=True))
        with self.assertRaisesRegex(ValueError, "build differs"):
            analyze_run(self.root)
        self.change_receipt(lambda r: (r["build"].update(dirty=False), r["canonicalExecution"].update(scoreAddress="wrong")))
        with self.assertRaisesRegex(ValueError, "score binding"):
            analyze_run(self.root)

    def test_nuisance_drift_and_changed_sampler_refuse(self):
        plan = deepcopy(self.plan)
        plan["cells"]["11"]["score"]["unexpected"] = 1
        with self.assertRaisesRegex(ValueError, "score drift"):
            validate_plan(plan)
        plan = deepcopy(self.plan)
        plan["sampler"]["fps"] = 12
        with self.assertRaisesRegex(ValueError, "sampler"):
            validate_plan(plan)

    def test_incomplete_rectangle_and_unequal_samples_refuse(self):
        self.manifest["cells"]["11"]["frames"] = self.artifact("11.gray", bytes(3 * 32 * 18))
        self.freeze()
        with self.assertRaisesRegex(ValueError, "same sample count"):
            analyze_run(self.root)
        del self.manifest["cells"]["11"]
        self.freeze()
        with self.assertRaisesRegex(ValueError, "incomplete rendered"):
            analyze_run(self.root)

    def test_artifact_cannot_escape_run(self):
        for name in ("../source.wav", "/source.wav", "..\\source.wav"):
            with self.assertRaises(ValueError):
                verified_artifact(self.root, {"path": name, "sha256": "anything"})
