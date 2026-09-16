"""Bounded multi-parent derivation receipts for LINEAGE-BRAID-001.

The braid layer references verified LINEAGE-SPINE-001 heads without embedding
those parent histories in the descendant.
"""

from __future__ import annotations

import copy

from dogram.lineage_spine import canonical_digest, verify_lineage


SPECIMEN = "LINEAGE-BRAID-001"
PARENT_SET_SCHEMA = "dogram.lineage-parent-set/v0"
MERGE_RECEIPT_SCHEMA = "dogram.lineage-merge-receipt/v0"
BRAID_CAPSULE_SCHEMA = "dogram.lineage-braid-capsule/v0"
BRAID_LEDGER_SCHEMA = "dogram.lineage-braid-ledger/v0"
PARENT_DESCRIPTOR_KEYS = {"head_digest", "root_digest", "carrier"}
PARENT_SET_KEYS = {"schema", "specimen", "parents"}
MERGE_RECEIPT_KEYS = {
    "schema",
    "specimen",
    "operator",
    "parent_set_digest",
    "inputs",
    "output",
}
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
        root_digest = parent["root_digest"]
        assert isinstance(root_digest, str)
        roots.add(root_digest)
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


def make_braid_ledger() -> dict[str, object]:
    return {
        "schema": BRAID_LEDGER_SCHEMA,
        "capsules": {},
        "parent_sets": {},
        "merge_receipts": {},
    }


def _bucket(ledger: dict[str, object], name: str) -> dict[str, object]:
    bucket = ledger.get(name)
    if not isinstance(bucket, dict):
        raise ValueError(f"braid ledger {name} bucket must be a mapping")
    return bucket


def _store(ledger: dict[str, object], bucket: str, value: dict[str, object]) -> str:
    digest = canonical_digest(value)
    _bucket(ledger, bucket)[digest] = copy.deepcopy(value)
    return digest


def store_parent_set(ledger: dict[str, object], parent_set: dict[str, object]) -> str:
    return _store(ledger, "parent_sets", parent_set)


def store_merge_receipt(ledger: dict[str, object], receipt: dict[str, object]) -> str:
    return _store(ledger, "merge_receipts", receipt)


def store_braid_capsule(ledger: dict[str, object], capsule: dict[str, object]) -> str:
    return _store(ledger, "capsules", capsule)


def _verification_result(
    status: str,
    reason: str | None,
    *,
    capsule: dict[str, object] | None = None,
    parents: list[dict[str, object]] | None = None,
    parent_head: str | None = None,
) -> dict[str, object]:
    parent_heads = [] if parents is None else [parent["head_digest"] for parent in parents]
    return {
        "status": status,
        "reason": reason,
        "carrier": None if capsule is None else capsule.get("carrier"),
        "parent_count": len(parent_heads),
        "parent_heads": parent_heads,
        "parent_head": parent_head,
    }


