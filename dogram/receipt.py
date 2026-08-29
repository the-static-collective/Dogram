from __future__ import annotations

from typing import Any

from .canonical import canonical_json_bytes, sha256_json


def _base_receipt(specimen: dict[str, Any], operator: str, operator_version: int, consumed_inputs: list[str]) -> dict[str, Any]:
    return {
        "schema": "dogram.receipt/v0",
        "specimen_id": specimen.get("specimen_id"),
        "operator": operator,
        "operator_version": operator_version,
        "input_digest": sha256_json(specimen),
        "consumed_inputs": sorted(set(consumed_inputs)),
        "result": None,
        "residuals": [],
        "warnings": [],
    }


def ok_receipt(specimen: dict[str, Any], operator: str, operator_version: int, consumed_inputs: list[str], result: dict[str, Any]) -> dict[str, Any]:
    receipt = _base_receipt(specimen, operator, operator_version, consumed_inputs)
    receipt["status"] = "OK"
    receipt["result"] = result
    return receipt


def refusal_receipt(
    specimen: dict[str, Any],
    operator: str,
    operator_version: int,
    status: str,
    reason_code: str,
    residuals: list[str] | None = None,
    consumed_inputs: list[str] | None = None,
) -> dict[str, Any]:
    receipt = _base_receipt(specimen, operator, operator_version, consumed_inputs or [])
    receipt["status"] = status
    receipt["reason_code"] = reason_code
    receipt["residuals"] = residuals or []
    return receipt


def canonical_receipt_bytes(receipt: dict[str, Any]) -> bytes:
    return canonical_json_bytes(receipt)
