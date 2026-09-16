"""Bounded content-addressed lineage receipts for LINEAGE-SPINE-001.

The receipt is not the road. This module preserves enough local provenance to
reconstruct declared derivation ancestry when the referenced ledger entries are
available, without recursively embedding the full past in every child capsule.
"""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any


CAPSULE_SCHEMA = "dogram.lineage-capsule/v0"
LEDGER_SCHEMA = "dogram.lineage-ledger/v0"
SPECIMEN = "LINEAGE-SPINE-001"
CAPSULE_KEYS = {
    "schema",
    "specimen",
    "generation",
    "carrier",
    "carrier_origin",
    "root_digest",
    "parent_digest",
    "crossing_digest",
}


def canonical_digest(value: Any) -> str:
    """Return a deterministic SHA-256 content address for JSON-compatible data."""
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _root_anchor(carrier: int) -> dict[str, object]:
    return {
        "specimen": SPECIMEN,
        "carrier": carrier,
        "carrier_origin": "declared_root",
    }


def make_root(carrier: int) -> dict[str, object]:
    if isinstance(carrier, bool) or not isinstance(carrier, int):
        raise ValueError("root carrier must be an integer")
    root_digest = canonical_digest(_root_anchor(carrier))
    return {
        "schema": CAPSULE_SCHEMA,
        "specimen": SPECIMEN,
        "generation": 0,
        "carrier": carrier,
        "carrier_origin": "declared_root",
        "root_digest": root_digest,
        "parent_digest": None,
        "crossing_digest": None,
    }


def append_from_crossing(
    parent_capsule: dict[str, object],
    crossing_receipt: dict[str, object],
) -> dict[str, object]:
    generation = parent_capsule.get("generation")
    carrier = crossing_receipt.get("delta")
    if isinstance(generation, bool) or not isinstance(generation, int) or generation < 0:
        raise ValueError("parent capsule must contain a nonnegative integer generation")
    if isinstance(carrier, bool) or not isinstance(carrier, int):
        raise ValueError("crossing receipt must contain an integer delta")
    if crossing_receipt.get("carrier") != parent_capsule.get("carrier"):
        raise ValueError("crossing carrier must equal parent carrier")
    root_digest = parent_capsule.get("root_digest")
    if not isinstance(root_digest, str) or not root_digest:
        raise ValueError("parent capsule must contain a root digest")

    return {
        "schema": CAPSULE_SCHEMA,
        "specimen": SPECIMEN,
        "generation": generation + 1,
        "carrier": carrier,
        "carrier_origin": "parent_crossing_delta",
        "root_digest": root_digest,
        "parent_digest": canonical_digest(parent_capsule),
        "crossing_digest": canonical_digest(crossing_receipt),
    }


def make_ledger() -> dict[str, object]:
    return {
        "schema": LEDGER_SCHEMA,
        "capsules": {},
        "receipts": {},
    }


def _bucket(ledger: dict[str, object], name: str) -> dict[str, object]:
    bucket = ledger.get(name)
    if not isinstance(bucket, dict):
        raise ValueError(f"ledger {name} bucket must be a mapping")
    return bucket


def store_capsule(ledger: dict[str, object], capsule: dict[str, object]) -> str:
    digest = canonical_digest(capsule)
    _bucket(ledger, "capsules")[digest] = copy.deepcopy(capsule)
    return digest


def store_receipt(ledger: dict[str, object], receipt: dict[str, object]) -> str:
    digest = canonical_digest(receipt)
    _bucket(ledger, "receipts")[digest] = copy.deepcopy(receipt)
    return digest


def _result(status: str, reason: str | None, chain: list[tuple[str, dict[str, object]]]) -> dict[str, object]:
    ordered = list(reversed(chain))
    return {
        "status": status,
        "reason": reason,
        "generations": [capsule["generation"] for _, capsule in ordered],
        "carriers": [capsule["carrier"] for _, capsule in ordered],
        "capsule_digests": [digest for digest, _ in ordered],
    }


