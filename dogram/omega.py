from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .canonical import sha256_json
from .gate import GateLimits, phase_gate
from .program import Program, decode_program
from .reify import ReificationError, reify_execution, reify_program
from .registry import Registry
from .vm import VMConfig, execute_program


_STDLIB = Path(__file__).with_name("stdlib")


def _load_program(name: str) -> Program:
    return decode_program(json.loads((_STDLIB / name).read_text()))


@dataclass(frozen=True)
class OmegaConfig:
    exec_config: VMConfig = VMConfig()
    meta_config: VMConfig = VMConfig(max_exec_steps=32)
    gate_limits: GateLimits = GateLimits()


@dataclass(frozen=True)
class OmegaCycleResult:
    status: str
    reason_code: str | None
    receipt: dict[str, Any]


def _receipt_shell(proposal_id: str) -> dict[str, Any]:
    return {
        "schema": "dogram.omega-cycle-receipt/v0",
        "proposal_id": proposal_id,
        "meta_rounds": 0,
        "program_before": None,
        "execution_before": None,
        "execution_before_digest": None,
        "meta_execution": None,
        "gate": None,
        "program_after": None,
        "execution_after": None,
        "execution_after_digest": None,
        "comparison": None,
    }


def _result_comparison(
    left: Any,
    right: Any,
    registry: Registry,
    config: VMConfig,
):
    delta_program = _load_program("delta.mathal.json")
    delta_inputs = {
        "boundary_order": ["result_digest"],
        "left": {
            "result_digest": {
                "kind": "opaque",
                "value": sha256_json(left),
            }
        },
        "right": {
            "result_digest": {
                "kind": "opaque",
                "value": sha256_json(right),
            }
        },
    }
    return execute_program(delta_program, delta_inputs, registry, config)


def run_omega_cycle(
    program: Program,
    inputs: Any,
    declared_target_step: str | None,
    proposal_id: str,
    registry: Registry,
    config: OmegaConfig | None = None,
) -> OmegaCycleResult:
    config = config or OmegaConfig()
    receipt = _receipt_shell(proposal_id)

    receipt["program_before"] = reify_program(program)
    execution_before = execute_program(
        program,
        inputs,
        registry,
        config.exec_config,
    )

    try:
        execution_before_data, execution_before_digest = reify_execution(
            program,
            inputs,
            execution_before,
        )
    except ReificationError:
        return OmegaCycleResult("REFUSE", "REIFICATION_REFUSED", receipt)

    receipt["execution_before"] = execution_before_data
    receipt["execution_before_digest"] = execution_before_digest

    meta_inputs: dict[str, Any] = {
        "program_data": receipt["program_before"],
        "execution_data": execution_before_data,
        "execution_digest": execution_before_digest,
        "proposal_id": proposal_id,
    }
    if declared_target_step is not None:
        meta_inputs["declared_target_step"] = declared_target_step

    meta_execution = execute_program(
        _load_program("meta_remove_declared_step.mathal.json"),
        meta_inputs,
        registry,
        config.meta_config,
    )
    receipt["meta_rounds"] = 1
    receipt["meta_execution"] = meta_execution.to_data()

    if meta_execution.status != "OK":
        return OmegaCycleResult("REFUSE", "META_EXECUTION_REFUSED", receipt)

    gate = phase_gate(
        meta_execution.result,
        program,
        execution_before_data,
        registry,
        config.gate_limits,
    )
    receipt["gate"] = gate.to_data()

    if gate.status != "ADMIT" or gate.program is None:
        return OmegaCycleResult("REFUSE", gate.reason_code, receipt)

    candidate = gate.program
    receipt["program_after"] = reify_program(candidate)
    execution_after = execute_program(
        candidate,
        inputs,
        registry,
        config.exec_config,
    )

    try:
        execution_after_data, execution_after_digest = reify_execution(
            candidate,
            inputs,
            execution_after,
        )
    except ReificationError:
        return OmegaCycleResult("REFUSE", "REIFICATION_REFUSED", receipt)

    receipt["execution_after"] = execution_after_data
    receipt["execution_after_digest"] = execution_after_digest

    if execution_after.status != "OK":
        return OmegaCycleResult("REFUSE", "EXECUTION_AFTER_REFUSED", receipt)

    comparison_execution = _result_comparison(
        execution_before.result,
        execution_after.result,
        registry,
        config.exec_config,
    )
    if comparison_execution.status != "OK":
        receipt["comparison"] = comparison_execution.to_data()
        return OmegaCycleResult("REFUSE", "COMPARISON_EXECUTION_REFUSED", receipt)

    receipt["comparison"] = comparison_execution.result
    return OmegaCycleResult("OK", None, receipt)


__all__ = [
    "OmegaConfig",
    "OmegaCycleResult",
    "run_omega_cycle",
]
