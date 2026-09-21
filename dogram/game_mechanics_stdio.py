from __future__ import annotations

import json
import sys
from typing import Any

from .budget_rounding_residual import receipt_integer_budget

REQUEST_SCHEMA = "dogram/game-mechanics-stdio-request/v0.1"
RESPONSE_SCHEMA = "dogram/game-mechanics-stdio-response/v0.1"


def _error(code: str, detail: str) -> dict[str, Any]:
    return {
        "schema": RESPONSE_SCHEMA,
        "ok": False,
        "error": {"code": code, "detail": detail},
        "authority": "none",
    }


def _string_list(value: object, *, field: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{field} must be an array of strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{field} must not contain duplicates")
    return value


def _successor_delta(request: dict[str, Any]) -> dict[str, Any]:
    before = _string_list(request.get("beforeActions"), field="beforeActions")
    after = _string_list(request.get("afterActions"), field="afterActions")
    before_set = set(before)
    after_set = set(after)
    return {
        "experiment": "SUCCESSOR-DELTA-001",
        "before_actions": sorted(before_set),
        "after_actions": sorted(after_set),
        "foreclosed": sorted(before_set - after_set),
        "newly_available": sorted(after_set - before_set),
        "retained": sorted(before_set & after_set),
        "authority": "none",
        "non_claims": [
            "available successor != occurred successor",
            "foreclosed successor != morally preferred alternative",
            "same successor set != same underlying state",
        ],
    }


def _budget_rounding(request: dict[str, Any]) -> dict[str, Any]:
    weights = request.get("weights")
    budget = request.get("budget")
    method = request.get("method", "largest_fractional_remainder")

    if not isinstance(weights, dict):
        raise ValueError("weights must be an object")
    normalized: dict[str, int] = {}
    for label, weight in weights.items():
        if not isinstance(label, str):
            raise ValueError("weight labels must be strings")
        if isinstance(weight, bool) or not isinstance(weight, int):
            raise ValueError("weights must be positive integers")
        normalized[label] = weight
    if isinstance(budget, bool) or not isinstance(budget, int):
        raise ValueError("budget must be a non-negative integer")
    if not isinstance(method, str):
        raise ValueError("method must be a string")

    return receipt_integer_budget(normalized, budget, method=method)


def handle_request(value: object) -> dict[str, Any]:
    if not isinstance(value, dict):
        return _error("REQUEST_NOT_OBJECT", "request must be a JSON object")
    if value.get("schema") != REQUEST_SCHEMA:
        return _error("SCHEMA_MISMATCH", f"expected {REQUEST_SCHEMA}")

    operation = value.get("operation")
    try:
        if operation == "budget_rounding":
            result = _budget_rounding(value)
        elif operation == "successor_delta":
            result = _successor_delta(value)
        else:
            return _error("UNKNOWN_OPERATION", f"unknown operation: {operation!r}")
    except (TypeError, ValueError) as exc:
        return _error("INVALID_INPUT", str(exc))

    return {
        "schema": RESPONSE_SCHEMA,
        "ok": True,
        "operation": operation,
        "result": result,
        "authority": "none",
        "non_claims": [
            "calculation receipt does not establish truth, virtue, obligation, or human worth",
            "Dogram does not choose the move",
        ],
    }


def main() -> int:
    raw = sys.stdin.read()
    try:
        request = json.loads(raw)
    except json.JSONDecodeError as exc:
        response = _error("MALFORMED_JSON", str(exc))
    else:
        response = handle_request(request)

    sys.stdout.write(json.dumps(response, sort_keys=True))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
