"""Bounded research kernel for successor-class preservation under a state quotient.

Research-only: enabled/executable != occurred/executed; quotient structure != evidence.
"""

from collections import defaultdict


def quotient_receipt(states, quotient, transitions):
    """Return exact enabled-label and successor-class factorization receipts.

    transitions are (source, label, target) triples. `quotient` maps every state
    to its declared quotient class. No semantics are inferred beyond those inputs.
    """
    states = tuple(states)
    by_state = defaultdict(lambda: defaultdict(set))
    for source, label, target in transitions:
        if source not in quotient or target not in quotient:
            raise ValueError("every transition endpoint must have a quotient class")
        by_state[source][label].add(quotient[target])

    classes = defaultdict(list)
    for state in states:
        if state not in quotient:
            raise ValueError("every declared state must have a quotient class")
        classes[quotient[state]].append(state)

    class_receipts = {}
    for qclass, members in sorted(classes.items()):
        enabled = {m: tuple(sorted(by_state[m])) for m in members}
        enabled_factors = len(set(enabled.values())) <= 1
        labels = sorted({label for m in members for label in by_state[m]})
        successors = {
            label: {m: tuple(sorted(by_state[m].get(label, set()))) for m in members}
            for label in labels
        }
        successor_factors = {
            label: len(set(per_member.values())) <= 1
            for label, per_member in successors.items()
        }
        class_receipts[qclass] = {
            "members": tuple(sorted(members)),
            "enabled": enabled,
            "enabled_factors": enabled_factors,
            "successor_classes": successors,
            "successor_factors": successor_factors,
            "exact_one_step_factors": enabled_factors and all(successor_factors.values()),
        }

    return {"classes": class_receipts}