def verify_braid(
    head_digest: str,
    braid_ledger: dict[str, object],
    spine_ledger: dict[str, object],
) -> dict[str, object]:
    """Verify declared derivation convergence without promoting it to causality."""
    capsules = _bucket(braid_ledger, "capsules")
    parent_sets = _bucket(braid_ledger, "parent_sets")
    merge_receipts = _bucket(braid_ledger, "merge_receipts")

    raw_capsule = capsules.get(head_digest)
    if raw_capsule is None:
        return _verification_result("incomplete", "missing_braid_head")
    if not isinstance(raw_capsule, dict):
        return _verification_result("invalid", "capsule_not_mapping")
    capsule = raw_capsule
    if canonical_digest(capsule) != head_digest:
        return _verification_result("invalid", "capsule_digest_mismatch", capsule=capsule)
    if set(capsule) != BRAID_CAPSULE_KEYS:
        return _verification_result("invalid", "capsule_shape_mismatch", capsule=capsule)
    if capsule.get("schema") != BRAID_CAPSULE_SCHEMA or capsule.get("specimen") != SPECIMEN:
        return _verification_result("invalid", "capsule_schema_mismatch", capsule=capsule)
    if capsule.get("carrier_origin") != "parent_set_merge":
        return _verification_result("invalid", "carrier_origin_mismatch", capsule=capsule)

    parent_set_digest = capsule.get("parent_set_digest")
    if not isinstance(parent_set_digest, str) or not parent_set_digest:
        return _verification_result("invalid", "invalid_parent_set_digest", capsule=capsule)
    raw_parent_set = parent_sets.get(parent_set_digest)
    if raw_parent_set is None:
        return _verification_result("incomplete", "missing_parent_set", capsule=capsule)
    if not isinstance(raw_parent_set, dict):
        return _verification_result("invalid", "parent_set_not_mapping", capsule=capsule)
    parent_set = raw_parent_set
    if canonical_digest(parent_set) != parent_set_digest:
        return _verification_result("invalid", "parent_set_digest_mismatch", capsule=capsule)
    if set(parent_set) != PARENT_SET_KEYS:
        return _verification_result("invalid", "parent_set_shape_mismatch", capsule=capsule)
    if parent_set.get("schema") != PARENT_SET_SCHEMA or parent_set.get("specimen") != SPECIMEN:
        return _verification_result("invalid", "parent_set_schema_mismatch", capsule=capsule)

    parents = parent_set.get("parents")
    if not isinstance(parents, list) or len(parents) < 2:
        return _verification_result("invalid", "insufficient_parents", capsule=capsule)
    try:
        canonical_parent_set = make_parent_set(parents)
    except ValueError:
        return _verification_result("invalid", "invalid_parent_descriptor", capsule=capsule)
    if canonical_parent_set != parent_set:
        return _verification_result("invalid", "parent_set_not_canonical", capsule=capsule)

    merge_digest = capsule.get("merge_receipt_digest")
    if not isinstance(merge_digest, str) or not merge_digest:
        return _verification_result("invalid", "invalid_merge_receipt_digest", capsule=capsule, parents=parents)
    raw_merge = merge_receipts.get(merge_digest)
    if raw_merge is None:
        return _verification_result("incomplete", "missing_merge_receipt", capsule=capsule, parents=parents)
    if not isinstance(raw_merge, dict):
        return _verification_result("invalid", "merge_receipt_not_mapping", capsule=capsule, parents=parents)
    merge = raw_merge
    if canonical_digest(merge) != merge_digest:
        return _verification_result("invalid", "merge_receipt_digest_mismatch", capsule=capsule, parents=parents)
    if set(merge) != MERGE_RECEIPT_KEYS:
        return _verification_result("invalid", "merge_receipt_shape_mismatch", capsule=capsule, parents=parents)
    if merge.get("schema") != MERGE_RECEIPT_SCHEMA or merge.get("specimen") != SPECIMEN:
        return _verification_result("invalid", "merge_receipt_schema_mismatch", capsule=capsule, parents=parents)
    if merge.get("operator") != "sum":
        return _verification_result("invalid", "merge_operator_mismatch", capsule=capsule, parents=parents)
    if merge.get("parent_set_digest") != parent_set_digest:
        return _verification_result("invalid", "merge_parent_set_mismatch", capsule=capsule, parents=parents)

    spine_capsules = spine_ledger.get("capsules")
    if not isinstance(spine_capsules, dict):
        return _verification_result("invalid", "spine_capsules_not_mapping", capsule=capsule, parents=parents)

    for parent in parents:
        head = parent["head_digest"]
        assert isinstance(head, str)
        lineage = verify_lineage(head, spine_ledger)
        if lineage.get("status") == "incomplete":
            return _verification_result(
                "incomplete",
                "parent_line_incomplete",
                capsule=capsule,
                parents=parents,
                parent_head=head,
            )
        if lineage.get("status") != "complete":
            return _verification_result(
                "invalid",
                "parent_line_invalid",
                capsule=capsule,
                parents=parents,
                parent_head=head,
            )

        raw_parent_head = spine_capsules.get(head)
        if not isinstance(raw_parent_head, dict):
            return _verification_result(
                "incomplete",
                "parent_line_incomplete",
                capsule=capsule,
                parents=parents,
                parent_head=head,
            )
        if raw_parent_head.get("carrier") != parent.get("carrier"):
            return _verification_result(
                "invalid",
                "parent_carrier_mismatch",
                capsule=capsule,
                parents=parents,
                parent_head=head,
            )
        if raw_parent_head.get("root_digest") != parent.get("root_digest"):
            return _verification_result(
                "invalid",
                "parent_root_mismatch",
                capsule=capsule,
                parents=parents,
                parent_head=head,
            )

    expected_inputs = [parent["carrier"] for parent in parents]
    if merge.get("inputs") != expected_inputs:
        return _verification_result("invalid", "merge_inputs_mismatch", capsule=capsule, parents=parents)
    merge_output = merge.get("output")
    if isinstance(merge_output, bool) or not isinstance(merge_output, int):
        return _verification_result("invalid", "merge_output_mismatch", capsule=capsule, parents=parents)
    if merge_output != sum(expected_inputs):
        return _verification_result("invalid", "merge_output_mismatch", capsule=capsule, parents=parents)
    if capsule.get("carrier") != merge_output:
        return _verification_result("invalid", "braid_carrier_mismatch", capsule=capsule, parents=parents)
    try:
        expected_root_set_digest = root_set_digest(parent_set)
    except ValueError:
        return _verification_result("invalid", "invalid_root_set", capsule=capsule, parents=parents)
    if capsule.get("root_set_digest") != expected_root_set_digest:
        return _verification_result("invalid", "root_set_digest_mismatch", capsule=capsule, parents=parents)

    return _verification_result("complete", None, capsule=capsule, parents=parents)
