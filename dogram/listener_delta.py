"""LISTENER-DELTA-001: finite transform measurement between sealed first-listen responses.

This is an internal research instrument, not a new public Dogram operator.

It compares the same declared listener identities across an explicit parent ->
descendant audio relation. It measures only response structure and exact lexical
differences. It does not infer semantic similarity, preference, quality, or a
causal effect of the audio transform.
"""
from __future__ import annotations

from collections import Counter
import re
import unicodedata
from typing import Any

from .canonical import sha256_json


REQUEST_SCHEMA = "dogram.listener-delta-request/v0"
RECEIPT_SCHEMA = "dogram.listener-delta-receipt/v0"
SEALED_SCHEMA = "autodisco.audio-look-twice-first-response/v0"
RELATION = "ADMITTED_PROPOSAL_AS_NEW_AUDIO_SPECIMEN"
MODES = ("OBSERVED", "DERIVED", "METAPHOR", "INTERPRETATION")
MAX_TEXT_CHARS = 2_000
MAX_TOTAL_TEXT_CHARS = 20_000
_TOKEN_RE = re.compile(r"[\w']+", flags=re.UNICODE)


class ListenerDeltaError(ValueError):
    pass


def _exact_keys(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ListenerDeltaError(f"{label} must be an object")
    if set(value) != keys:
        raise ListenerDeltaError(f"{label} has unexpected fields")
    return value


def _digest_hex(value: Any) -> str:
    digest = sha256_json(value)
    if not digest.startswith("sha256:"):
        raise ListenerDeltaError("internal digest format mismatch")
    return digest.split(":", 1)[1]


def _decode_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise ListenerDeltaError(f"{label} must be a SHA-256 hex string")
    raw = value[7:] if value.startswith("sha256:") else value
    if len(raw) != 64 or any(ch not in "0123456789abcdef" for ch in raw):
        raise ListenerDeltaError(f"{label} must be lowercase SHA-256")
    return raw


def _normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value)
    return " ".join(normalized.strip().split()).casefold()


def _tokens(value: str) -> list[str]:
    return sorted(set(_TOKEN_RE.findall(_normalize_text(value))))


def _validate_response(value: Any, label: str) -> dict[str, Any]:
    response = _exact_keys(
        value,
        {"observations", "lingering_intrigue", "closing_line"},
        label,
    )
    observations = response["observations"]
    if (
        not isinstance(observations, list)
        or not 2 <= len(observations) <= 8
    ):
        raise ListenerDeltaError(f"{label}.observations must contain 2 to 8 items")

    total_chars = 0
    for index, raw in enumerate(observations):
        item = _exact_keys(raw, {"mode", "text"}, f"{label}.observations[{index}]")
        if item["mode"] not in MODES:
            raise ListenerDeltaError(f"{label}.observations[{index}].mode is invalid")
        text = item["text"]
        if (
            not isinstance(text, str)
            or not text.strip()
            or len(text) > MAX_TEXT_CHARS
        ):
            raise ListenerDeltaError(f"{label}.observations[{index}].text is invalid")
        total_chars += len(text)

    intrigue = response["lingering_intrigue"]
    if type(intrigue) is not bool:
        raise ListenerDeltaError(f"{label}.lingering_intrigue must be boolean")

    closing = response["closing_line"]
    if (
        not isinstance(closing, str)
        or not closing.strip()
        or len(closing) > MAX_TEXT_CHARS
    ):
        raise ListenerDeltaError(f"{label}.closing_line is invalid")
    total_chars += len(closing)
    if total_chars > MAX_TOTAL_TEXT_CHARS:
        raise ListenerDeltaError(f"{label} exceeds bounded text size")
    return response


