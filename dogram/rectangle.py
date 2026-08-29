from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from .values import ScalarValue, ValueDecodeError, decode_value


@dataclass
class RectangleInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


def _numeric(value: ScalarValue) -> int | Fraction | float:
    if value.kind == "opaque":
        raise RectangleInputError("MIXED_VALUE_MODES", "opaque values are not numeric")
    assert isinstance(value.value, (int, Fraction, float))
    return value.value


def _encode_number(value: int | Fraction | float) -> dict[str, Any]:
    if isinstance(value, float):
        return {"kind": "float", "value": value}
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return {"kind": "integer", "value": value.numerator}
        return {"kind": "rational", "numerator": value.numerator, "denominator": value.denominator}
    return {"kind": "integer", "value": value}


def evaluate_rectangle(inputs: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    if not isinstance(inputs, dict) or not isinstance(inputs.get("axis_a"), str) or not isinstance(inputs.get("axis_b"), str):
        raise RectangleInputError("MALFORMED_INPUTS", "axis_a and axis_b must be strings")
    cells = inputs.get("cells")
    if not isinstance(cells, dict) or set(cells) != {"00", "01", "10", "11"}:
        raise RectangleInputError("INVALID_RECTANGLE", "cells must contain exactly 00,01,10,11")
    try:
        decoded = {k: decode_value(v) for k, v in cells.items()}
    except ValueDecodeError as exc:
        raise RectangleInputError("INVALID_VALUE", str(exc)) from exc

    kinds = {v.kind for v in decoded.values()}
    any_opaque = "opaque" in kinds
    if any_opaque and kinds != {"opaque"}:
        raise RectangleInputError("MIXED_VALUE_MODES", "rectangle cannot mix opaque and numeric cells")

    consumed = ["inputs.axis_a", "inputs.axis_b"] + [f"inputs.cells.{k}" for k in ("00", "01", "10", "11")]

    if any_opaque:
        eq_b0 = decoded["00"].value == decoded["10"].value
        eq_b1 = decoded["01"].value == decoded["11"].value
        return {
            "mode": "equivalence",
            "equivalent_across_axis_a_when_b0": eq_b0,
            "equivalent_across_axis_a_when_b1": eq_b1,
            "interaction_detected": eq_b0 != eq_b1,
        }, consumed

    values = {k: _numeric(v) for k, v in decoded.items()}
    if any(isinstance(v, float) for v in values.values()):
        mixed: int | Fraction | float = float(values["11"]) - float(values["10"]) - float(values["01"]) + float(values["00"])
    else:
        exact = {k: Fraction(v) for k, v in values.items()}
        mixed = exact["11"] - exact["10"] - exact["01"] + exact["00"]
    return {
        "mode": "numeric",
        "mixed_delta": _encode_number(mixed),
        "interaction_detected": mixed != 0,
    }, consumed
