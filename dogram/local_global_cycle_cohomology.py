"""Bounded local-to-global consistency receipt on an oriented 3-cycle over GF(2).

Research-only helper. This module does not promote a public Dogram operator.
"""

from itertools import product


EDGES = ((0, 1), (1, 2), (2, 0))


def _validate_edge_bits(edge_bits):
    bits = tuple(edge_bits)
    if len(bits) != 3 or any(bit not in (0, 1) for bit in bits):
        raise ValueError("edge_bits must contain exactly three GF(2) bits")
    return bits


def _satisfies(assignment, bits):
    return all(
        (assignment[target] - assignment[source]) % 2 == bit
        for (source, target), bit in zip(EDGES, bits, strict=True)
    )


def analyze_cycle_constraints(edge_bits):
    """Return an exact finite receipt for parity constraints on C3 over GF(2).

    The oriented edge cochain ``bits`` is a coboundary of a vertex assignment
    exactly when its parity around the cycle is zero.  ``cohomology_class`` is
    the resulting single GF(2) class coordinate for H^1(C3; GF(2)).
    """

    bits = _validate_edge_bits(edge_bits)
    global_solutions = [
        list(assignment)
        for assignment in product((0, 1), repeat=3)
        if _satisfies(assignment, bits)
    ]
    cycle_parity = sum(bits) % 2

    # Any one equation x_v - x_u = b over GF(2) has two local solutions.
    local_edge_solution_counts = [2, 2, 2]

    return {
        "edge_bits": list(bits),
        "cycle_parity": cycle_parity,
        "cohomology_class": cycle_parity,
        "is_coboundary": cycle_parity == 0,
        "globally_glueable": bool(global_solutions),
        "global_solutions": global_solutions,
        "local_edge_satisfiable": [True, True, True],
        "local_edge_solution_counts": local_edge_solution_counts,
        "receipt_boundary": {
            "local_satisfiable_is_not_global": True,
            "cohomology_is_not_occurrence": True,
            "cohomology_is_not_causality": True,
            "global_section_is_not_truth": True,
        },
    }
