from __future__ import annotations

from typing import Any, Callable

from .ablate import AblateInputError, evaluate_ablate
from .delta import DeltaInputError, evaluate_delta
from .reach import ReachInputError, evaluate_reach
from .receipt import ok_receipt, refusal_receipt
from .rectangle import RectangleInputError, evaluate_rectangle

Evaluator = Callable[[dict[str, Any]], tuple[dict[str, Any], list[str]]]

OPERATORS: dict[tuple[str, int], Evaluator] = {
    ("delta", 1): evaluate_delta,
    ("rectangle", 1): evaluate_rectangle,
    ("ablate", 1): evaluate_ablate,
    ("reach", 1): evaluate_reach,
}

_OPERATOR_NAMES = {name for name, _ in OPERATORS}
_INPUT_ERRORS = (DeltaInputError, RectangleInputError, AblateInputError, ReachInputError)


def _identity(specimen: Any) -> tuple[dict[str, Any], str, int]:
    if not isinstance(specimen, dict):
        return {}, "unknown", 0
    operator = specimen.get("operator") if isinstance(specimen.get("operator"), str) else "unknown"
    version = specimen.get("operator_version") if type(specimen.get("operator_version")) is int else 0
    return specimen, operator, version


def evaluate_specimen(specimen: dict[str, Any]) -> dict[str, Any]:
    raw, operator, version = _identity(specimen)
    required = {"schema", "specimen_id", "operator", "operator_version", "inputs", "assumptions", "metadata"}
    if (
        not isinstance(specimen, dict)
        or set(specimen) != required
        or specimen.get("schema") != "dogram.specimen/v0"
        or not isinstance(specimen.get("specimen_id"), str)
        or not specimen.get("specimen_id")
        or not isinstance(specimen.get("operator"), str)
        or type(specimen.get("operator_version")) is not int
        or not isinstance(specimen.get("inputs"), dict)
        or not isinstance(specimen.get("assumptions"), list)
        or not isinstance(specimen.get("metadata"), dict)
    ):
        return refusal_receipt(raw, operator, version, "REFUSE", "MALFORMED_SPECIMEN", ["invalid dogram.specimen/v0 envelope"])

    if operator not in _OPERATOR_NAMES:
        return refusal_receipt(specimen, operator, version, "REFUSE", "UNSUPPORTED_OPERATOR", [operator])
    if (operator, version) not in OPERATORS:
        return refusal_receipt(specimen, operator, version, "REFUSE", "UNSUPPORTED_OPERATOR_VERSION", [str(version)])

    evaluator = OPERATORS[(operator, version)]
    try:
        result, consumed = evaluator(specimen["inputs"])
    except _INPUT_ERRORS as exc:
        return refusal_receipt(specimen, operator, version, "REFUSE", exc.reason_code, [exc.residual])
    return ok_receipt(specimen, operator, version, consumed, result)
