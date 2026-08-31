from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProductiveDesyncAssessment:
    status: str
    reason_code: str | None
    target_preserved: bool
    execution_residual: dict[str, Any]
    baseline_reach_count: int
    historical_reach_count: int
    closure_reach_count: int
    historical_expanded: bool
    closure_expanded: bool
    cut_declared: bool
    cut_budget: int
    cuts_used: int
    returned_to_coherence: bool

    def to_data(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "reason_code": self.reason_code,
            "target_preserved": self.target_preserved,
            "execution_residual": self.execution_residual,
            "baseline_reach_count": self.baseline_reach_count,
            "historical_reach_count": self.historical_reach_count,
            "closure_reach_count": self.closure_reach_count,
            "historical_expanded": self.historical_expanded,
            "closure_expanded": self.closure_expanded,
            "cut_declared": self.cut_declared,
            "cut_budget": self.cut_budget,
            "cuts_used": self.cuts_used,
            "returned_to_coherence": self.returned_to_coherence,
        }


def _is_count(value: int) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def assess_productive_desync(
    *,
    target_preserved: bool,
    execution_residual: dict[str, Any],
    baseline_reach_count: int,
    historical_reach_count: int,
    closure_reach_count: int,
    cut_declared: bool,
    cut_budget: int,
    cuts_used: int,
    returned_to_coherence: bool,
) -> ProductiveDesyncAssessment:
    if not isinstance(target_preserved, bool):
        raise ValueError("target_preserved must be boolean")
    if not isinstance(execution_residual, dict):
        raise ValueError("execution_residual must be an inert dictionary")
    if not isinstance(cut_declared, bool) or not isinstance(returned_to_coherence, bool):
        raise ValueError("cut/coherence flags must be booleans")
    for value in (baseline_reach_count, historical_reach_count, closure_reach_count, cut_budget, cuts_used):
        if not _is_count(value):
            raise ValueError("reach counts and cut counts must be non-negative integers")
    if historical_reach_count > closure_reach_count:
        raise ValueError("historical reach cannot exceed declared closure reach")

    historical_expanded = historical_reach_count > baseline_reach_count
    closure_expanded = closure_reach_count > baseline_reach_count

    if cuts_used > cut_budget:
        status, reason_code = "REFUSE", "CUT_BUDGET_EXCEEDED"
    elif not cut_declared:
        status, reason_code = "REFUSE", "UNTYPED_CUT"
    elif not returned_to_coherence:
        status, reason_code = "REFUSE", "NO_COHERENCE_RETURN"
    elif not target_preserved:
        status, reason_code = "REFUSE", "TARGET_NOT_PRESERVED"
    elif not execution_residual:
        status, reason_code = "REFUSE", "NO_EXECUTION_RESIDUAL"
    elif historical_expanded:
        status, reason_code = "WITNESS", None
    elif closure_expanded:
        status, reason_code = "POTENTIAL", "CLOSURE_ONLY"
    else:
        status, reason_code = "REFUSE", "NO_REACHABILITY_EXPANSION"

    return ProductiveDesyncAssessment(
        status=status,
        reason_code=reason_code,
        target_preserved=target_preserved,
        execution_residual=execution_residual,
        baseline_reach_count=baseline_reach_count,
        historical_reach_count=historical_reach_count,
        closure_reach_count=closure_reach_count,
        historical_expanded=historical_expanded,
        closure_expanded=closure_expanded,
        cut_declared=cut_declared,
        cut_budget=cut_budget,
        cuts_used=cuts_used,
        returned_to_coherence=returned_to_coherence,
    )


__all__ = ["ProductiveDesyncAssessment", "assess_productive_desync"]
