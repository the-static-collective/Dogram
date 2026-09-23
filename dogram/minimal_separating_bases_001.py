"""MINIMAL-SEPARATING-BASES-001.

Finite research kernel only.  A probe family separates a supplied finite state
set when its joint signatures are injective.  This module exhaustively reports
separating subsets and distinguishes inclusion-minimal from minimum-cardinality
families.  It assigns no evidentiary, causal, semantic, or execution authority.
"""

from itertools import combinations


def _signature(state, probes, family):
    return tuple(probes[name][state] for name in family)


def separates(states, probes, family):
    signatures = [_signature(s, probes, family) for s in states]
    return len(set(signatures)) == len(states)


def analyze_minimal_bases(states, probes):
    """Exhaustively analyze all subsets of a finite declared probe dictionary."""
    states = tuple(states)
    names = tuple(sorted(probes))
    if len(set(states)) != len(states):
        raise ValueError("states must be distinct")
    for name in names:
        if set(probes[name]) != set(states):
            raise ValueError(f"probe {name!r} must define exactly the supplied states")

    separating = []
    for r in range(len(names) + 1):
        for family in combinations(names, r):
            if separates(states, probes, family):
                separating.append(family)

    separating_set = set(separating)
    inclusion_minimal = []
    for family in separating:
        if not any(
            tuple(x for x in family if x != removed) in separating_set
            for removed in family
        ):
            inclusion_minimal.append(family)

    minimum_size = min((len(f) for f in separating), default=None)
    minimum = [f for f in separating if len(f) == minimum_size] if minimum_size is not None else []

    indispensable = {
        family: tuple(
            name for name in family
            if not separates(states, probes, tuple(x for x in family if x != name))
        )
        for family in inclusion_minimal
    }

    return {
        "states": states,
        "probe_names": names,
        "separating_families": tuple(separating),
        "inclusion_minimal_families": tuple(inclusion_minimal),
        "minimum_cardinality": minimum_size,
        "minimum_families": tuple(minimum),
        "indispensable_within_minimal_family": indispensable,
        "authority": "none",
    }
