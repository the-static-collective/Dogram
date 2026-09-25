"""Bounded COLOR-REFINEMENT-FIXPOINT-001 witness."""
from collections import Counter


def cycle6():
    return {i: {(i - 1) % 6, (i + 1) % 6} for i in range(6)}


def two_triangles():
    g = {i: set() for i in range(6)}
    for tri in ((0, 1, 2), (3, 4, 5)):
        for i in tri:
            g[i].update(set(tri) - {i})
    return g


def components(g):
    unseen, out = set(g), []
    while unseen:
        stack, seen = [min(unseen)], set()
        while stack:
            v = stack.pop()
            if v in seen:
                continue
            seen.add(v)
            stack.extend(g[v] - seen)
        unseen -= seen
        out.append(tuple(sorted(seen)))
    return tuple(out)


def refine_once(g, colors):
    sig = {v: (colors[v], tuple(sorted(colors[u] for u in g[v]))) for v in g}
    palette = {s: i for i, s in enumerate(sorted(set(sig.values())))}
    return {v: palette[sig[v]] for v in g}


def stable_refinement(g):
    colors = {v: 0 for v in g}
    history = [tuple(colors[v] for v in sorted(g))]
    while True:
        nxt = refine_once(g, colors)
        history.append(tuple(nxt[v] for v in sorted(g)))
        if Counter(nxt.values()) == Counter(colors.values()):
            return nxt, tuple(history)
        colors = nxt


def receipt():
    a, b = cycle6(), two_triangles()
    ca, ha = stable_refinement(a)
    cb, hb = stable_refinement(b)
    return {
        'degree_sequence_a': tuple(sorted(len(a[v]) for v in a)),
        'degree_sequence_b': tuple(sorted(len(b[v]) for v in b)),
        'component_count_a': len(components(a)),
        'component_count_b': len(components(b)),
        'stable_histogram_a': tuple(sorted(Counter(ca.values()).items())),
        'stable_histogram_b': tuple(sorted(Counter(cb.values()).items())),
        'history_a': ha,
        'history_b': hb,
        'seal': 'SAME STABLE COLOR REFINEMENT != ISOMORPHIC',
        'authority': 'none',
    }