def verify_lineage(head_digest: str, ledger: dict[str, object]) -> dict[str, object]:
    """Verify a declared lineage as complete, incomplete, or invalid.

    `incomplete` means witness material required for reconstruction is absent.
    It does not claim that the underlying causal or derivation line was severed.
    """
    capsules = _bucket(ledger, "capsules")
    receipts = _bucket(ledger, "receipts")
    current_digest = head_digest
    chain: list[tuple[str, dict[str, object]]] = []
    expected_root: str | None = None
    seen: set[str] = set()

    while True:
        if current_digest in seen:
            return _result("invalid", "cycle_detected", chain)
        seen.add(current_digest)

        raw_capsule = capsules.get(current_digest)
        if raw_capsule is None:
            reason = "missing_head_capsule" if not chain else "missing_parent_capsule"
            return _result("incomplete", reason, chain)
        if not isinstance(raw_capsule, dict):
            return _result("invalid", "capsule_not_mapping", chain)
        capsule = raw_capsule

        if canonical_digest(capsule) != current_digest:
            return _result("invalid", "capsule_digest_mismatch", chain)
        if set(capsule) != CAPSULE_KEYS:
            return _result("invalid", "capsule_shape_mismatch", chain)
        if capsule.get("schema") != CAPSULE_SCHEMA or capsule.get("specimen") != SPECIMEN:
            return _result("invalid", "capsule_schema_mismatch", chain)

        generation = capsule.get("generation")
        carrier = capsule.get("carrier")
        root_digest = capsule.get("root_digest")
        if isinstance(generation, bool) or not isinstance(generation, int) or generation < 0:
            return _result("invalid", "invalid_generation", chain)
        if isinstance(carrier, bool) or not isinstance(carrier, int):
            return _result("invalid", "invalid_carrier", chain)
        if not isinstance(root_digest, str) or not root_digest:
            return _result("invalid", "invalid_root_digest", chain)

        if expected_root is None:
            expected_root = root_digest
        elif root_digest != expected_root:
            return _result("invalid", "root_digest_mismatch", chain)

        chain.append((current_digest, capsule))

        if generation == 0:
            if capsule.get("parent_digest") is not None or capsule.get("crossing_digest") is not None:
                return _result("invalid", "root_has_parentage", chain)
            if capsule.get("carrier_origin") != "declared_root":
                return _result("invalid", "root_origin_mismatch", chain)
            if canonical_digest(_root_anchor(carrier)) != root_digest:
                return _result("invalid", "root_anchor_mismatch", chain)
            return _result("complete", None, chain)

        if capsule.get("carrier_origin") != "parent_crossing_delta":
            return _result("invalid", "derived_origin_mismatch", chain)
        parent_digest = capsule.get("parent_digest")
        crossing_digest = capsule.get("crossing_digest")
        if not isinstance(parent_digest, str) or not parent_digest:
            return _result("invalid", "invalid_parent_digest", chain)
        if not isinstance(crossing_digest, str) or not crossing_digest:
            return _result("invalid", "invalid_crossing_digest", chain)

        raw_receipt = receipts.get(crossing_digest)
        if raw_receipt is None:
            return _result("incomplete", "missing_crossing_receipt", chain)
        if not isinstance(raw_receipt, dict):
            return _result("invalid", "crossing_receipt_not_mapping", chain)
        receipt = raw_receipt
        if canonical_digest(receipt) != crossing_digest:
            return _result("invalid", "crossing_digest_mismatch", chain)
        if receipt.get("delta") != carrier:
            return _result("invalid", "carrier_delta_mismatch", chain)

        raw_parent = capsules.get(parent_digest)
        if raw_parent is None:
            return _result("incomplete", "missing_parent_capsule", chain)
        if not isinstance(raw_parent, dict):
            return _result("invalid", "parent_capsule_not_mapping", chain)
        if canonical_digest(raw_parent) != parent_digest:
            return _result("invalid", "parent_digest_mismatch", chain)
        if raw_parent.get("generation") != generation - 1:
            return _result("invalid", "generation_gap", chain)
        if receipt.get("carrier") != raw_parent.get("carrier"):
            return _result("invalid", "crossing_parent_carrier_mismatch", chain)
        if raw_parent.get("root_digest") != root_digest:
            return _result("invalid", "parent_root_mismatch", chain)

        current_digest = parent_digest
