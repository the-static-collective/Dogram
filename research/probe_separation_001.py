"""PROBE-SEPARATION-001: finite declared-observable separation receipt.

Research only. Indistinguishability under a supplied probe family is relative to
that family; it is not literal state identity unless separation is established.
"""


def analyze(states, probes):
    """Return exact signatures and indistinguishable pairs for finite probes.

    states: mapping state_id -> mapping attribute -> immutable scalar
    probes: ordered iterable of attribute names to expose
    """
    names = tuple(sorted(states))
    probes = tuple(probes)
    signatures = {s: tuple(states[s][p] for p in probes) for s in names}
    collisions = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if signatures[a] == signatures[b]:
                collisions.append((a, b))
    return {
        "probes": probes,
        "signatures": signatures,
        "indistinguishable_pairs": tuple(collisions),
        "separates_states": not collisions,
        "state_count": len(names),
        "pair_count_checked": len(names) * (len(names) - 1) // 2,
    }


def specimen():
    states = {
        "x": {"parity": 0, "high_bit": 0},
        "y": {"parity": 0, "high_bit": 1},
        "z": {"parity": 1, "high_bit": 1},
    }
    coarse = analyze(states, ("parity",))
    refined = analyze(states, ("parity", "high_bit"))
    return {
        "states": states,
        "coarse": coarse,
        "refined": refined,
        "seal": "INDISTINGUISHABLE UNDER DECLARED PROBES != IDENTICAL UNLESS SEPARATION IS ESTABLISHED",
        "non_claims": (
            "probe output is not occurrence",
            "indistinguishability is not identity",
            "separation is not evidentiary truth",
            "adding a probe is not authority to interpret it",
        ),
    }