def _validate_sealed(value: Any, label: str) -> dict[str, Any]:
    sealed = _exact_keys(
        value,
        {
            "schema",
            "pair_id",
            "packet_id",
            "listener",
            "window_id",
            "audio_sha256",
            "model_used",
            "response_sha256",
            "response",
            "laws",
            "first_response_id",
        },
        label,
    )
    if sealed["schema"] != SEALED_SCHEMA:
        raise ListenerDeltaError(f"{label}.schema is invalid")
    if (
        not isinstance(sealed["pair_id"], str)
        or not sealed["pair_id"].startswith("autodisco-audio-look-twice-pair-v0:")
    ):
        raise ListenerDeltaError(f"{label}.pair_id is invalid")
    if (
        not isinstance(sealed["packet_id"], str)
        or not sealed["packet_id"].startswith("autodisco-audio-look-twice-first-v0:")
    ):
        raise ListenerDeltaError(f"{label}.packet_id is invalid")

    listener = sealed["listener"]
    if not isinstance(listener, dict):
        raise ListenerDeltaError(f"{label}.listener must be an object")
    listener_id = listener.get("id")
    if not isinstance(listener_id, str) or not listener_id:
        raise ListenerDeltaError(f"{label}.listener.id is invalid")

    window_id = sealed["window_id"]
    if (
        not isinstance(window_id, str)
        or not window_id.startswith("autodisco-audio-window-v0:")
    ):
        raise ListenerDeltaError(f"{label}.window_id is invalid")
    _decode_sha256(sealed["audio_sha256"], f"{label}.audio_sha256")

    model_used = sealed["model_used"]
    if not isinstance(model_used, str) or not model_used.strip():
        raise ListenerDeltaError(f"{label}.model_used is invalid")

    response = _validate_response(sealed["response"], f"{label}.response")
    expected_response_hash = _digest_hex(response)
    response_hash = _decode_sha256(
        sealed["response_sha256"],
        f"{label}.response_sha256",
    )
    if response_hash != expected_response_hash:
        raise ListenerDeltaError(f"{label}.response_sha256 mismatch")

    laws = sealed["laws"]
    if not isinstance(laws, list) or not all(isinstance(item, str) for item in laws):
        raise ListenerDeltaError(f"{label}.laws is invalid")

    first_response_id = sealed["first_response_id"]
    if (
        not isinstance(first_response_id, str)
        or not first_response_id.startswith(
            "autodisco-audio-look-twice-response-v0:"
        )
    ):
        raise ListenerDeltaError(f"{label}.first_response_id is invalid")
    body = {
        key: sealed[key]
        for key in sealed
        if key != "first_response_id"
    }
    expected_first_id = (
        "autodisco-audio-look-twice-response-v0:" + _digest_hex(body)
    )
    if first_response_id != expected_first_id:
        raise ListenerDeltaError(f"{label}.first_response_id mismatch")
    return sealed


def _validate_generation(
    values: Any,
    label: str,
    expected_window_id: str,
) -> dict[str, dict[str, Any]]:
    if not isinstance(values, list) or len(values) != 2:
        raise ListenerDeltaError(f"{label} must contain exactly two sealed responses")
    by_listener: dict[str, dict[str, Any]] = {}
    pair_ids: set[str] = set()
    audio_hashes: set[str] = set()
    for index, value in enumerate(values):
        sealed = _validate_sealed(value, f"{label}[{index}]")
        if sealed["window_id"] != expected_window_id:
            raise ListenerDeltaError(f"{label}[{index}] window identity mismatch")
        listener_id = sealed["listener"]["id"]
        if listener_id in by_listener:
            raise ListenerDeltaError(f"{label} contains duplicate listener identity")
        by_listener[listener_id] = sealed
        pair_ids.add(sealed["pair_id"])
        audio_hashes.add(sealed["audio_sha256"])
    if len(pair_ids) != 1:
        raise ListenerDeltaError(f"{label} responses do not share one pair")
    if len(audio_hashes) != 1:
        raise ListenerDeltaError(f"{label} responses do not share one audio digest")
    return by_listener


def _profile(sealed: dict[str, Any]) -> dict[str, Any]:
    response = sealed["response"]
    observations = []
    mode_counts = {mode: 0 for mode in MODES}
    observation_tokens: set[str] = set()
    for item in response["observations"]:
        normalized = _normalize_text(item["text"])
        observations.append({
            "mode": item["mode"],
            "text": item["text"],
            "normalized_text": normalized,
        })
        mode_counts[item["mode"]] += 1
        observation_tokens.update(_tokens(item["text"]))

    closing = response["closing_line"]
    return {
        "listener": sealed["listener"],
        "model_used": sealed["model_used"],
        "pair_id": sealed["pair_id"],
        "window_id": sealed["window_id"],
        "audio_sha256": sealed["audio_sha256"],
        "response_sha256": sealed["response_sha256"],
        "first_response_id": sealed["first_response_id"],
        "observation_count": len(observations),
        "mode_counts": mode_counts,
        "observations": observations,
        "observation_tokens": sorted(observation_tokens),
        "lingering_intrigue": response["lingering_intrigue"],
        "closing_line": {
            "text": closing,
            "normalized_text": _normalize_text(closing),
            "char_count": len(closing),
            "token_count": len(_TOKEN_RE.findall(_normalize_text(closing))),
        },
    }


