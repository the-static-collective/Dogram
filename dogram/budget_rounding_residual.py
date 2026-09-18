from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction

_METHODS = {
    "largest_fractional_remainder",
    "declared_order_remainder",
}


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def receipt_integer_budget(
    weights: Mapping[str, int],
    budget: int,
    *,
    method: str = "largest_fractional_remainder",
) -> dict[str, object]:
    """Receipt exact proportional targets and one declared integer realization."""
    if not weights:
        raise ValueError("weights must be non-empty")
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a non-negative integer")
    if any(type(weight) is not int or weight <= 0 for weight in weights.values()):
        raise ValueError("weights must be positive integers")
    if method not in _METHODS:
        raise ValueError(f"unknown method: {method}")

    declared_order = [str(label) for label in weights]
    normalized_weights = {str(label): weight for label, weight in weights.items()}
    total_weight = sum(normalized_weights.values())
    exact = {
        label: Fraction(budget * weight, total_weight)
        for label, weight in normalized_weights.items()
    }
    allocation = {
        label: value.numerator // value.denominator
        for label, value in exact.items()
    }
    remaining = budget - sum(allocation.values())

    if method == "largest_fractional_remainder":
        remainder_order = sorted(
            exact,
            key=lambda label: (
                -(exact[label] - allocation[label]),
                label,
            ),
        )
    else:
        remainder_order = declared_order

    for label in remainder_order[:remaining]:
        allocation[label] += 1

    residuals = {
        label: Fraction(allocation[label]) - exact[label]
        for label in exact
    }
    residual_sum = sum(residuals.values(), Fraction(0))
    labels = sorted(exact)

    return {
        "experiment": "BUDGET-ROUNDING-RESIDUAL-001",
        "method": method,
        "budget": budget,
        "weights": {label: normalized_weights[label] for label in labels},
        "declared_order": declared_order,
        "exact": {label: _fraction_text(exact[label]) for label in labels},
        "allocation": {label: allocation[label] for label in labels},
        "residuals": {label: _fraction_text(residuals[label]) for label in labels},
        "residual_sum": _fraction_text(residual_sum),
        "allocated_total": sum(allocation.values()),
        "authority": "none",
    }
