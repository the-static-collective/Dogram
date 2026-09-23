"""ROBUST-SEPARATION-MARGIN-001: finite signature-distance receipt.

Research-only. A probe signature is a declared calculation, not occurrence,
evidence, ontology, or authority.
"""
from itertools import combinations


def analyze(states, probes):
    """Return exact binary signatures, pairwise Hamming distances, and margin."""
    names = tuple(probes)
    if len(set(states)) != len(states):
        raise ValueError("states must be distinct")
    if not names:
        raise ValueError("at least one probe required")
    signatures = {}
    for state in states:
        sig = tuple(int(bool(probes[name](state))) for name in names)
        signatures[state] = sig
    pairs = []
    for a, b in combinations(states, 2):
        d = sum(x != y for x, y in zip(signatures[a], signatures[b]))
        pairs.append((a, b, d))
    margin = min((p[2] for p in pairs), default=None)
    return {
        "probe_names": names,
        "signatures": signatures,
        "pair_distances": tuple(pairs),
        "margin": margin,
        "separating": margin is None or margin >= 1,
        "single_probe_loss_tolerant": margin is not None and margin >= 2,
    }


def deletion_receipts(states, probes):
    """Recompute separation after deleting each single declared probe."""
    out = {}
    for removed in probes:
        kept = {k: v for k, v in probes.items() if k != removed}
        out[removed] = analyze(states, kept)
    return out


def frozen_specimen():
    states = ((0, 0), (0, 1), (1, 0), (1, 1))
    probes = {
        "x": lambda s: s[0],
        "y": lambda s: s[1],
        "xor": lambda s: s[0] ^ s[1],
    }
    return analyze(states, probes), deletion_receipts(states, probes)


if __name__ == "__main__":
    full, deletions = frozen_specimen()
    print("signatures", full["signatures"])
    print("margin", full["margin"])
    print("single_probe_loss_tolerant", full["single_probe_loss_tolerant"])
    print("deletion_margins", {k: v["margin"] for k, v in deletions.items()})
