"""Typed composition receipts for LINEAGE-WEAVE-001.

This layer composes verified lineage kinds without modifying their frozen
contracts or promoting derivation structure into causal meaning.
"""

from __future__ import annotations

import copy

from dogram.lineage_braid import verify_braid
from dogram.lineage_spine import canonical_digest, verify_lineage


SPECIMEN = "LINEAGE-WEAVE-001"
ROOT_SET_SCHEMA = "dogram.lineage-weave-root-set/v0"
PARENT_SET_SCHEMA = "dogram.lineage-weave-parent-set/v0"
MERGE_RECEIPT_SCHEMA = "dogram.lineage-weave-merge-receipt/v0"
WEAVE_CAPSULE_SCHEMA = "dogram.lineage-weave-capsule/v0"
WEAVE_LEDGER_SCHEMA = "dogram.lineage-weave-ledger/v0"
PARENT_DESCRIPTOR_KEYS = {"kind", "head_digest", "carrier", "root_set_digest"}
ROOT_SET_KEYS = {"schema", "specimen", "roots"}
PARENT_SET_KEYS = {"schema", "specimen", "parents"}
MERGE_RECEIPT_KEYS = {
    "schema",
    "specimen",
    "operator",
    "parent_set_digest",
    "inputs",
    "output",
}
WEAVE_CAPSULE_KEYS = {
    "schema",
    "specimen",
    "carrier",
    "carrier_origin",
    "parent_set_digest",
    "merge_receipt_digest",
    "root_set_digest",
}
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


def _result(
    status: str,
    reason: str | None,
    *,
    capsule: dict[str, object] | None = None,
    parents: list[dict[str, object]] | None = None,
    parent_kind: str | None = None,
    parent_head: str | None = None,
) -> dict[str, object]:
    parent_list = [] if parents is None else parents
    return {
        "status": status,
        "reason": reason,
        "carrier": None if capsule is None else capsule.get("carrier"),
        "parent_count": len(parent_list),
        "parent_kinds": [parent.get("kind") for parent in parent_list],
        "parent_heads": [parent.get("head_digest") for parent in parent_list],
        "parent_kind": parent_kind,
        "parent_head": parent_head,
    }


def _mapping_bucket(ledger: dict[str, object], name: str) -> dict[str, object] | None:
    value = ledger.get(name)
    return value if isinstance(value, dict) else None


def _braid_roots(
    head_digest: str,
    braid_ledger: dict[str, object],
) -> list[str] | None:
    capsules = _mapping_bucket(braid_ledger, "capsules")
    parent_sets = _mapping_bucket(braid_ledger, "parent_sets")
    if capsules is None or parent_sets is None:
        return None
    capsule = capsules.get(head_digest)
    if not isinstance(capsule, dict):
        return None
    parent_set_digest = capsule.get("parent_set_digest")
    if not isinstance(parent_set_digest, str):
        return None
    parent_set = parent_sets.get(parent_set_digest)
    if not isinstance(parent_set, dict):
        return None
    parents = parent_set.get("parents")
    if not isinstance(parents, list):
        return None
    roots: list[str] = []
    for parent in parents:
        if not isinstance(parent, dict):
            return None
        root = parent.get("root_digest")
        if not isinstance(root, str) or not root:
            return None
        roots.append(root)
    return roots


