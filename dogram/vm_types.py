from __future__ import annotations

from dataclasses import dataclass
from typing import Any

InputAddress = tuple[str | int, ...]


@dataclass(frozen=True)
class VMConfig:
    max_exec_steps: int = 1000
    max_call_depth: int = 8

    def __post_init__(self) -> None:
        if type(self.max_exec_steps) is not int or self.max_exec_steps < 0:
            raise ValueError("max_exec_steps must be a non-negative integer")
        if type(self.max_call_depth) is not int or self.max_call_depth < 1:
            raise ValueError("max_call_depth must be a positive integer")


@dataclass(frozen=True)
class StepTrace:
    step_id: str
    op: str
    arg_digest: str
    result_digest: str
    fuel_before: int
    fuel_after: int

    def to_data(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "op": self.op,
            "arg_digest": self.arg_digest,
            "result_digest": self.result_digest,
            "fuel_before": self.fuel_before,
            "fuel_after": self.fuel_after,
        }


@dataclass(frozen=True)
class VMExecution:
    status: str
    result: Any
    reason_code: str | None
    residuals: tuple[str, ...]
    step_trace: tuple[StepTrace, ...]
    consumed_input_addresses: tuple[InputAddress, ...]
    fuel_remaining: int

    def to_data(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "result": self.result,
            "reason_code": self.reason_code,
            "residuals": list(self.residuals),
            "step_trace": [entry.to_data() for entry in self.step_trace],
            "consumed_input_addresses": [list(address) for address in self.consumed_input_addresses],
            "fuel_remaining": self.fuel_remaining,
        }
