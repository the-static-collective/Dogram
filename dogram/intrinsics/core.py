from __future__ import annotations

from fractions import Fraction
from typing import Any

from ..canonical import canonical_json_bytes
from ..values import ScalarValue, ValueDecodeError, compare_values, decode_value, encode_value


class IntrinsicRefusal(ValueError):
    def __init__(self, reason_code: str, residual: str):
        super().__init__(residual)
        self.reason_code = reason_code
        self.residual = residual


def _arity(args: tuple[Any, ...], count: int) -> None:
    if len(args) != count:
        raise IntrinsicRefusal("ARITY_MISMATCH", f"expected {count} arguments, got {len(args)}")


def _traverse(container: Any, path: list[Any]) -> Any:
    current = container
    for part in path:
        if isinstance(current, dict) and isinstance(part, str) and part in current:
            current = current[part]
        elif isinstance(current, list) and type(part) is int and 0 <= part < len(current):
            current = current[part]
        else:
            raise IntrinsicRefusal("PATH_NOT_FOUND", f"path segment {part!r} is unavailable")
    return current


def core_get(args: tuple[Any, ...]) -> Any:
    _arity(args, 2)
    container, path = args
    if not isinstance(path, list):
        raise IntrinsicRefusal("INVALID_PATH", "path must be a list")
    return _traverse(container, path)


def core_same(args: tuple[Any, ...]) -> bool:
    _arity(args, 2)
    try:
        return canonical_json_bytes(args[0]) == canonical_json_bytes(args[1])
    except (TypeError, ValueError) as exc:
        raise IntrinsicRefusal("NON_CANONICAL_VALUE", str(exc)) from exc


def _number(value: ScalarValue) -> int | Fraction | float:
    if value.kind == "opaque":
        raise IntrinsicRefusal("INCOMPATIBLE_VALUE", "opaque values are not numeric")
    assert isinstance(value.value, (int, Fraction, float))
    return value.value


def _numeric_result(value: int | Fraction | float) -> dict[str, Any]:
    if isinstance(value, float):
        return encode_value(ScalarValue("float", value))
    if isinstance(value, Fraction):
        return encode_value(ScalarValue("rational", value))
    return encode_value(ScalarValue("integer", value))


def core_add(args: tuple[Any, ...]) -> dict[str, Any]:
    _arity(args, 2)
    try:
        left = decode_value(args[0])
        right = decode_value(args[1])
    except ValueDecodeError as exc:
        raise IntrinsicRefusal("INVALID_VALUE", str(exc)) from exc
    return _numeric_result(_number(left) + _number(right))


def core_sub(args: tuple[Any, ...]) -> dict[str, Any]:
    _arity(args, 2)
    try:
        left = decode_value(args[0])
        right = decode_value(args[1])
    except ValueDecodeError as exc:
        raise IntrinsicRefusal("INVALID_VALUE", str(exc)) from exc
    return _numeric_result(_number(left) - _number(right))


def core_length(args: tuple[Any, ...]) -> int:
    _arity(args, 1)
    value = args[0]
    if not isinstance(value, (list, dict, str)):
        raise IntrinsicRefusal("INVALID_SEQUENCE", "length accepts list, object, or string")
    return len(value)


def core_gt(args: tuple[Any, ...]) -> bool:
    _arity(args, 2)
    left, right = args
    if isinstance(left, bool) or isinstance(right, bool) or not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
        raise IntrinsicRefusal("INVALID_NUMBER", "gt accepts plain numeric scalars")
    return left > right


def core_select_first(args: tuple[Any, ...]) -> Any:
    _arity(args, 1)
    value = args[0]
    if not isinstance(value, list):
        raise IntrinsicRefusal("INVALID_SEQUENCE", "select_first accepts a list")
    if not value:
        raise IntrinsicRefusal("EMPTY_SEQUENCE", "cannot select from an empty list")
    return value[0]


def trace_compare_ordered(args: tuple[Any, ...]) -> dict[str, Any]:
    _arity(args, 3)
    order, left, right = args
    if not isinstance(order, list) or not order or any(not isinstance(x, str) or not x for x in order) or len(set(order)) != len(order):
        raise IntrinsicRefusal("INVALID_BOUNDARY_ORDER", "boundary_order must be a non-empty list of unique strings")
    if not isinstance(left, dict) or not isinstance(right, dict):
        raise IntrinsicRefusal("MALFORMED_TRACE", "left and right must be objects")
    if set(left) != set(order) or set(right) != set(order):
        raise IntrinsicRefusal("BOUNDARY_KEYS_MISMATCH", "left/right keys must exactly match boundary_order")

    comparisons: list[dict[str, Any]] = []
    differences: list[str] = []
    for boundary in order:
        try:
            comparison = compare_values(decode_value(left[boundary]), decode_value(right[boundary]))
        except ValueDecodeError as exc:
            raise IntrinsicRefusal("INVALID_VALUE", str(exc)) from exc
        comparisons.append({"boundary": boundary, **comparison})
        if comparison["relation"] == "DIFFERENT":
            differences.append(boundary)
    return {"comparisons": comparisons, "differences": differences}


def set_difference(args: tuple[Any, ...]) -> list[Any]:
    _arity(args, 2)
    left, right = args
    if not isinstance(left, list) or not isinstance(right, list):
        raise IntrinsicRefusal("INVALID_SET", "set.difference accepts two lists")
    right_keys = {canonical_json_bytes(item) for item in right}
    remaining = [item for item in left if canonical_json_bytes(item) not in right_keys]
    return sorted(remaining, key=canonical_json_bytes)
