from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .values import ValueDecodeError, compare_values, decode_value


@dataclass
class DeltaInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


def evaluate_delta(inputs: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    if not isinstance(inputs, dict):
        raise DeltaInputError("MALFORMED_INPUTS", "inputs must be an object")
    order = inputs.get("boundary_order")
    left = inputs.get("left")
    right = inputs.get("right")
    if not isinstance(order, list) or not order or any(not isinstance(x, str) or not x for x in order) or len(set(order)) != len(order):
        raise DeltaInputError("INVALID_BOUNDARY_ORDER", "boundary_order must be a non-empty list of unique strings")
    if not isinstance(left, dict) or not isinstance(right, dict):
        raise DeltaInputError("MALFORMED_TRACE", "left and right must be objects")
    if set(left) != set(order) or set(right) != set(order):
        raise DeltaInputError("BOUNDARY_KEYS_MISMATCH", "left/right keys must exactly match boundary_order")

    comparisons: list[dict[str, Any]] = []
    consumed: list[str] = ["inputs.boundary_order"]
    first_difference: str | None = None
    for boundary in order:
        try:
            comparison = compare_values(decode_value(left[boundary]), decode_value(right[boundary]))
        except ValueDecodeError as exc:
            raise DeltaInputError("INVALID_VALUE", str(exc)) from exc
        item = {"boundary": boundary, **comparison}
        comparisons.append(item)
        consumed.extend([f"inputs.left.{boundary}", f"inputs.right.{boundary}"])
        if first_difference is None and comparison["relation"] == "DIFFERENT":
            first_difference = boundary
    return {"comparisons": comparisons, "first_difference": first_difference}, consumed
