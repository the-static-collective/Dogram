"""Finite specimen: equal one-cell equitable quotient, different realization."""
from collections import deque

def cycle6():
    return {i:{(i-1)%6,(i+1)%6} for i in range(6)}

def two_triangles():
    return {0:{1,2},1:{0,2},2:{0,1},3:{4,5},4:{3,5},5:{3,4}}

def one_cell_quotient(graph):
    degrees={len(v) for v in graph.values()}
    if len(degrees)!=1:
        raise ValueError("graph must be regular")
    return ((next(iter(degrees)),),)

def components(graph):
    unseen=set(graph); out=[]
    while unseen:
        q=[unseen.pop()]; seen=set(q)
        while q:
            u=q.pop()
            for v in graph[u]:
                if v in unseen:
                    unseen.remove(v); seen.add(v); q.append(v)
        out.append(tuple(sorted(seen)))
    return tuple(out)

def receipt():
    a,b=cycle6(),two_triangles()
    return {"same_quotient":one_cell_quotient(a)==one_cell_quotient(b),
            "a_components":components(a),"b_components":components(b)}
