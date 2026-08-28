from __future__ import annotations
from .graph import DirectedGraph, GraphInputError
from .canonical import sha256_json
class AblateInputError(ValueError):
    def __init__(self,reason_code,residual): self.reason_code=reason_code; self.residual=residual; super().__init__(residual)

def evaluate_ablate(inputs):
    try: g=DirectedGraph.from_spec(inputs.get('graph') if isinstance(inputs,dict) else None)
    except GraphInputError as e: raise AblateInputError(e.reason_code,e.residual) from e
    target=inputs.get('target'); queries=inputs.get('queries',[])
    try:
        if not isinstance(target,dict): raise AblateInputError('MISSING_ABLATION_TARGET','target missing')
        if target.get('kind')=='node':
            node=target.get('node')
            if node not in g.nodes: raise AblateInputError('MISSING_ABLATION_TARGET','node not present')
            g2=g.remove_node(node); removed={'kind':'node','node':node}
        elif target.get('kind')=='edge':
            edge=(target.get('source'),target.get('target'))
            if edge not in g.edges: raise AblateInputError('MISSING_ABLATION_TARGET','edge not present')
            g2=g.remove_edge(*edge); removed={'kind':'edge','source':edge[0],'target':edge[1]}
        else: raise AblateInputError('MISSING_ABLATION_TARGET','unsupported target')
    except GraphInputError as e: raise AblateInputError(e.reason_code,e.residual) from e
    before={tuple(x) for x in g.reachable_pairs()}; after={tuple(x) for x in g2.reachable_pairs()}
    req=[]
    for q in queries:
        if not isinstance(q,list) or len(q)!=2: raise AblateInputError('INVALID_GRAPH_REFERENCE','query malformed')
        try: rb=g.reachable(q[0],q[1]); ra=(q[0] in g2.nodes and q[1] in g2.nodes and g2.reachable(q[0],q[1]))
        except GraphInputError as e: raise AblateInputError(e.reason_code,e.residual) from e
        req.append({'source':q[0],'target':q[1],'reachable_before':rb,'reachable_after':ra,'changed':rb!=ra})
    return {'removed_component':removed,'graph_before_digest':sha256_json(g.to_spec()),'graph_after_digest':sha256_json(g2.to_spec()),'lost_reachability':[list(x) for x in sorted(before-after)],'gained_reachability':[list(x) for x in sorted(after-before)],'requested_targets':req}, ['inputs.graph','inputs.target','inputs.queries']
