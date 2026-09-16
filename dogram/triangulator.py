"""Bounded order-comparison kernel for TRIANGULATOR-001.

This module is not wired into Dogram's public operator floor. It receipts how
explicit integer operators compose in two orders and classifies the resulting
delta only under a declared structure test.
"""

from copy import deepcopy
from dataclasses import dataclass
from typing import Callable


StructureTest = Callable[[int, int], bool]


@dataclass(frozen=True)
class Operator:
    """Named unary integer operator retained with composition receipts."""

    name: str
    function: Callable[[int], int]

    def __call__(self, value: int) -> int:
        return self.function(value)


def _require_nonnegative_integer(value: int, *, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")


def _triangular(value: int) -> int:
    _require_nonnegative_integer(value, name="triangular input")
    return value * (value + 1) // 2


def _square(value: int) -> int:
    _require_nonnegative_integer(value, name="square input")
    return value * value


triangular = Operator("triangular", _triangular)
square = Operator("square", _square)


def add(amount: int) -> Operator:
    if isinstance(amount, bool) or not isinstance(amount, int):
        raise ValueError("add amount must be an integer")
    return Operator(f"add({amount})", lambda value: value + amount)


def compare_order(
    carrier: int,
    first: Operator,
    second: Operator,
    *,
    structure_test: StructureTest | None = None,
    structure_label: str | None = None,
) -> dict[str, object]:
    """Receipt second(first(C)) versus first(second(C)) and their signed delta."""
    if isinstance(carrier, bool) or not isinstance(carrier, int):
        raise ValueError("carrier must be an integer")
    if structure_test is not None and not structure_label:
        raise ValueError("structure_label is required when structure_test is declared")

    first_value = first(carrier)
    second_after_first = second(first_value)
    second_value = second(carrier)
    first_after_second = first(second_value)
    delta = second_after_first - first_after_second

    structure: dict[str, object] = {
        "declared": structure_test is not None,
        "label": structure_label,
        "passed": None,
    }
    if delta == 0:
        classification = "zero"
    elif structure_test is None:
        classification = "nonzero_unclassified"
    else:
        passed = bool(structure_test(carrier, delta))
        structure["passed"] = passed
        classification = (
            "nonzero_structured"
            if passed
            else "nonzero_not_structured_under_declared_test"
        )

    return {
        "carrier": carrier,
        "operators": {"first": first.name, "second": second.name},
        "paths": {
            "second_after_first": second_after_first,
            "first_after_second": first_after_second,
        },
        "delta": delta,
        "classification": classification,
        "structure": structure,
    }


def continue_from_delta(
    parent_receipt: dict[str, object],
    operator: Operator,
) -> dict[str, object]:
    """Reuse a parent delta as a new carrier while retaining parent ancestry."""
    delta = parent_receipt.get("delta")
    if isinstance(delta, bool) or not isinstance(delta, int):
        raise ValueError("parent receipt must contain an integer delta")

    required = ("carrier", "operators", "paths", "classification")
    missing = [key for key in required if key not in parent_receipt]
    if missing:
        raise ValueError(f"parent receipt is missing ancestry fields: {', '.join(missing)}")

    ancestry = {
        "parent_specimen": parent_receipt.get("specimen"),
        "parent_carrier": deepcopy(parent_receipt["carrier"]),
        "parent_operators": deepcopy(parent_receipt["operators"]),
        "parent_paths": deepcopy(parent_receipt["paths"]),
        "parent_delta": delta,
        "parent_classification": deepcopy(parent_receipt["classification"]),
    }

    return {
        "specimen": "DELTA-AS-CARRIER-001",
        "carrier": delta,
        "carrier_origin": "parent_delta",
        "operator": operator.name,
        "projection": operator(delta),
        "ancestry": ancestry,
    }


def triangulator_001_receipt() -> dict[str, object]:
    """Frozen n=5 square/triangular specimen plus exact 3T5 numeric anchors."""
    carrier = 5
    expected_delta = triangular(carrier - 1) ** 2
    receipt = compare_order(
        carrier,
        square,
        triangular,
        structure_test=lambda n, delta: delta == triangular(n - 1) ** 2,
        structure_label="delta == triangular(carrier - 1)^2",
    )
    receipt["specimen"] = "TRIANGULATOR-001"
    receipt["paths"]["triangular_after_square"] = receipt["paths"]["second_after_first"]
    receipt["paths"]["square_after_triangular"] = receipt["paths"]["first_after_second"]
    receipt["structure"]["expected_delta"] = expected_delta
    receipt["anchors"] = {
        "3^5": 3**5,
        "T_(5^2)": triangular(5**2),
        "T_5^2": triangular(5) ** 2,
        "325-243": triangular(5**2) - 3**5,
        "3^4+1": 3**4 + 1,
        "022100_base3": int("022100", 3),
    }
    return receipt
