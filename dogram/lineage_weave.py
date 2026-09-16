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
