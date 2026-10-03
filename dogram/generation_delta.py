"""GENERATION-DELTA-001: finite transform measurement between bounded audio generations.

This is an internal research instrument, not a new public Dogram operator.

It compares exact canonical PCM carriers that already have an explicit declared
parent -> descendant relation. It measures the transform and leaves semantics,
quality, value, and listener effect unresolved.
"""
from __future__ import annotations

import base64
import hashlib
import io
import json
import math
import wave
from typing import Any

from .canonical import sha256_json


REQUEST_SCHEMA = "dogram.generation-delta-request/v0"
RECEIPT_SCHEMA = "dogram.generation-delta-receipt/v0"
RELATION = "ADMITTED_PROPOSAL_AS_NEW_AUDIO_SPECIMEN"
SAMPLE_RATE = 44_100
CHANNELS = 2
SAMPLE_WIDTH_BYTES = 2
BYTES_PER_FRAME = CHANNELS * SAMPLE_WIDTH_BYTES
MAX_AUDIO_BYTES = 12 * 1024 * 1024


class GenerationDeltaError(ValueError):
    pass


def _exact_keys(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise GenerationDeltaError(f"{label} must be an object")
    if set(value) != keys:
        raise GenerationDeltaError(f"{label} has unexpected fields")
    return value


def _decode_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise GenerationDeltaError(f"{label} must be a SHA-256 hex string")
    raw = value[7:] if value.startswith("sha256:") else value
    if len(raw) != 64 or any(ch not in "0123456789abcdef" for ch in raw):
        raise GenerationDeltaError(f"{label} must be lowercase SHA-256")
    return raw


def _decode_window(value: Any, label: str) -> tuple[dict[str, Any], bytes]:
    window = _exact_keys(
        value,
        {
            "window_id",
            "audio_sha256",
            "media_type",
            "base64",
        },
        label,
    )
    window_id = window["window_id"]
    if (
        not isinstance(window_id, str)
        or not window_id.startswith("autodisco-audio-window-v0:")
    ):
        raise GenerationDeltaError(f"{label}.window_id is invalid")
    if window["media_type"] != "audio/wav":
        raise GenerationDeltaError(f"{label}.media_type must be audio/wav")
    expected = _decode_sha256(window["audio_sha256"], f"{label}.audio_sha256")
    encoded = window["base64"]
    if not isinstance(encoded, str):
        raise GenerationDeltaError(f"{label}.base64 must be a string")
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (ValueError, TypeError) as exc:
        raise GenerationDeltaError(f"{label}.base64 is invalid") from exc
    if not raw or len(raw) > MAX_AUDIO_BYTES:
        raise GenerationDeltaError(f"{label} audio size is outside the bounded carrier")
    if hashlib.sha256(raw).hexdigest() != expected:
        raise GenerationDeltaError(f"{label} audio digest mismatch")
    return window, raw


def _pcm(raw: bytes, label: str) -> tuple[bytes, int]:
    try:
        with wave.open(io.BytesIO(raw), "rb") as handle:
            channels = handle.getnchannels()
            width = handle.getsampwidth()
            rate = handle.getframerate()
            frames = handle.getnframes()
            compression = handle.getcomptype()
            pcm = handle.readframes(frames)
    except (wave.Error, EOFError) as exc:
        raise GenerationDeltaError(f"{label} is not a readable PCM WAV") from exc

    if (
        channels != CHANNELS
        or width != SAMPLE_WIDTH_BYTES
        or rate != SAMPLE_RATE
        or compression != "NONE"
        or frames <= 0
    ):
        raise GenerationDeltaError(
            f"{label} must be 44.1kHz stereo 16-bit uncompressed PCM"
        )
    if len(pcm) != frames * BYTES_PER_FRAME:
        raise GenerationDeltaError(f"{label} PCM frame count mismatch")
    return pcm, frames


def _q15_rms(sum_squares: int, sample_count: int) -> int:
    if sample_count <= 0:
        return 0
    # Integer sqrt keeps the measurement deterministic and avoids float
    # serialization differences. Samples are already signed 16-bit integers.
    mean_square = sum_squares // sample_count
    return min(32767, math.isqrt(mean_square))


def _profile(pcm: bytes, frame_count: int) -> dict[str, Any]:
    quarter_sum_squares = [0, 0, 0, 0]
    quarter_sample_counts = [0, 0, 0, 0]
    peak = 0
    zero_crossings = 0
    previous_left: int | None = None

    for frame in range(frame_count):
        offset = frame * BYTES_PER_FRAME
        left = int.from_bytes(pcm[offset : offset + 2], "little", signed=True)
        right = int.from_bytes(pcm[offset + 2 : offset + 4], "little", signed=True)
        quarter = min(3, (frame * 4) // frame_count)

        quarter_sum_squares[quarter] += left * left + right * right
        quarter_sample_counts[quarter] += 2
        peak = max(peak, abs(left), abs(right))

        if previous_left is not None and (
            (previous_left < 0 <= left) or (previous_left >= 0 > left)
        ):
            zero_crossings += 1
        previous_left = left

    rms_quartiles_q15 = [
        _q15_rms(total, count)
        for total, count in zip(quarter_sum_squares, quarter_sample_counts)
    ]
    zero_crossing_ppm = (
        (zero_crossings * 1_000_000) // max(1, frame_count - 1)
    )

    return {
        "frame_count": frame_count,
        "duration_ms_floor": (frame_count * 1000) // SAMPLE_RATE,
        "duration_frame_remainder": (frame_count * 1000) % SAMPLE_RATE,
        "rms_quartiles_q15": rms_quartiles_q15,
        "peak_q15": min(32767, peak),
        "zero_crossing_ppm": zero_crossing_ppm,
    }


def _delta(parent: dict[str, Any], child: dict[str, Any]) -> dict[str, Any]:
    axes = {
        "frame_count": child["frame_count"] - parent["frame_count"],
        "duration_ms_floor": (
            child["duration_ms_floor"] - parent["duration_ms_floor"]
        ),
        "duration_frame_remainder": (
            child["duration_frame_remainder"] - parent["duration_frame_remainder"]
        ),
        "rms_quartiles_q15": [
            right - left
            for left, right in zip(
                parent["rms_quartiles_q15"],
                child["rms_quartiles_q15"],
            )
        ],
        "peak_q15": child["peak_q15"] - parent["peak_q15"],
        "zero_crossing_ppm": (
            child["zero_crossing_ppm"] - parent["zero_crossing_ppm"]
        ),
    }
    changed: list[str] = []
    unchanged: list[str] = []
    for key, value in axes.items():
        nonzero = any(item != 0 for item in value) if isinstance(value, list) else value != 0
        (changed if nonzero else unchanged).append(key)

    return {
        "axes": axes,
        "changed_axes": changed,
        "unchanged_axes": unchanged,
        "classification": "MEASURED_CHANGE" if changed else "NO_MEASURED_CHANGE",
    }


def compare_generation(request: dict[str, Any]) -> dict[str, Any]:
    request = _exact_keys(
        request,
        {"schema", "transform", "parent", "child"},
        "request",
    )
    if request["schema"] != REQUEST_SCHEMA:
        raise GenerationDeltaError("unsupported generation-delta request schema")

    transform = _exact_keys(
        request["transform"],
        {
            "relation",
            "human_action",
            "parent_window_id",
            "child_window_id",
            "proposal_receipt_hash",
            "audition_sha256",
        },
        "transform",
    )
    if transform["relation"] != RELATION:
        raise GenerationDeltaError("unsupported generation relation")
    if transform["human_action"] != "explicit-admit":
        raise GenerationDeltaError("generation comparison requires explicit admission")
    proposal_receipt_hash = _decode_sha256(
        transform["proposal_receipt_hash"],
        "transform.proposal_receipt_hash",
    )
    audition_sha256 = _decode_sha256(
        transform["audition_sha256"],
        "transform.audition_sha256",
    )

    parent_window, parent_raw = _decode_window(request["parent"], "parent")
    child_window, child_raw = _decode_window(request["child"], "child")

    if transform["parent_window_id"] != parent_window["window_id"]:
        raise GenerationDeltaError("transform parent does not match parent window")
    if transform["child_window_id"] != child_window["window_id"]:
        raise GenerationDeltaError("transform child does not match child window")
    if transform["parent_window_id"] == transform["child_window_id"]:
        raise GenerationDeltaError("parent and child window identities must differ")

    # The admitted proposal audition is the source file from which the child
    # AUDIO WINDOW was cut. Its digest does not have to equal the child window
    # digest when a sub-millisecond tail was lawfully excluded.
    if not audition_sha256:
        raise GenerationDeltaError("transform audition digest is required")

    parent_pcm, parent_frames = _pcm(parent_raw, "parent")
    child_pcm, child_frames = _pcm(child_raw, "child")
    parent_profile = _profile(parent_pcm, parent_frames)
    child_profile = _profile(child_pcm, child_frames)
    measured_delta = _delta(parent_profile, child_profile)

    body = {
        "schema": RECEIPT_SCHEMA,
        "specimen": "GENERATION-DELTA-001",
        "status": "OK",
        "transform": {
            "relation": RELATION,
            "human_action": "explicit-admit",
            "parent_window_id": parent_window["window_id"],
            "child_window_id": child_window["window_id"],
            "proposal_receipt_hash": f"sha256:{proposal_receipt_hash}",
            "audition_sha256": f"sha256:{audition_sha256}",
        },
        "parent": {
            "window_id": parent_window["window_id"],
            "audio_sha256": f"sha256:{_decode_sha256(parent_window['audio_sha256'], 'parent.audio_sha256')}",
            "profile": parent_profile,
        },
        "child": {
            "window_id": child_window["window_id"],
            "audio_sha256": f"sha256:{_decode_sha256(child_window['audio_sha256'], 'child.audio_sha256')}",
            "profile": child_profile,
        },
        "delta": measured_delta,
        "residuals": [
            "pitch_or_key_not_measured",
            "harmony_not_measured",
            "source_instrumentation_not_measured",
            "semantic_meaning_not_measured",
            "musical_value_not_measured",
            "listener_effect_not_measured_here",
        ],
        "laws": [
            "DOGRAM MEASURES TRANSFORMS, NOT PEOPLE",
            "DELTA != VALUE",
            "MEASURED CHANGE != MUSICAL MEANING",
            "RESIDUAL != FAILURE",
            "DESCENDANT != PARENT",
            "ANCESTRY != AUTHORITY",
            "DO NOT DECIDE WHAT IT MEANS",
        ],
    }
    return {
        **body,
        "receipt_hash": sha256_json(body),
    }


def canonical_receipt(receipt: dict[str, Any]) -> bytes:
    return json.dumps(
        receipt,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
