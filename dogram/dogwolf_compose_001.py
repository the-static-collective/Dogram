"""DOGWOLF-COMPOSE-001: one declared model, three independent research calculations.

A pure, read-only, JSON-safe handoff for a prospective Workbench adapter.
No public Dogram operator, project authority, or automated Workbench invocation.
"""
from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json

from .commute_001 import analyze_commutation
from .descend_001 import analyze_descent, _typed
from .successor_descent_001 import analyze_successor_descent


def _json_safe(value: object) -> object:
    """Convert the three stable internal dataclass receipts to JSON values."""
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_safe(item) for item in value]
    return value


def canonical_sha256(value: object) -> str:
    """Content checksum, not a signature or trusted execution attestation."""
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    return sha256(encoded).hexdigest()


def compose_receipt(
    states: tuple[str, ...],
    projection: tuple[object, ...],
    first: tuple[str, tuple[str, ...]],
    second: tuple[str, tuple[str, ...]],
    successors: tuple[tuple[str, ...], ...],
    *,
    max_pair_checks: int = 4096,
    max_state_checks: int = 64,
) -> dict[str, object]:
    """Calculate three separate views of one finite declared carrier.

    The successor relation is *independently* declared. Membership of an
    operation's target in this relation is neither assumed nor inferred.
    The adapter never reduces heterogeneous result statuses to one verdict.
    """
    if type(first) is not tuple or len(first) != 2 or type(second) is not tuple or len(second) != 2:
        raise ValueError("first and second must be (name, targets) tuples")
    if type(first[0]) is not str or type(second[0]) is not str or first[0] == second[0]:
        raise ValueError("operation names must be distinct strings")

    # Every underlying calculator independently validates the same input.
    descent = analyze_descent(
        states, projection, {first[0]: first[1], second[0]: second[1]},
        max_pair_checks=max_pair_checks,
    )
    successor = analyze_successor_descent(
        states, projection, successors, max_pair_checks=max_pair_checks,
    )
    commutation = analyze_commutation(
        states, projection, first, second, max_state_checks=max_state_checks,
    )

    model = {
        "states": _json_safe(states),
        "projection": _json_safe(projection),
        "operations": {
            "first": {"name": first[0], "targets": _json_safe(first[1])},
            "second": {"name": second[0], "targets": _json_safe(second[1])},
        },
        "successors": _json_safe(successors),
        "successor_relation": (
            "independently declared one-step succession; do not infer it "
            "from operation targets or treat it as executed history"
        ),
        "budgets": {"max_pair_checks": max_pair_checks, "max_state_checks": max_state_checks},
    }
    # Bind primitive type identity as well as human-readable values.
    model_digest_data = {
        "schema": "dogram/dogwolf-compose-model/v0",
        "states": states,
        "typed_projection": tuple(_typed(v) for v in projection),
        "first": first,
        "second": second,
        "successors": successors,
        "budgets": model["budgets"],
    }
    packet: dict[str, object] = {
        "schema": "dogram/dogwolf-compose-001/v0",
        "model": model,
        "model_sha256": canonical_sha256(model_digest_data),
        "results": {
            "descent": _json_safe(asdict(descent)),
            "successor": _json_safe(asdict(successor)),
            "commutation": _json_safe(asdict(commutation)),
        },
        "authority": "none",
        "non_claims": [
            "Research calculation receipt, not dogram.receipt/v0 public dispatch.",
            "Model and successor relation are declared; no occurrence or execution is inferred.",
            "Matching projected endpoints do not establish path or raw-state identity.",
            "No aggregate pass/fail, safety, quality, readiness or merge recommendation.",
            "SHA-256 is a content checksum, not a signature or trusted provenance attestation.",
            "No Workbench action, project mutation, automatic invocation or permission grant.",
        ],
    }
    packet["receipt_sha256"] = canonical_sha256(packet)
    return packet


__all__ = ["compose_receipt", "canonical_sha256"]