def _expanded(counter: Counter[tuple[str, str]]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for (mode, text), count in sorted(counter.items()):
        items.append({"mode": mode, "normalized_text": text, "count": count})
    return items


def _listener_delta(
    parent: dict[str, Any],
    child: dict[str, Any],
) -> dict[str, Any]:
    parent_obs = Counter(
        (item["mode"], item["normalized_text"])
        for item in parent["observations"]
    )
    child_obs = Counter(
        (item["mode"], item["normalized_text"])
        for item in child["observations"]
    )
    persisted = parent_obs & child_obs
    disappeared = parent_obs - child_obs
    appeared = child_obs - parent_obs

    parent_modes: dict[str, set[str]] = {}
    child_modes: dict[str, set[str]] = {}
    for mode, text in parent_obs:
        parent_modes.setdefault(text, set()).add(mode)
    for mode, text in child_obs:
        child_modes.setdefault(text, set()).add(mode)
    migrations = []
    for text in sorted(set(parent_modes) & set(child_modes)):
        before = sorted(parent_modes[text])
        after = sorted(child_modes[text])
        if before != after:
            migrations.append({
                "normalized_text": text,
                "parent_modes": before,
                "child_modes": after,
            })

    mode_count_delta = {
        mode: child["mode_counts"][mode] - parent["mode_counts"][mode]
        for mode in MODES
    }
    intrigue = (
        "SAME_TRUE"
        if parent["lingering_intrigue"] and child["lingering_intrigue"]
        else "SAME_FALSE"
        if not parent["lingering_intrigue"] and not child["lingering_intrigue"]
        else "FALSE_TO_TRUE"
        if child["lingering_intrigue"]
        else "TRUE_TO_FALSE"
    )
    closing_same = (
        parent["closing_line"]["normalized_text"]
        == child["closing_line"]["normalized_text"]
    )

    parent_tokens = set(parent["observation_tokens"])
    child_tokens = set(child["observation_tokens"])
    token_delta = {
        "persisted": sorted(parent_tokens & child_tokens),
        "appeared": sorted(child_tokens - parent_tokens),
        "disappeared": sorted(parent_tokens - child_tokens),
    }

    changed_axes: list[str] = []
    if appeared or disappeared:
        changed_axes.append("exact_observations")
    if migrations:
        changed_axes.append("observation_modes")
    if any(mode_count_delta.values()):
        changed_axes.append("mode_counts")
    if intrigue not in {"SAME_TRUE", "SAME_FALSE"}:
        changed_axes.append("lingering_intrigue")
    if not closing_same:
        changed_axes.append("closing_line")
    if token_delta["appeared"] or token_delta["disappeared"]:
        changed_axes.append("observation_vocabulary")
    if parent["model_used"] != child["model_used"]:
        changed_axes.append("model_used")

    return {
        "classification": (
            "MEASURED_RESPONSE_CHANGE"
            if changed_axes
            else "NO_MEASURED_RESPONSE_CHANGE"
        ),
        "changed_axes": changed_axes,
        "unchanged_axes": [
            axis
            for axis in (
                "exact_observations",
                "observation_modes",
                "mode_counts",
                "lingering_intrigue",
                "closing_line",
                "observation_vocabulary",
                "model_used",
            )
            if axis not in changed_axes
        ],
        "exact_observations": {
            "persisted": _expanded(persisted),
            "appeared": _expanded(appeared),
            "disappeared": _expanded(disappeared),
        },
        "mode_migrations": migrations,
        "mode_count_delta": mode_count_delta,
        "intrigue_relation": intrigue,
        "closing_line": {
            "relation": "SAME_NORMALIZED" if closing_same else "DIFFERENT",
            "char_count_delta": (
                child["closing_line"]["char_count"]
                - parent["closing_line"]["char_count"]
            ),
            "token_count_delta": (
                child["closing_line"]["token_count"]
                - parent["closing_line"]["token_count"]
            ),
        },
        "observation_vocabulary": token_delta,
        "model_relation": (
            "SAME"
            if parent["model_used"] == child["model_used"]
            else "DIFFERENT"
        ),
    }


def compare_listener_responses(request: dict[str, Any]) -> dict[str, Any]:
    request = _exact_keys(
        request,
        {"schema", "transform", "parent_responses", "child_responses"},
        "request",
    )
    if request["schema"] != REQUEST_SCHEMA:
        raise ListenerDeltaError("unsupported listener-delta request schema")

    transform = _exact_keys(
        request["transform"],
        {
            "relation",
            "human_action",
            "parent_window_id",
            "child_window_id",
            "proposal_receipt_hash",
            "generation_delta_receipt_hash",
        },
        "transform",
    )
    if transform["relation"] != RELATION:
        raise ListenerDeltaError("unsupported listener generation relation")
    if transform["human_action"] != "explicit-admit":
        raise ListenerDeltaError("listener comparison requires explicit admission")
    parent_window_id = transform["parent_window_id"]
    child_window_id = transform["child_window_id"]
    if (
        not isinstance(parent_window_id, str)
        or not parent_window_id.startswith("autodisco-audio-window-v0:")
        or not isinstance(child_window_id, str)
        or not child_window_id.startswith("autodisco-audio-window-v0:")
        or parent_window_id == child_window_id
    ):
        raise ListenerDeltaError("listener generation window identities are invalid")
    _decode_sha256(
        transform["proposal_receipt_hash"],
        "transform.proposal_receipt_hash",
    )
    _decode_sha256(
        transform["generation_delta_receipt_hash"],
        "transform.generation_delta_receipt_hash",
    )

    parent_by_listener = _validate_generation(
        request["parent_responses"],
        "parent_responses",
        parent_window_id,
    )
    child_by_listener = _validate_generation(
        request["child_responses"],
        "child_responses",
        child_window_id,
    )
    if set(parent_by_listener) != set(child_by_listener):
        raise ListenerDeltaError(
            "parent and child generations must contain the same listener identities"
        )

    listeners: dict[str, Any] = {}
    for listener_id in sorted(parent_by_listener):
        parent_sealed = parent_by_listener[listener_id]
        child_sealed = child_by_listener[listener_id]
        if parent_sealed["listener"] != child_sealed["listener"]:
            raise ListenerDeltaError(
                f"listener descriptor changed for {listener_id}"
            )
        parent_profile = _profile(parent_sealed)
        child_profile = _profile(child_sealed)
        listeners[listener_id] = {
            "listener": parent_sealed["listener"],
            "parent": parent_profile,
            "child": child_profile,
            "delta": _listener_delta(parent_profile, child_profile),
        }

    deltas = [item["delta"] for item in listeners.values()]
    changed_sets = [set(item["changed_axes"]) for item in deltas]
    shared_changed_axes = sorted(set.intersection(*changed_sets)) if changed_sets else []
    union_changed_axes = sorted(set.union(*changed_sets)) if changed_sets else []

    appeared_token_sets = [
        set(item["observation_vocabulary"]["appeared"])
        for item in deltas
    ]
    disappeared_token_sets = [
        set(item["observation_vocabulary"]["disappeared"])
        for item in deltas
    ]
    shared_appeared_tokens = (
        sorted(set.intersection(*appeared_token_sets))
        if appeared_token_sets
        else []
    )
    shared_disappeared_tokens = (
        sorted(set.intersection(*disappeared_token_sets))
        if disappeared_token_sets
        else []
    )

    appeared_observation_sets = []
    for item in deltas:
        appeared_observation_sets.append({
            entry["normalized_text"]
            for entry in item["exact_observations"]["appeared"]
        })
    shared_appeared_observations = (
        sorted(set.intersection(*appeared_observation_sets))
        if appeared_observation_sets
        else []
    )

    changed_listener_count = sum(
        1
        for item in deltas
        if item["classification"] == "MEASURED_RESPONSE_CHANGE"
    )
    cohort = {
        "classification": (
            "MEASURED_RESPONSE_CHANGE"
            if changed_listener_count
            else "NO_MEASURED_RESPONSE_CHANGE"
        ),
        "listener_count": len(listeners),
        "changed_listener_count": changed_listener_count,
        "shared_changed_axes": shared_changed_axes,
        "union_changed_axes": union_changed_axes,
        "shared_appeared_tokens": shared_appeared_tokens,
        "shared_disappeared_tokens": shared_disappeared_tokens,
        "shared_appeared_observations": shared_appeared_observations,
    }

    body = {
        "schema": RECEIPT_SCHEMA,
        "specimen": "LISTENER-DELTA-001",
        "status": "OK",
        "transform": transform,
        "listeners": listeners,
        "cohort": cohort,
        "residuals": [
            "semantic_similarity_not_measured",
            "preference_not_measured",
            "musical_value_not_measured",
            "listener_identity_essence_not_inferred",
            "audio_change_causality_not_established",
            "stochastic_generation_effect_not_separated",
            "unobserved_listener_context_not_measured",
        ],
        "laws": [
            "DOGRAM MEASURES TRANSFORMS, NOT PEOPLE",
            "RESPONSE DELTA != PERSON DELTA",
            "RESPONSE DELTA != CAUSAL EFFECT",
            "SIGNAL DELTA != LISTENER DELTA",
            "LEXICAL OVERLAP != SEMANTIC AGREEMENT",
            "FIRST LISTEN != STABLE PREFERENCE",
            "DELTA != VALUE",
            "RESIDUAL != FAILURE",
            "DO NOT DECIDE WHAT IT MEANS",
        ],
    }
    return {
        **body,
        "receipt_hash": sha256_json(body),
    }
