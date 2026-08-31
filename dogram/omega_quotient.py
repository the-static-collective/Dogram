from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .execution_cut import make_execution_cut, typed_footprint_residual
from .omega import OmegaConfig, run_omega_cycle
from .program import Program
from .registry import Registry


_SUPPORTED_PROBES = frozenset(
    {"result", "status", "reason_code", "residuals", "step_trace"}
)
_DOES_NOT_ESTABLISH = [
    "global_equivalence",
    "causal_irrelevance",
    "evidence",
    "support",
    "truth",
    "authority",
    "cross-runtime replay",
]


@dataclass(frozen=True)
class TargetFamily:
    id: str
    probes: tuple[str, ...]
    declared_before_comparison: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id:
            raise ValueError("target family id must be a non-empty string")
        if not isinstance(self.probes, tuple) or not self.probes:
            raise ValueError("target family probes must be a non-empty tuple")
        if any(not isinstance(probe, str) or not probe for probe in self.probes):
            raise ValueError("target family probes must be non-empty strings")
        if len(set(self.probes)) != len(self.probes):
            raise ValueError("target family probes must be unique")
        if not isinstance(self.declared_before_comparison, bool):
            raise ValueError("declared_before_comparison must be boolean")

    def to_data(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "declared_before_comparison": self.declared_before_comparison,
            "probes": list(self.probes),
        }


@dataclass(frozen=True)
class QuotientComparison:
    status: str
    reason_code: str | None
    target_verdict: str | None
    footprint_residual: dict[str, Any]

    def to_data(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "reason_code": self.reason_code,
            "target_verdict": self.target_verdict,
            "footprint_residual": self.footprint_residual,
        }


@dataclass(frozen=True)
class OmegaQuotientResult:
    status: str
    reason_code: str | None
    receipt: dict[str, Any]


def _refused_comparison(reason_code: str) -> QuotientComparison:
    return QuotientComparison(
        status="REFUSE",
        reason_code=reason_code,
        target_verdict=None,
        footprint_residual={},
    )


def compare_execution_cuts(
    before: dict[str, Any],
    after: dict[str, Any],
    target: TargetFamily,
    *,
    same_runtime_invocation: bool = True,
) -> QuotientComparison:
    if not target.declared_before_comparison:
        return _refused_comparison("TARGET_NOT_PREDECLARED")

    if before.get("input_digest") != after.get("input_digest"):
        return _refused_comparison("INPUT_CUT_MISMATCH")

    if not isinstance(same_runtime_invocation, bool):
        raise ValueError("same_runtime_invocation must be boolean")
    if not same_runtime_invocation:
        return QuotientComparison(
            status="HOLD",
            reason_code="RUNTIME_BODY_UNPINNED",
            target_verdict=None,
            footprint_residual={},
        )

    if any(probe not in _SUPPORTED_PROBES for probe in target.probes):
        return _refused_comparison("UNSUPPORTED_TARGET_PROBE")

    footprint_residual = typed_footprint_residual(before, after)
    equivalent = all(before.get(probe) == after.get(probe) for probe in target.probes)
    return QuotientComparison(
        status="OK",
        reason_code=None,
        target_verdict=(
            "EQUIVALENT_UNDER_T" if equivalent else "DIFFERENT_UNDER_T"
        ),
        footprint_residual=footprint_residual,
    )


def _receipt_shell(target: TargetFamily) -> dict[str, Any]:
    return {
        "schema": "dogram.omega-quotient/v0",
        "omega_cycle": None,
        "baseline": None,
        "candidate": None,
        "input_digest": None,
        "target_family": target.to_data(),
        "target_verdict": None,
        "footprint_residual": None,
        "same_runtime_invocation": True,
        "does_not_establish": list(_DOES_NOT_ESTABLISH),
    }


def run_omega_quotient(
    *,
    program: Program,
    inputs: Any,
    declared_target_step: str | None,
    proposal_id: str,
    target: TargetFamily,
    registry: Registry,
    config: OmegaConfig | None = None,
) -> OmegaQuotientResult:
    config = config or OmegaConfig()
    receipt = _receipt_shell(target)

    if not target.declared_before_comparison:
        return OmegaQuotientResult(
            status="REFUSE",
            reason_code="TARGET_NOT_PREDECLARED",
            receipt=receipt,
        )

    cycle = run_omega_cycle(
        program,
        inputs,
        declared_target_step,
        proposal_id,
        registry,
        config,
    )
    receipt["omega_cycle"] = cycle.receipt

    if cycle.status != "OK":
        return OmegaQuotientResult(
            status="REFUSE",
            reason_code=cycle.reason_code,
            receipt=receipt,
        )

    cycle_receipt = cycle.receipt
    before_data = cycle_receipt["execution_before"]
    after_data = cycle_receipt["execution_after"]
    if before_data is None or after_data is None:
        return OmegaQuotientResult(
            status="REFUSE",
            reason_code="MISSING_EXECUTION_CUT_SOURCE",
            receipt=receipt,
        )

    fuel_initial = config.exec_config.max_exec_steps
    before_cut = make_execution_cut(before_data, fuel_initial=fuel_initial)
    after_cut = make_execution_cut(after_data, fuel_initial=fuel_initial)

    receipt["baseline"] = {
        "program_digest": cycle_receipt["program_before"]["program_digest"],
        "execution_digest": cycle_receipt["execution_before_digest"],
        "execution_cut": before_cut,
    }
    receipt["candidate"] = {
        "program_digest": cycle_receipt["program_after"]["program_digest"],
        "execution_digest": cycle_receipt["execution_after_digest"],
        "execution_cut": after_cut,
    }
    receipt["input_digest"] = before_cut["input_digest"]

    comparison = compare_execution_cuts(
        before_cut,
        after_cut,
        target,
        same_runtime_invocation=True,
    )
    receipt["target_verdict"] = comparison.target_verdict
    receipt["footprint_residual"] = comparison.footprint_residual

    if comparison.status != "OK":
        return OmegaQuotientResult(
            status=comparison.status,
            reason_code=comparison.reason_code,
            receipt=receipt,
        )

    return OmegaQuotientResult(
        status="OK",
        reason_code=None,
        receipt=receipt,
    )


__all__ = [
    "OmegaQuotientResult",
    "QuotientComparison",
    "TargetFamily",
    "compare_execution_cuts",
    "run_omega_quotient",
]