def verify_weave(
    head_digest: str,
    weave_ledger: dict[str, object],
    braid_ledger: dict[str, object],
    spine_ledger: dict[str, object],
) -> dict[str, object]:
    """Verify typed composition without erasing which verifier governs each parent."""
    if weave_ledger.get("schema") != WEAVE_LEDGER_SCHEMA:
        return _result("invalid", "weave_ledger_schema_mismatch")

    capsules = _mapping_bucket(weave_ledger, "capsules")
    parent_sets = _mapping_bucket(weave_ledger, "parent_sets")
    root_sets = _mapping_bucket(weave_ledger, "root_sets")
    merge_receipts = _mapping_bucket(weave_ledger, "merge_receipts")
    if capsules is None or parent_sets is None or root_sets is None or merge_receipts is None:
        return _result("invalid", "weave_ledger_bucket_mismatch")

    raw_capsule = capsules.get(head_digest)
    if raw_capsule is None:
        return _result("incomplete", "missing_weave_head")
    if not isinstance(raw_capsule, dict):
        return _result("invalid", "capsule_not_mapping")
    capsule = raw_capsule
    if canonical_digest(capsule) != head_digest:
        return _result("invalid", "capsule_digest_mismatch", capsule=capsule)
    if set(capsule) != WEAVE_CAPSULE_KEYS:
        return _result("invalid", "capsule_shape_mismatch", capsule=capsule)
    if capsule.get("schema") != WEAVE_CAPSULE_SCHEMA or capsule.get("specimen") != SPECIMEN:
        return _result("invalid", "capsule_schema_mismatch", capsule=capsule)
    if capsule.get("carrier_origin") != "typed_parent_set_merge":
        return _result("invalid", "carrier_origin_mismatch", capsule=capsule)
    carrier = capsule.get("carrier")
    if isinstance(carrier, bool) or not isinstance(carrier, int):
        return _result("invalid", "invalid_weave_carrier", capsule=capsule)

    parent_set_digest = capsule.get("parent_set_digest")
    if not isinstance(parent_set_digest, str) or not parent_set_digest:
        return _result("invalid", "invalid_parent_set_digest", capsule=capsule)
    raw_parent_set = parent_sets.get(parent_set_digest)
    if raw_parent_set is None:
        return _result("incomplete", "missing_parent_set", capsule=capsule)
    if not isinstance(raw_parent_set, dict):
        return _result("invalid", "parent_set_not_mapping", capsule=capsule)
    parent_set = raw_parent_set
    if canonical_digest(parent_set) != parent_set_digest:
        return _result("invalid", "parent_set_digest_mismatch", capsule=capsule)
    if set(parent_set) != PARENT_SET_KEYS:
        return _result("invalid", "parent_set_shape_mismatch", capsule=capsule)
    if parent_set.get("schema") != PARENT_SET_SCHEMA or parent_set.get("specimen") != SPECIMEN:
        return _result("invalid", "parent_set_schema_mismatch", capsule=capsule)
    parents = parent_set.get("parents")
    if not isinstance(parents, list) or len(parents) < 2:
        return _result("invalid", "insufficient_parents", capsule=capsule)
    try:
        canonical_parent_set = make_parent_set(parents)
    except ValueError:
        return _result("invalid", "parent_descriptor_shape_mismatch", capsule=capsule)
    if canonical_parent_set != parent_set:
        return _result("invalid", "parent_set_not_canonical", capsule=capsule, parents=parents)

    root_set_digest = capsule.get("root_set_digest")
    if not isinstance(root_set_digest, str) or not root_set_digest:
        return _result("invalid", "invalid_root_set_digest", capsule=capsule, parents=parents)
    raw_root_set = root_sets.get(root_set_digest)
    if raw_root_set is None:
        return _result("incomplete", "missing_root_set", capsule=capsule, parents=parents)
    if not isinstance(raw_root_set, dict):
        return _result("invalid", "root_set_not_mapping", capsule=capsule, parents=parents)
    root_set = raw_root_set
    if canonical_digest(root_set) != root_set_digest:
        return _result("invalid", "root_set_digest_mismatch", capsule=capsule, parents=parents)
    if set(root_set) != ROOT_SET_KEYS:
        return _result("invalid", "root_set_shape_mismatch", capsule=capsule, parents=parents)
    if root_set.get("schema") != ROOT_SET_SCHEMA or root_set.get("specimen") != SPECIMEN:
        return _result("invalid", "root_set_schema_mismatch", capsule=capsule, parents=parents)
    roots_value = root_set.get("roots")
    if not isinstance(roots_value, list):
        return _result("invalid", "root_set_roots_mismatch", capsule=capsule, parents=parents)
    try:
        canonical_root_set = make_root_set(roots_value)
    except ValueError:
        return _result("invalid", "root_set_roots_mismatch", capsule=capsule, parents=parents)
    if canonical_root_set != root_set:
        return _result("invalid", "root_set_not_canonical", capsule=capsule, parents=parents)

    merge_digest = capsule.get("merge_receipt_digest")
    if not isinstance(merge_digest, str) or not merge_digest:
        return _result("invalid", "invalid_merge_receipt_digest", capsule=capsule, parents=parents)
    raw_merge = merge_receipts.get(merge_digest)
    if raw_merge is None:
        return _result("incomplete", "missing_merge_receipt", capsule=capsule, parents=parents)
    if not isinstance(raw_merge, dict):
        return _result("invalid", "merge_receipt_not_mapping", capsule=capsule, parents=parents)
    merge = raw_merge
    if canonical_digest(merge) != merge_digest:
        return _result("invalid", "merge_receipt_digest_mismatch", capsule=capsule, parents=parents)
    if set(merge) != MERGE_RECEIPT_KEYS:
        return _result("invalid", "merge_receipt_shape_mismatch", capsule=capsule, parents=parents)
    if merge.get("schema") != MERGE_RECEIPT_SCHEMA or merge.get("specimen") != SPECIMEN:
        return _result("invalid", "merge_receipt_schema_mismatch", capsule=capsule, parents=parents)
    if merge.get("operator") != "sum":
        return _result("invalid", "merge_operator_mismatch", capsule=capsule, parents=parents)
    if merge.get("parent_set_digest") != parent_set_digest:
        return _result("invalid", "merge_parent_set_mismatch", capsule=capsule, parents=parents)

    spine_capsules = _mapping_bucket(spine_ledger, "capsules")
    braid_capsules = _mapping_bucket(braid_ledger, "capsules")
    if spine_capsules is None or braid_capsules is None:
        return _result("invalid", "typed_ledger_bucket_mismatch", capsule=capsule, parents=parents)

    represented_roots: list[str] = []
    for parent in parents:
        assert isinstance(parent, dict)
        kind = parent["kind"]
        head = parent["head_digest"]
        assert isinstance(kind, str) and isinstance(head, str)

        if kind == "spine":
            if head not in spine_capsules:
                if head in braid_capsules:
                    return _result(
                        "invalid",
                        "parent_kind_mismatch",
                        capsule=capsule,
                        parents=parents,
                        parent_kind=kind,
                        parent_head=head,
                    )
                return _result(
                    "incomplete",
                    "parent_spine_incomplete",
                    capsule=capsule,
                    parents=parents,
                    parent_kind=kind,
                    parent_head=head,
                )
            verification = verify_lineage(head, spine_ledger)
            if verification.get("status") == "incomplete":
                return _result("incomplete", "parent_spine_incomplete", capsule=capsule, parents=parents, parent_kind=kind, parent_head=head)
            if verification.get("status") != "complete":
                return _result("invalid", "parent_spine_invalid", capsule=capsule, parents=parents, parent_kind=kind, parent_head=head)
            underlying = spine_capsules.get(head)
            if not isinstance(underlying, dict):
                return _result("invalid", "parent_spine_invalid", capsule=capsule, parents=parents, parent_kind=kind, parent_head=head)
            actual_carrier = underlying.get("carrier")
            root = underlying.get("root_digest")
            if not isinstance(root, str) or not root:
                return _result("invalid", "parent_spine_invalid", capsule=capsule, parents=parents, parent_kind=kind, parent_head=head)
            parent_roots = [root]
        else:
            if head not in braid_capsules:
                if head in spine_capsules:
                    return _result(
                        "invalid",
                        "parent_kind_mismatch",
                        capsule=capsule,
                        parents=parents,
                        parent_kind=kind,
                        parent_head=head,
                    )
                return _result(
                    "incomplete",
                    "parent_braid_incomplete",
                    capsule=capsule,
                    parents=parents,
                    parent_kind=kind,
                    parent_head=head,
                )
            verification = verify_braid(head, braid_ledger, spine_ledger)
            if verification.get("status") == "incomplete":
                return _result("incomplete", "parent_braid_incomplete", capsule=capsule, parents=parents, parent_kind=kind, parent_head=head)
            if verification.get("status") != "complete":
                return _result("invalid", "parent_braid_invalid", capsule=capsule, parents=parents, parent_kind=kind, parent_head=head)
            underlying = braid_capsules.get(head)
            if not isinstance(underlying, dict):
                return _result("invalid", "parent_braid_invalid", capsule=capsule, parents=parents, parent_kind=kind, parent_head=head)
            actual_carrier = underlying.get("carrier")
            parent_roots = _braid_roots(head, braid_ledger)
            if parent_roots is None:
                return _result("invalid", "parent_braid_invalid", capsule=capsule, parents=parents, parent_kind=kind, parent_head=head)

        if actual_carrier != parent.get("carrier"):
            return _result("invalid", "parent_carrier_mismatch", capsule=capsule, parents=parents, parent_kind=kind, parent_head=head)
        normalized_parent_roots = make_root_set(parent_roots)
        if canonical_digest(normalized_parent_roots) != parent.get("root_set_digest"):
            return _result("invalid", "parent_root_set_mismatch", capsule=capsule, parents=parents, parent_kind=kind, parent_head=head)
        represented_roots.extend(parent_roots)

    expected_inputs = [parent["carrier"] for parent in parents]
    merge_inputs = merge.get("inputs")
    if not isinstance(merge_inputs, list) or any(
        isinstance(value, bool) or not isinstance(value, int) for value in merge_inputs
    ):
        return _result("invalid", "merge_inputs_mismatch", capsule=capsule, parents=parents)
    if merge_inputs != expected_inputs:
        return _result("invalid", "merge_inputs_mismatch", capsule=capsule, parents=parents)
    merge_output = merge.get("output")
    if isinstance(merge_output, bool) or not isinstance(merge_output, int):
        return _result("invalid", "merge_output_mismatch", capsule=capsule, parents=parents)
    if merge_output != sum(expected_inputs):
        return _result("invalid", "merge_output_mismatch", capsule=capsule, parents=parents)
    if carrier != merge_output:
        return _result("invalid", "weave_carrier_mismatch", capsule=capsule, parents=parents)

    expected_root_set = make_root_set(represented_roots)
    if root_set != expected_root_set:
        return _result("invalid", "root_union_mismatch", capsule=capsule, parents=parents)
    if capsule.get("root_set_digest") != canonical_digest(expected_root_set):
        return _result("invalid", "root_set_digest_mismatch", capsule=capsule, parents=parents)

    return _result("complete", None, capsule=capsule, parents=parents)
