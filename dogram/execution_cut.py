from __future__ import annotations

from copy import deepcopy
from typing import Any


_EXECUTION_DATA_SCHEMA = "dogram.execution-data/v0"
_EXECUTION_CUT_SCHEMA = "dogram.execution-cut/v0"
_REQUIRED_EXECUTION_FIELDS = (
    "program_digest",
    "input_digest",
    "status",
    "result",
    "reason_code",
    "residuals",
    "step_trace",
    "consumed_input_addresses",
    "fuel_remaining",
)


def _require_mapping(value: Any, *, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a dictionary")
    return value


def _require_execution_data(execution_data: Any) -> dict[str, Any]:
    data = _require_mapping(execution_data, name="execution_data")
    if data.get("schema") != _EXECUTION_DATA_SCHEMA:
        raise ValueError("execution_data must use dogram.execution-data/v0")
    missing = [field for field in _REQUIRED_EXECUTION_FIELDS if field not in data]
    if missing:
        raise ValueError(f"execution_data missing required fields: {', '.join(missing)}")
    if not isinstance(data["consumed_input_addresses"], list):
        raise ValueError("consumed_input_addresses must be an ordered list")
    if not isinstance(data["step_trace"], list):
        raise ValueError("step_trace must be an ordered list")
    if type(data["fuel_remaining"]) is not int or data["fuel_remaining"] < 0:
        raise ValueError("fuel_remaining must be a non-negative integer")
    return data


def _require_execution_cut(cut: Any) -> dict[str, Any]:
    data = _require_mapping(cut, name="execution_cut")
    if data.get("schema") != _EXECUTION_CUT_SCHEMA:
        raise ValueError("execution_cut must use dogram.execution-cut/v0")
    return data


def make_execution_cut(
    execution_data: dict[str, Any],
    *,
    fuel_initial: int,
) -> dict[str, Any]:
    data = _require_execution_data(execution_data)
    if type(fuel_initial) is not int or fuel_initial < 0:
        raise ValueError("fuel_initial must be a non-negative integer")
    if data["fuel_remaining"] > fuel_initial:
        raise ValueError("fuel_remaining cannot exceed fuel_initial")

    return {
        "schema": _EXECUTION_CUT_SCHEMA,
        "program_digest": data["program_digest"],
        "input_digest": data["input_digest"],
        "status": data["status"],
        "result": deepcopy(data["result"]),
        "reason_code": data["reason_code"],
        "residuals": deepcopy(data["residuals"]),
        "consumed_input_addresses": deepcopy(data["consumed_input_addresses"]),
        "step_trace": deepcopy(data["step_trace"]),
        "fuel_initial": fuel_initial,
        "fuel_remaining": data["fuel_remaining"],
    }


def _component_delta(before: Any, after: Any) -> dict[str, Any]:
    if before == after:
        return {"relation": "SAME"}
    return {
        "before": deepcopy(before),
        "after": deepcopy(after),
    }


def typed_footprint_residual(
    before: dict[str, Any],
    after: dict[str, Any],
) -> dict[str, Any]:
    left = _require_execution_cut(before)
    right = _require_execution_cut(after)

    residual: dict[str, Any] = {}
    changed_components: list[str] = []

    for field in (
        "status",
        "result",
        "reason_code",
        "residuals",
        "consumed_input_addresses",
        "step_trace",
    ):
        residual[field] = _component_delta(left.get(field), right.get(field))
        if left.get(field) != right.get(field):
            changed_components.append(field)

    if left["fuel_initial"] == right["fuel_initial"]:
        if left["fuel_remaining"] == right["fuel_remaining"]:
            residual["fuel"] = {
                "relation": "SAME",
                "initial": left["fuel_initial"],
                "remaining": left["fuel_remaining"],
            }
        else:
            residual["fuel"] = {
                "initial": left["fuel_initial"],
                "before_remaining": left["fuel_remaining"],
                "after_remaining": right["fuel_remaining"],
            }
            changed_components.append("fuel")
    else:
        residual["fuel"] = {
            "before_initial": left["fuel_initial"],
            "after_initial": right["fuel_initial"],
            "before_remaining": left["fuel_remaining"],
            "after_remaining": right["fuel_remaining"],
        }
        changed_components.append("fuel")

    residual["changed_components"] = changed_components
    return residual


__all__ = [
    "make_execution_cut",
    "typed_footprint_residual",
]
