"""Bounded research kernel for MODAL-EXTREMA-INCIDENCE-001.

This module compares finite families of representative successor sets.  It does
not interpret transitions as occurrences, evidence, causes, truth, or authority.
"""

from functools import reduce


def receipt(family):
    """Return exact family plus may-union/must-intersection summaries."""
    members = tuple(tuple(sorted(set(member))) for member in family)
    if not members:
        raise ValueError("family must contain at least one representative")
    sets = [set(member) for member in members]
    may_union = tuple(sorted(set().union(*sets)))
    must_intersection = tuple(sorted(reduce(set.intersection, sets)))
    return {
        "representative_successors": members,
        "may_union": may_union,
        "must_intersection": must_intersection,
        "member_size_multiset": tuple(sorted(len(s) for s in sets)),
    }


def compare(left, right):
    """Receipt whether modal extrema collide while incidence differs."""
    l = receipt(left)
    r = receipt(right)
    return {
        "left": l,
        "right": r,
        "same_may_union": l["may_union"] == r["may_union"],
        "same_must_intersection": l["must_intersection"] == r["must_intersection"],
        "same_exact_family": l["representative_successors"] == r["representative_successors"],
        "same_member_size_multiset": l["member_size_multiset"] == r["member_size_multiset"],
    }
