from __future__ import annotations
from .graph import DirectedGraph, GraphInputError
from .canonical import sha256_json
class ReachInputError(ValueError):
    def __init__(self,reason_code,residual): self.reason_code=reason_code; self.residual=residual; super().__init__(residual)

def _mutate(g,m):
    if not isinstance(m,dict): raise ReachInputError('UNSUPPORTED_MUTATION','mutation missing')
    op=m.get('op')
    try:
        if op=='ADD_NODE': return g.add_node(m.get('node'))
        if op=='REMOVE_NODE': return g.remove_node(m.get('node'))
        if op=='ADD_EDGE': return g.add_edge(m.get('source'),m.get('target'))
        if op=='REMOVE_EDGE': return g.remove_edge(m.get('source'),m.get('target'))
    except GraphInputError as e: raise ReachInputError(e.reason_code,e.residual) from e
    raise ReachInputError('UNSUPPORTED_MUTATION','unknown mutation operation')

def evaluate_reach(inputs):
    try: g=DirectedGraph.from_spec(inputs.get('graph') if isinstance(inputs,dict) else None)
    except GraphInputError as e: raise ReachInputError(e.reason_code,e.residual) from e
    g2=_mutate(g,inputs.get('mutation')); out=[]
    for q in inputs.get('queries',[]):
        if not isinstance(q,list) or len(q)!=2: raise ReachInputError('INVALID_GRAPH_REFERENCE','query malformed')
        s,t=q
        if s not in g.nodes or t not in g.nodes or s not in g2.nodes or t not in g2.nodes: raise ReachInputError('INVALID_GRAPH_REFERENCE','query node missing before/after')
        pb=g.shortest_path(s,t); pa=g2.shortest_path(s,t)
        out.append({'source':s,'target':t,'reachable_before':pb is not None,'reachable_after':pa is not None,'changed':(pb is None)!=(pa is None),'path_before':pb,'path_after':pa})
    return {'graph_before_digest':sha256_json(g.to_spec()),'graph_after_digest':sha256_json(g2.to_spec()),'mutation':inputs.get('mutation'),'queries':out}, ['inputs.graph','inputs.mutation','inputs.queries']
