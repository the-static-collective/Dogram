"""Bounded research kernel for MAY-UNION-QUOTIENT-001.

Structural only: transitions are declared possibilities, never occurrence evidence.
"""

from collections import defaultdict


def successor_classes(transitions, quotient, state, action):
    """Return sorted quotient classes reachable by one declared action."""
    return tuple(sorted({quotient[target] for source, label, target in transitions if source == state and label == action}))


def quotient_fiber(quotient, quotient_state):
    return tuple(sorted(state for state, cls in quotient.items() if cls == quotient_state))


def may_union(transitions, quotient, quotient_state, action):
    """Existential/may successor surface: union across representatives."""
    out = set()
    for state in quotient_fiber(quotient, quotient_state):
        out.update(successor_classes(transitions, quotient, state, action))
    return tuple(sorted(out))


def must_intersection(transitions, quotient, quotient_state, action):
    """Representative-common successor surface: intersection across representatives."""
    fiber = quotient_fiber(quotient, quotient_state)
    if not fiber:
        return ()
    sets = [set(successor_classes(transitions, quotient, state, action)) for state in fiber]
    return tuple(sorted(set.intersection(*sets)))


def exact_successor_factorization(transitions, quotient, quotient_state, action):
    """Whether every representative has the same successor-class set."""
    fiber = quotient_fiber(quotient, quotient_state)
    receipts = {state: successor_classes(transitions, quotient, state, action) for state in fiber}
    return len(set(receipts.values())) <= 1, receipts


def specimen_receipt():
    """Frozen hostile control: same aggregate may surface, different representative menus."""
    quotient = {
        "left": "pending",
        "right": "pending",
        "green": "green",
        "hold": "hold",
    }
    transitions = (
        ("left", "advance", "green"),
        ("right", "advance", "hold"),
    )
    exact, per_rep = exact_successor_factorization(transitions, quotient, "pending", "advance")
    return {
        "quotient_state": "pending",
        "action": "advance",
        "enabled_labels_per_representative": {"left": ("advance",), "right": ("advance",)},
        "representative_successor_classes": per_rep,
        "may_union": may_union(transitions, quotient, "pending", "advance"),
        "must_intersection": must_intersection(transitions, quotient, "pending", "advance"),
        "exact_successor_factorization": exact,
    }
