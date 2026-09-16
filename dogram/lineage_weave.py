"""Typed composition receipts for LINEAGE-WEAVE-001.

This layer composes verified lineage kinds without modifying their frozen
contracts or promoting derivation structure into causal meaning.
"""

from __future__ import annotations

import copy

from dogram.lineage_spine import canonical_digest


SPECIMEN = "LINEAGE-WEAVE-001"
ROOT_SET_SCHEMA = "dogram.lineage-weave-root-set/v0"
PARENT_SET_SCHEMA = "dogram.lineage-weave-parent-set/v0"
MERGE_RECEIPT_SCHEMA = "dogram.lineage-weave-merge-receipt/v0"
WEAVE_CAPSULE_SCHEMA = "dogram.lineage-weave-capsule/v0"
WEAVE_LEDGER_SCHEMA = "dogram.lineage-weave-ledger/v0"
PARENT_DESCRIPTOR_KEYS = {"kind", "head_digest", "carrier", "root_set_digest"}
SUPPORTED_KINDS = {"spine", "braid"}


def _require_digest(value: object, *, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name} digest must be a non-empty string")
    return value


def make_root_set(root_digests: list[str]) -> dict[str, object]:
    if not root_digests:
        raise ValueError("root set requires at least one root digest")
    roots: set[str] = set()
    for root in root_digests:
        roots.add(_require_digest(root, name="root"))
    return {
        "schema": ROOT_SET_SCHEMA,
        "specimen": SPECIMEN,
        "roots": sorted(roots),
    }


def make_typed_parent(
    kind: str,
    head_digest: str,
    carrier: int,
    root_digests: list[str],
) -> dict[str, object]:
    if kind not in SUPPORTED_KINDS:
        raise ValueError("parent kind must be 'spine' or 'braid'")
    _require_digest(head_digest, name="head")
    if isinstance(carrier, bool) or not isinstance(carrier, int):
        raise ValueError("parent carrier must be an integer")
    root_set = make_root_set(root_digests)
    return {
        "kind": kind,
        "head_digest": head_digest,
        "carrier": carrier,
        "root_set_digest": canonical_digest(root_set),
    }


def _validate_parent_descriptor(parent: dict[str, object]) -> None:
    if set(parent) != PARENT_DESCRIPTOR_KEYS:
        raise ValueError("parent descriptor shape must be exact")
    kind = parent.get("kind")
    if kind not in SUPPORTED_KINDS:
        raise ValueError("parent kind must be 'spine' or 'braid'")
    _require_digest(parent.get("head_digest"), name="head")
    carrier = parent.get("carrier")
    if isinstance(carrier, bool) or not isinstance(carrier, int):
        raise ValueError("parent carrier must be an integer")
    _require_digest(parent.get("root_set_digest"), name="root set")


def make_parent_set(parents: list[dict[str, object]]) -> dict[str, object]:
    if len(parents) < 2:
        raise ValueError("parent set requires at least two parents")

    normalized: list[dict[str, object]] = []
    for parent in parents:
        if not isinstance(parent, dict):
            raise ValueError("parent descriptor must be a mapping")
        _validate_parent_descriptor(parent)
        normalized.append(copy.deepcopy(parent))

    identities = [(parent["kind"], parent["head_digest"]) for parent in normalized]
    if len(set(identities)) != len(identities):
        raise ValueError("typed parent heads must be unique")

    normalized.sort(key=lambda parent: (parent["kind"], parent["head_digest"]))
    return {
        "schema": PARENT_SET_SCHEMA,
        "specimen": SPECIMEN,
        "parents": normalized,
    }


def make_sum_merge(parent_set: dict[str, object]) -> dict[str, object]:
    if parent_set.get("schema") != PARENT_SET_SCHEMA or parent_set.get("specimen") != SPECIMEN:
        raise ValueError("invalid parent set")
    parents = parent_set.get("parents")
    if not isinstance(parents, list) or len(parents) < 2:
        raise ValueError("parent set requires at least two parents")

    inputs: list[int] = []
    for parent in parents:
        if not isinstance(parent, dict):
            raise ValueError("parent descriptor must be a mapping")
        _validate_parent_descriptor(parent)
        carrier = parent["carrier"]
        assert isinstance(carrier, int) and not isinstance(carrier, bool)
        inputs.append(carrier)

    return {
        "schema": MERGE_RECEIPT_SCHEMA,
        "specimen": SPECIMEN,
        "operator": "sum",
        "parent_set_digest": canonical_digest(parent_set),
        "inputs": inputs,
        "output": sum(inputs),
    }


def make_weave_capsule(
    parent_set: dict[str, object],
    root_set: dict[str, object],
    merge_receipt: dict[str, object],
) -> dict[str, object]:
    parent_set_digest = canonical_digest(parent_set)
    if merge_receipt.get("schema") != MERGE_RECEIPT_SCHEMA or merge_receipt.get("specimen") != SPECIMEN:
        raise ValueError("invalid merge receipt")
    if merge_receipt.get("operator") != "sum":
        raise ValueError("unsupported merge operator")
    if merge_receipt.get("parent_set_digest") != parent_set_digest:
        raise ValueError("merge parent set digest mismatch")
    output = merge_receipt.get("output")
    if isinstance(output, bool) or not isinstance(output, int):
        raise ValueError("merge output must be an integer")
    if root_set.get("schema") != ROOT_SET_SCHEMA or root_set.get("specimen") != SPECIMEN:
        raise ValueError("invalid root set")

    return {
        "schema": WEAVE_CAPSULE_SCHEMA,
        "specimen": SPECIMEN,
        "carrier": output,
        "carrier_origin": "typed_parent_set_merge",
        "parent_set_digest": parent_set_digest,
        "merge_receipt_digest": canonical_digest(merge_receipt),
        "root_set_digest": canonical_digest(root_set),
    }


def make_weave_ledger() -> dict[str, object]:
    return {
        "schema": WEAVE_LEDGER_SCHEMA,
        "capsules": {},
        "parent_sets": {},
        "root_sets": {},
        "merge_receipts": {},
    }


def _bucket(ledger: dict[str, object], name: str) -> dict[str, object]:
    bucket = ledger.get(name)
    if not isinstance(bucket, dict):
        raise ValueError(f"weave ledger {name} bucket must be a mapping")
    return bucket


def _store(ledger: dict[str, object], bucket: str, value: dict[str, object]) -> str:
    digest = canonical_digest(value)
    _bucket(ledger, bucket)[digest] = copy.deepcopy(value)
    return digest


def store_parent_set(ledger: dict[str, object], parent_set: dict[str, object]) -> str:
    return _store(ledger, "parent_sets", parent_set)


def store_root_set(ledger: dict[str, object], root_set: dict[str, object]) -> str:
    return _store(ledger, "root_sets", root_set)


def store_merge_receipt(ledger: dict[str, object], receipt: dict[str, object]) -> str:
    return _store(ledger, "merge_receipts", receipt)


def store_weave_capsule(ledger: dict[str, object], capsule: dict[str, object]) -> str:
    return _store(ledger, "capsules", capsule)
