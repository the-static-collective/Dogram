import base64
import hashlib
import io
import unittest
import wave

from dogram.generation_delta import (
    GenerationDeltaError,
    compare_generation,
)


SAMPLE_RATE = 44_100
CHANNELS = 2
BYTES_PER_FRAME = 4


def make_wav(*, seconds: float = 1.0, gain: float = 0.25, step: int = 8) -> bytes:
    frames = int(SAMPLE_RATE * seconds)
    pcm = bytearray()
    for frame in range(frames):
        phase = ((frame // step) % 2) * 2 - 1
        sample = int(phase * gain * 32767)
        pcm.extend(int(sample).to_bytes(2, "little", signed=True))
        pcm.extend(int(-sample).to_bytes(2, "little", signed=True))
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as handle:
        handle.setnchannels(CHANNELS)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(bytes(pcm))
    return buffer.getvalue()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def window(window_id: str, raw: bytes) -> dict:
    return {
        "window_id": window_id,
        "audio_sha256": sha256(raw),
        "media_type": "audio/wav",
        "base64": base64.b64encode(raw).decode("ascii"),
    }


def request(parent_raw: bytes, child_raw: bytes) -> dict:
    parent_id = "autodisco-audio-window-v0:" + "1" * 64
    child_id = "autodisco-audio-window-v0:" + "2" * 64
    return {
        "schema": "dogram.generation-delta-request/v0",
        "transform": {
            "relation": "ADMITTED_PROPOSAL_AS_NEW_AUDIO_SPECIMEN",
            "human_action": "explicit-admit",
            "parent_window_id": parent_id,
            "child_window_id": child_id,
            "proposal_receipt_hash": "sha256:" + "3" * 64,
            "audition_sha256": "sha256:" + "4" * 64,
        },
        "parent": window(parent_id, parent_raw),
        "child": window(child_id, child_raw),
    }


class GenerationDeltaTests(unittest.TestCase):
    def test_changed_carrier_reports_only_measured_axes(self):
        parent = make_wav(gain=0.20, step=12)
        child = make_wav(gain=0.55, step=5)

        receipt = compare_generation(request(parent, child))

        self.assertEqual(receipt["schema"], "dogram.generation-delta-receipt/v0")
        self.assertEqual(receipt["specimen"], "GENERATION-DELTA-001")
        self.assertEqual(receipt["status"], "OK")
        self.assertEqual(receipt["delta"]["classification"], "MEASURED_CHANGE")
        self.assertIn("rms_quartiles_q15", receipt["delta"]["changed_axes"])
        self.assertIn("peak_q15", receipt["delta"]["changed_axes"])
        self.assertIn("zero_crossing_ppm", receipt["delta"]["changed_axes"])
        self.assertIn("semantic_meaning_not_measured", receipt["residuals"])
        self.assertIn("listener_effect_not_measured_here", receipt["residuals"])
        self.assertIn("DELTA != VALUE", receipt["laws"])
        self.assertTrue(receipt["receipt_hash"].startswith("sha256:"))

    def test_identical_carrier_under_distinct_window_ids_is_no_measured_change(self):
        raw = make_wav()

        receipt = compare_generation(request(raw, raw))

        self.assertEqual(receipt["delta"]["classification"], "NO_MEASURED_CHANGE")
        self.assertEqual(receipt["delta"]["changed_axes"], [])
        self.assertEqual(
            set(receipt["delta"]["unchanged_axes"]),
            {
                "frame_count",
                "duration_ms_floor",
                "duration_frame_remainder",
                "rms_quartiles_q15",
                "peak_q15",
                "zero_crossing_ppm",
            },
        )
        self.assertNotEqual(
            receipt["transform"]["parent_window_id"],
            receipt["transform"]["child_window_id"],
        )

    def test_duration_change_is_exactly_receipted_without_semantic_inference(self):
        parent = make_wav(seconds=1.0)
        child = make_wav(seconds=0.75)

        receipt = compare_generation(request(parent, child))

        self.assertEqual(receipt["delta"]["axes"]["frame_count"], -11025)
        self.assertEqual(receipt["delta"]["axes"]["duration_ms_floor"], -250)
        self.assertIn("frame_count", receipt["delta"]["changed_axes"])
        self.assertIn("MEASURED CHANGE != MUSICAL MEANING", receipt["laws"])

    def test_tampered_audio_digest_refuses(self):
        req = request(make_wav(), make_wav(gain=0.4))
        req["child"]["audio_sha256"] = "f" * 64

        with self.assertRaisesRegex(GenerationDeltaError, "audio digest mismatch"):
            compare_generation(req)

    def test_lineage_ids_must_bind_exact_windows(self):
        req = request(make_wav(), make_wav(gain=0.4))
        req["transform"]["child_window_id"] = (
            "autodisco-audio-window-v0:" + "9" * 64
        )

        with self.assertRaisesRegex(
            GenerationDeltaError,
            "transform child does not match child window",
        ):
            compare_generation(req)

    def test_explicit_human_admission_is_required(self):
        req = request(make_wav(), make_wav(gain=0.4))
        req["transform"]["human_action"] = "automatic"

        with self.assertRaisesRegex(
            GenerationDeltaError,
            "requires explicit admission",
        ):
            compare_generation(req)

    def test_receipt_is_deterministic(self):
        req = request(make_wav(gain=0.18), make_wav(gain=0.36, step=6))

        first = compare_generation(req)
        second = compare_generation(req)

        self.assertEqual(first, second)
        self.assertEqual(first["receipt_hash"], second["receipt_hash"])


if __name__ == "__main__":
    unittest.main()
