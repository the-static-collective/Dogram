"""Bounded research kernel for BIREGULAR-INCIDENCE-COLLISION-001.

Retains exact representative×successor incidence after modal extrema and both
partite degree summaries collide. Research-only; no public Dogram operator.
"""

from collections import deque


def receipt(family):
    """Return exact finite incidence and coarse summaries for a set family."""
    rows = tuple(tuple(sorted(set(row))) for row in family)
    successors = tuple(sorted({x for row in rows for x in row}))
    common = tuple(sorted(set(rows[0]).intersection(*map(set, rows[1:])))) if rows else ()
    row_degrees = tuple(sorted(len(row) for row in rows))
    column_degrees = tuple(sorted(sum(x in row for row in rows) for x in successors))

    # Connected components of the bipartite incidence graph.
    adj = {}
    for i, row in enumerate(rows):
        r = ("r", i)
        adj.setdefault(r, set())
        for x in row:
            s = ("s", x)
            adj.setdefault(s, set())
            adj[r].add(s)
            adj[s].add(r)

    unseen = set(adj)
    component_sizes = []
    while unseen:
        start = min(unseen, key=repr)
        q = deque([start])
        unseen.remove(start)
        size = 0
        while q:
            u = q.popleft()
            size += 1
            for v in adj[u]:
                if v in unseen:
                    unseen.remove(v)
                    q.append(v)
        component_sizes.append(size)

    incidence = tuple((i, x) for i, row in enumerate(rows) for x in row)
    return {
        "may_union": successors,
        "must_intersection": common,
        "row_degree_multiset": row_degrees,
        "column_degree_multiset": column_degrees,
        "edge_count": len(incidence),
        "component_sizes": tuple(sorted(component_sizes)),
        "incidence": incidence,
    }
