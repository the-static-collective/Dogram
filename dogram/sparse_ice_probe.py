from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from typing import Any, Mapping

from .ice_cube import _pixel_for, canonical_work_bytes, work_address


KIND = "dogram.sparse-ice-probe-receipt"
VERSION = "0"
POLICY = "adaptive-sparse-region-probe/v0"
CLAIM_SCOPE = "bounded-adaptive-region-witness/v0"


def _content_address(value: Any) -> str:
    data = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _parse_prior(prior: Mapping[str, str] | None) -> dict[str, Fraction] | None:
    if prior is None:
        return None
    if set(prior) != {"clean", "dirty"}:
        raise ValueError("prior must contain exactly clean and dirty")
    result = {key: Fraction(str(value)) for key, value in prior.items()}
    if any(value < 0 for value in result.values()):
        raise ValueError("prior weights must be nonnegative")
    if sum(result.values(), Fraction(0, 1)) != Fraction(1, 1):
        raise ValueError("prior weights must sum exactly to one")
    return result


def _validate_plan_and_claims(
    work: dict[str, Any],
    plan: dict[str, Any],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not isinstance(plan, dict):
        raise ValueError("plan must be an object")
    rows = plan.get("regions")
    if not isinstance(rows, list) or not rows:
        raise ValueError("plan.regions must be a nonempty array")
    if int(plan.get("region_count", -1)) != len(rows):
        raise ValueError("plan region_count mismatch")
    if plan.get("work_address") != work_address(work):
        raise ValueError("plan work address mismatch")

    expected_by_id: dict[str, dict[str, Any]] = {}
    for expected_index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError("region descriptor must be an object")
        descriptor = {
            "work_address": plan["work_address"],
            "index": expected_index,
            "x": int(row["x"]),
            "y": int(row["y"]),
        }
        expected_id = _content_address(descriptor)
        if row.get("index") != expected_index:
            raise ValueError("region indices must be contiguous")
        if row.get("region_id") != expected_id:
            raise ValueError("region identity mismatch")
        if expected_id in expected_by_id:
            raise ValueError("duplicate region identity")
        expected_by_id[expected_id] = row

    if not isinstance(claims, list) or len(claims) != len(rows):
        raise ValueError("claims must cover every declared region structurally")
    claim_by_id: dict[str, dict[str, Any]] = {}
    for claim in claims:
        if not isinstance(claim, dict):
            raise ValueError("region claim must be an object")
        region_id = str(claim.get("region_id") or "")
        if region_id in claim_by_id:
            raise ValueError("duplicate region claim")
        row = expected_by_id.get(region_id)
        if row is None:
            raise ValueError("claim names region outside plan")
        if int(claim.get("index", -1)) != int(row["index"]):
            raise ValueError("claim index mismatch")
        if int(claim.get("x", -1)) != int(row["x"]):
            raise ValueError("claim x mismatch")
        if int(claim.get("y", -1)) != int(row["y"]):
            raise ValueError("claim y mismatch")
        value = claim.get("value")
        if isinstance(value, bool) or not isinstance(value, int) or not (0 <= value <= 255):
            raise ValueError("claim value must be byte integer")
        claim_by_id[region_id] = claim

    return [
        claim_by_id[row["region_id"]]
        for row in rows
    ]


def deterministic_probe_indices(
    work: dict[str, Any],
    plan: dict[str, Any],
    root_probe_count: int,
) -> list[int]:
    total = int(plan["region_count"])
    if root_probe_count <= 0:
        raise ValueError("root_probe_count must be positive")
    target = min(root_probe_count, total)
    seed = hashlib.sha256(
        canonical_work_bytes(work)
        + str(plan.get("pixel_region_plan_id") or "").encode("utf-8")
        + b"|Dogram-SparseIceProbe-v0"
    ).digest()
    result: list[int] = []
    counter = 0
    while len(result) < target:
        block = hashlib.sha256(seed + counter.to_bytes(8, "big")).digest()
        index = int.from_bytes(block[:8], "big") % total
        if index not in result:
            result.append(index)
        counter += 1
    return result


def verify_sparse_region_claims(
    work: dict[str, Any],
    plan: dict[str, Any],
    claims: list[dict[str, Any]],
    *,
    root_probe_count: int = 4,
    prior: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Verify a structurally complete region claim set with adaptive value probes.

    The prior affects only expected-cost reporting. It cannot alter probe
    selection, branch behavior, evidence, or status.
    """
    try:
        ordered_claims = _validate_plan_and_claims(work, plan, claims)
        parsed_prior = _parse_prior(prior)
        root_indices = deterministic_probe_indices(
            work,
            plan,
            root_probe_count,
        )
        probed: list[int] = []
        mismatches: list[dict[str, Any]] = []

        def probe(index: int) -> None:
            if index in probed:
                return
            claim = ordered_claims[index]
            expected = _pixel_for(
                work,
                int(claim["x"]),
                int(claim["y"]),
            )
            probed.append(index)
            if int(claim["value"]) != expected:
                mismatches.append({
                    "index": index,
                    "region_id": claim["region_id"],
                    "claimed": int(claim["value"]),
                    "expected": expected,
                })

        for index in root_indices:
            probe(index)

        branch_triggered = bool(mismatches)
        if branch_triggered:
            for index in range(len(ordered_claims)):
                probe(index)

        total = len(ordered_claims)
        root_cost = len(root_indices)
        adaptive_worst_case = total
        fixed_full_cost = total
        expected_cost = None
        prior_record = None
        if parsed_prior is not None:
            expected = (
                parsed_prior["clean"] * root_cost
                + parsed_prior["dirty"] * total
            )
            expected_cost = _fraction_text(expected)
            prior_record = {
                "clean": _fraction_text(parsed_prior["clean"]),
                "dirty": _fraction_text(parsed_prior["dirty"]),
            }

        status = "OK" if not mismatches else "REFUSED"
        body = {
            "kind": KIND,
            "version": VERSION,
            "status": status,
            "policy": POLICY,
            "claim_scope": CLAIM_SCOPE,
            "work_address": work_address(work),
            "pixel_region_plan_id": plan.get("pixel_region_plan_id"),
            "region_count": total,
            "structural_region_coverage_verified": True,
            "root_probe_count": root_cost,
            "root_probe_indices": root_indices,
            "branch_triggered": branch_triggered,
            "probed_region_count": len(probed),
            "probed_region_indices": probed,
            "mismatches": mismatches,
            "cost_analysis": {
                "adaptive_observed_cost": len(probed),
                "adaptive_worst_case_cost": adaptive_worst_case,
                "fixed_full_cost": fixed_full_cost,
                "declared_prior": prior_record,
                "adaptive_expected_cost_if_prior_declared": expected_cost,
            },
            "laws": [
                "PRIOR != EVIDENCE",
                "LOWER EXPECTED COST != MORE TRUE",
                "POLICY != AUTHORITY",
                "COST ORDER != EVIDENCE ORDER",
                "STRUCTURAL COVERAGE != FULL VALUE VERIFICATION",
                "BOUNDED PROBES != UNIVERSAL PROOF",
            ],
        }
        return {
            **body,
            "receipt_id": _content_address(body),
        }
    except Exception as exc:
        body = {
            "kind": KIND,
            "version": VERSION,
            "status": "REFUSED",
            "policy": POLICY,
            "claim_scope": CLAIM_SCOPE,
            "error": f"{type(exc).__name__}: {exc}",
            "laws": [
                "PRIOR != EVIDENCE",
                "POLICY != AUTHORITY",
            ],
        }
        return {
            **body,
            "receipt_id": _content_address(body),
        }


__all__ = [
    "CLAIM_SCOPE",
    "KIND",
    "POLICY",
    "deterministic_probe_indices",
    "verify_sparse_region_claims",
]
