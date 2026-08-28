from __future__ import annotations
from typing import Any
from .canonical import canonical_json_bytes, sha256_json

def _base(specimen: dict[str, Any], operator: str, version: int, status: str, consumed_inputs: list[str], result: dict[str, Any], residuals: list[str], warnings: list[str]) -> dict[str, Any]:
    return {"schema":"dogram.receipt/v0","specimen_id": specimen.get("specimen_id","unknown"),"operator": operator,"operator_version": version,"input_digest": sha256_json(specimen),"status": status,"consumed_inputs": sorted(set(consumed_inputs)),"result": result,"residuals": list(residuals),"warnings": list(warnings)}

def ok_receipt(specimen, operator, version, consumed_inputs, result, residuals=None, warnings=None):
    return _base(specimen,operator,version,"OK",consumed_inputs,result,residuals or [],warnings or [])

def refusal_receipt(specimen, operator, version, status, reason_code, residuals=None, warnings=None, consumed_inputs=None):
    r=_base(specimen if isinstance(specimen,dict) else {},operator,version,status,consumed_inputs or [],{},residuals or [],warnings or [])
    r["reason_code"]=reason_code
    return r

def canonical_receipt_bytes(receipt: dict[str, Any]) -> bytes:
    return canonical_json_bytes(receipt)
