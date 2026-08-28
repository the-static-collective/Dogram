from __future__ import annotations
from dataclasses import dataclass
from collections import deque

class GraphInputError(ValueError):
    def __init__(self, reason_code, residual): self.reason_code=reason_code; self.residual=residual; super().__init__(residual)

@dataclass(frozen=True)
class DirectedGraph:
    nodes: tuple[str,...]
    edges: tuple[tuple[str,str],...]
    @classmethod
    def from_spec(cls,spec):
        if not isinstance(spec,dict) or not isinstance(spec.get('nodes'),list) or not isinstance(spec.get('edges'),list): raise GraphInputError('MALFORMED_SPECIMEN','graph requires nodes and edges')
        nodes=spec['nodes']
        if any(not isinstance(n,str) or not n for n in nodes) or len(nodes)!=len(set(nodes)): raise GraphInputError('INVALID_GRAPH_REFERENCE','nodes must be unique strings')
        es=[]
        for e in spec['edges']:
            if not isinstance(e,list) or len(e)!=2 or any(not isinstance(x,str) for x in e): raise GraphInputError('INVALID_GRAPH_REFERENCE','edge must be [source,target]')
            es.append((e[0],e[1]))
        if len(es)!=len(set(es)): raise GraphInputError('INVALID_GRAPH_REFERENCE','duplicate edge')
        ns=set(nodes)
        if any(s not in ns or t not in ns for s,t in es): raise GraphInputError('INVALID_GRAPH_REFERENCE','edge endpoint missing')
        return cls(tuple(sorted(nodes)),tuple(sorted(es)))
    def to_spec(self): return {'nodes':list(self.nodes),'edges':[list(e) for e in self.edges]}
    def _neighbors(self,n): return sorted(t for s,t in self.edges if s==n)
    def shortest_path(self,source,target):
        if source not in self.nodes or target not in self.nodes: raise GraphInputError('INVALID_GRAPH_REFERENCE','query node missing')
        q=deque([(source,[source])]); seen={source}
        while q:
            n,p=q.popleft()
            if n==target: return p
            for nxt in self._neighbors(n):
                if nxt not in seen: seen.add(nxt); q.append((nxt,p+[nxt]))
        return None
    def reachable(self,source,target): return self.shortest_path(source,target) is not None
    def reachable_pairs(self): return [[a,b] for a in self.nodes for b in self.nodes if a!=b and self.reachable(a,b)]
    def remove_node(self,node):
        if node not in self.nodes: raise GraphInputError('INVALID_GRAPH_REFERENCE','node missing')
        return DirectedGraph(tuple(n for n in self.nodes if n!=node),tuple(e for e in self.edges if node not in e))
    def remove_edge(self,source,target):
        if (source,target) not in self.edges: raise GraphInputError('INVALID_GRAPH_REFERENCE','edge missing')
        return DirectedGraph(self.nodes,tuple(e for e in self.edges if e!=(source,target)))
    def add_node(self,node):
        if not isinstance(node,str) or not node or node in self.nodes: raise GraphInputError('INVALID_GRAPH_REFERENCE','invalid/new node required')
        return DirectedGraph(tuple(sorted(self.nodes+(node,))),self.edges)
    def add_edge(self,source,target):
        if source not in self.nodes or target not in self.nodes or (source,target) in self.edges: raise GraphInputError('INVALID_GRAPH_REFERENCE','invalid/new edge required')
        return DirectedGraph(self.nodes,tuple(sorted(self.edges+((source,target),))))
