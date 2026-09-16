"""Bounded multi-parent derivation receipts for LINEAGE-BRAID-001.

The braid layer references verified LINEAGE-SPINE-001 heads without embedding
those parent histories in the descendant.
"""

from __future__ import annotations

import copy

from dogram.lineage_spine import canonical_digest


SPECIMEN = "LINEAGE-BRAID-001"
PARENT_SET_SCHEMA = "dogram.lineage-parent-set/v0"
MERGE_RECEIPT_SCHEMA = "dogram.lineage-merge-receipt/v0"
BRAID_CAPSULE_SCHEMA = "dogram.lineage-braid-capsule/v0"
PARENT_DESCRIPTOR_KEYS = {"head_digest", "root_digest", "carrier"}
BRAID_CAPSULE_KEYS = {
    "schema",
    "specimen",
    "carrier",
    "carrier_origin",
    "parent_set_digest",
    "merge_receipt_digest",
    "root_set_digest",
}


def _validate_parent_descriptor(parent: dict[str, object]) -> None:
    if set(parent) != PARENT_DESCRIPTOR_KEYS:
        raise ValueError("parent descriptor shape must be exact")
    head_digest = parent.get("head_digest")
    root_digest = parent.get("root_digest")
    carrier = parent.get("carrier")
    if not isinstance(head_digest, str) or not head_digest:
        raise ValueError("parent head digest must be a non-empty string")
    if not isinstance(root_digest, str) or not root_digest:
        raise ValueError("parent root digest must be a non-empty string")
    if isinstance(carrier, bool) or not isinstance(carrier, int):
        raise ValueError("parent carrier must be an integer")


def make_parent_set(parents: list[dict[str, object]]) -> dict[str, object]:
    if len(parents) < 2:
        raise ValueError("parent set requires at least two parents")

    normalized: list[dict[str, object]] = []
    for parent in parents:
        if not isinstance(parent, dict):
            raise ValueError("parent descriptor must be a mapping")
        _validate_parent_descriptor(parent)
        normalized.append(copy.deepcopy(parent))

    head_digests = [parent["head_digest"] for parent in normalized]
    if len(set(head_digests)) != len(head_digests):
        raise ValueError("parent head digests must be unique")

    normalized.sort(key=lambda parent: parent["head_digest"])
    return {
        "schema": PARENT_SET_SCHEMA,
        "specimen": SPECIMEN,
        "parents": normalized,
    }


def root_set_digest(parent_set: dict[str, object]) -> str:
    if parent_set.get("schema") != PARENT_SET_SCHEMA or parent_set.get("specimen") != SPECIMEN:
        raise ValueError("invalid parent set")
    parents = parent_set.get("parents")
    if not isinstance(parents, list):
        raise ValueError("parent set parents must be a list")
    roots: set[str] = set()
    for parent in parents:
        if not isinstance(parent, dict):
            raise ValueError("parent descriptor must be a mapping")
        _validate_parent_descriptor(parent)
        roots.add(parent["root_digest"])
    return canonical_digest({"roots": sorted(roots)})


def make_sum_merge(parent_set: dict[str, object]) -> dict[str, object]:
    parents = parent_set.get("parents")
    if parent_set.get("schema") != PARENT_SET_SCHEMA or parent_set.get("specimen") != SPECIMEN:
        raise ValueError("invalid parent set")
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


def make_braid_capsule(
    parent_set: dict[str, object],
    merge_receipt: dict[str, object],
) -> dict[str, object]:
    parent_digest = canonical_digest(parent_set)
    if merge_receipt.get("schema") != MERGE_RECEIPT_SCHEMA or merge_receipt.get("specimen") != SPECIMEN:
        raise ValueError("invalid merge receipt")
    if merge_receipt.get("operator") != "sum":
        raise ValueError("unsupported merge operator")
    if merge_receipt.get("parent_set_digest") != parent_digest:
        raise ValueError("merge parent set digest mismatch")
    output = merge_receipt.get("output")
    if isinstance(output, bool) or not isinstance(output, int):
        raise ValueError("merge output must be an integer")

    return {
        "schema": BRAID_CAPSULE_SCHEMA,
        "specimen": SPECIMEN,
        "carrier": output,
        "carrier_origin": "parent_set_merge",
        "parent_set_digest": parent_digest,
        "merge_receipt_digest": canonical_digest(merge_receipt),
        "root_set_digest": root_set_digest(parent_set),
    }
