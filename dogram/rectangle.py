from __future__ import annotations
from fractions import Fraction
from .values import decode_value, ValueDecodeError

class RectangleInputError(ValueError):
    def __init__(self, reason_code, residual): self.reason_code=reason_code; self.residual=residual; super().__init__(residual)

def _enc(v):
    if isinstance(v,float): return {'kind':'float','value':v}
    if isinstance(v,Fraction):
        if v.denominator==1: return {'kind':'integer','value':v.numerator}
        return {'kind':'rational','numerator':v.numerator,'denominator':v.denominator}
    return {'kind':'integer','value':v}

def evaluate_rectangle(inputs: dict):
    if not isinstance(inputs,dict): raise RectangleInputError('MALFORMED_SPECIMEN','inputs must be object')
    a=inputs.get('axis_a'); b=inputs.get('axis_b'); cells=inputs.get('cells')
    if not isinstance(a,str) or not a or not isinstance(b,str) or not b or not isinstance(cells,dict) or set(cells)!={'00','01','10','11'}:
        raise RectangleInputError('MISSING_COORDINATE','rectangle requires axes and cells 00,01,10,11')
    try: vals={k:decode_value(v) for k,v in cells.items()}
    except ValueDecodeError as e: raise RectangleInputError('TYPE_MISMATCH',str(e)) from e
    kinds={v.kind for v in vals.values()}; consumed=[f'inputs.cells.{k}' for k in ('00','01','10','11')]+['inputs.axis_a','inputs.axis_b']
    if kinds=={'opaque'}:
        e0=vals['00'].value==vals['10'].value; e1=vals['01'].value==vals['11'].value
        return {'mode':'equivalence','axis_a':a,'axis_b':b,'equivalent_across_axis_a_when_b0':e0,'equivalent_across_axis_a_when_b1':e1,'interaction_detected':e0!=e1}, consumed
    if 'opaque' in kinds: raise RectangleInputError('TYPE_MISMATCH','numeric and opaque cells cannot mix')
    any_float='float' in kinds
    def num(v): return float(v.value) if any_float else Fraction(v.value)
    mixed=num(vals['11'])-num(vals['10'])-num(vals['01'])+num(vals['00'])
    return {'mode':'numeric','axis_a':a,'axis_b':b,'mixed_delta':_enc(mixed),'interaction_detected':mixed!=0}, consumed
