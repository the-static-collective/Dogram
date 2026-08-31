from __future__ import annotations

from typing import Any

from .canonical import sha256_json
from .program import Program, encode_program, program_digest
from .vm_types import VMExecution


class ReificationError(ValueError):
    def __init__(self, reason_code: str, residual: str):
        super().__init__(residual)
        self.reason_code = reason_code
        self.residual = residual


def _safe_digest(value: Any) -> str:
    try:
        return sha256_json(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ReificationError(
            "NON_CANONICAL_REIFICATION",
            f"value cannot cross reification membrane as canonical JSON ({type(exc).__name__})",
        ) from exc


def reify_program(program: Program) -> dict[str, Any]:
    data = {
        "schema": "dogram.program-data/v0",
        "program": encode_program(program),
        "program_digest": program_digest(program),
    }
    _safe_digest(data)
    return data


def reify_execution(
    program: Program,
    inputs: Any,
    execution: VMExecution,
) -> tuple[dict[str, Any], str]:
    runtime_data = execution.to_data()
    data = {
        "schema": "dogram.execution-data/v0",
        "program_digest": program_digest(program),
        "input_digest": _safe_digest(inputs),
        "status": runtime_data["status"],
        "result": runtime_data["result"],
        "reason_code": runtime_data["reason_code"],
        "residuals": runtime_data["residuals"],
        "step_trace": runtime_data["step_trace"],
        "consumed_input_addresses": runtime_data["consumed_input_addresses"],
        "fuel_remaining": runtime_data["fuel_remaining"],
    }
    return data, _safe_digest(data)


__all__ = [
    "ReificationError",
    "reify_execution",
    "reify_program",
]
