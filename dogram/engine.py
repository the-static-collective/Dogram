from __future__ import annotations
from .delta import evaluate_delta, DeltaInputError
from .rectangle import evaluate_rectangle, RectangleInputError
from .ablate import evaluate_ablate, AblateInputError
from .reach import evaluate_reach, ReachInputError
from .receipt import ok_receipt, refusal_receipt

OPERATORS={('delta',1):evaluate_delta,('rectangle',1):evaluate_rectangle,('ablate',1):evaluate_ablate,('reach',1):evaluate_reach}
ERRORS=(DeltaInputError,RectangleInputError,AblateInputError,ReachInputError)
REQUIRED={'schema','specimen_id','operator','operator_version','inputs','assumptions','metadata'}

def evaluate_specimen(specimen):
    op = specimen.get('operator','unknown') if isinstance(specimen,dict) else 'unknown'
    ver = specimen.get('operator_version',0) if isinstance(specimen,dict) else 0
    if not isinstance(specimen,dict) or set(specimen)!=REQUIRED or specimen.get('schema')!='dogram.specimen/v0' or not isinstance(specimen.get('specimen_id'),str) or not specimen.get('specimen_id') or not isinstance(specimen.get('inputs'),dict) or not isinstance(specimen.get('assumptions'),list) or not isinstance(specimen.get('metadata'),dict):
        return refusal_receipt(specimen if isinstance(specimen,dict) else {}, str(op), ver if isinstance(ver,int) else 0, 'REFUSE','MALFORMED_SPECIMEN',['invalid top-level specimen envelope'])
    if not isinstance(op,str) or op not in {k[0] for k in OPERATORS}:
        return refusal_receipt(specimen,str(op),ver if isinstance(ver,int) else 0,'REFUSE','UNSUPPORTED_OPERATOR',['operator not in v0 floor'])
    if (op,ver) not in OPERATORS:
        return refusal_receipt(specimen,op,ver if isinstance(ver,int) else 0,'REFUSE','UNSUPPORTED_OPERATOR_VERSION',['operator version not supported'])
    try:
        result,consumed=OPERATORS[(op,ver)](specimen['inputs'])
        return ok_receipt(specimen,op,ver,consumed,result)
    except ERRORS as e:
        return refusal_receipt(specimen,op,ver,'INSUFFICIENT_TO_TEST',e.reason_code,[e.residual])
