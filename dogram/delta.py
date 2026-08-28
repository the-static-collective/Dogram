from __future__ import annotations
from .values import decode_value, compare_values, ValueDecodeError

class DeltaInputError(ValueError):
    def __init__(self, reason_code, residual): self.reason_code=reason_code; self.residual=residual; super().__init__(residual)

def evaluate_delta(inputs: dict):
    if not isinstance(inputs,dict): raise DeltaInputError('MALFORMED_SPECIMEN','inputs must be object')
    order=inputs.get('boundary_order'); left=inputs.get('left'); right=inputs.get('right')
    if not isinstance(order,list) or not order or any(not isinstance(x,str) or not x for x in order) or len(order)!=len(set(order)):
        raise DeltaInputError('AMBIGUOUS_BOUNDARY_ORDER','boundary_order must be unique non-empty strings')
    if not isinstance(left,dict) or not isinstance(right,dict) or set(left)!=set(order) or set(right)!=set(order):
        raise DeltaInputError('MISSING_COORDINATE','left/right keys must exactly match boundary_order')
    comparisons=[]; consumed=[]; first=None
    for b in order:
        try: comp=compare_values(decode_value(left[b]), decode_value(right[b]))
        except ValueDecodeError as e: raise DeltaInputError('TYPE_MISMATCH',str(e)) from e
        row={'boundary':b,**comp}; comparisons.append(row)
        consumed += [f'inputs.left.{b}', f'inputs.right.{b}']
        if first is None and comp['relation']=='DIFFERENT': first=b
    return {'first_difference':first,'comparisons':comparisons}, consumed
