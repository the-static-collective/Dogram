from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal

ValueKind = Literal["integer", "rational", "float", "opaque"]
class ValueDecodeError(ValueError): pass

@dataclass(frozen=True)
class ScalarValue:
    kind: ValueKind
    value: int | Fraction | float | str

def decode_value(spec: dict[str, Any]) -> ScalarValue:
    if not isinstance(spec, dict): raise ValueDecodeError("value must be an object")
    kind=spec.get("kind")
    if kind=="integer" and type(spec.get("value")) is int: return ScalarValue("integer", spec["value"])
    if kind=="rational" and type(spec.get("numerator")) is int and type(spec.get("denominator")) is int:
        if spec["denominator"]==0: raise ValueDecodeError("rational denominator must be non-zero")
        return ScalarValue("rational", Fraction(spec["numerator"], spec["denominator"]))
    if kind=="float" and isinstance(spec.get("value"),(int,float)) and not isinstance(spec.get("value"),bool):
        return ScalarValue("float", float(spec["value"]))
    if kind=="opaque" and isinstance(spec.get("value"),str): return ScalarValue("opaque", spec["value"])
    raise ValueDecodeError("unsupported or malformed value kind")

def encode_value(value: ScalarValue) -> dict[str, Any]:
    if value.kind=="integer": return {"kind":"integer","value":value.value}
    if value.kind=="rational":
        assert isinstance(value.value,Fraction)
        return {"kind":"rational","numerator":value.value.numerator,"denominator":value.value.denominator}
    if value.kind=="float": return {"kind":"float","value":value.value}
    return {"kind":"opaque","value":value.value}

def _numeric(value: ScalarValue):
    if value.kind=="opaque": raise ValueDecodeError("opaque values are not numeric")
    assert isinstance(value.value,(int,Fraction,float)); return value.value

def _encode_numeric_result(value):
    if isinstance(value,float): return {"kind":"float","value":value}
    if isinstance(value,Fraction):
        if value.denominator==1: return {"kind":"integer","value":value.numerator}
        return {"kind":"rational","numerator":value.numerator,"denominator":value.denominator}
    return {"kind":"integer","value":value}

def compare_values(left: ScalarValue, right: ScalarValue) -> dict[str, Any]:
    if left.kind=="opaque" or right.kind=="opaque":
        if left.kind!=right.kind: raise ValueDecodeError("opaque and numeric values are incompatible")
        return {"relation":"SAME" if left.value==right.value else "DIFFERENT"}
    delta=_numeric(right)-_numeric(left)
    out={"relation":"SAME" if delta==0 else "DIFFERENT"}
    if delta!=0: out["delta"]=_encode_numeric_result(delta)
    return out
