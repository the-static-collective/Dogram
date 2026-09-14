"""Bounded Petri-net specimen separating incidence/reachability from step concurrency.

Research-only helper. It does not promote a Dogram public operator or attach
causal/evidentiary semantics to Petri-net structure.
"""

from collections import deque


PLACES = ("guard", "pa", "qa", "pb", "qb")
TRANSITIONS = ("a", "b")


def _zero_table():
    return {place: {transition: 0 for transition in TRANSITIONS} for place in PLACES}


def _net(shared_guard):
    pre = _zero_table()
    post = _zero_table()

    pre["pa"]["a"] = 1
    post["qa"]["a"] = 1
    pre["pb"]["b"] = 1
    post["qb"]["b"] = 1

    if shared_guard:
        for transition in TRANSITIONS:
            pre["guard"][transition] = 1
            post["guard"][transition] = 1

    return {
        "places": PLACES,
        "transitions": TRANSITIONS,
        "pre": pre,
        "post": post,
        "initial_marking": {"guard": 1, "pa": 1, "qa": 0, "pb": 1, "qb": 0},
    }


def frozen_specimen():
    initial = {"guard": 1, "pa": 1, "qa": 0, "pb": 1, "qb": 0}
    final = {"guard": 1, "pa": 0, "qa": 1, "pb": 0, "qb": 1}
    return {
        "parallel": _net(shared_guard=False),
        "mutex": _net(shared_guard=True),
        "initial_marking": initial,
        "final_marking": final,
    }


def incidence_matrix(net):
    return {
        place: {
            transition: net["post"][place][transition] - net["pre"][place][transition]
            for transition in net["transitions"]
        }
        for place in net["places"]
    }


def enabled(net, marking, transition):
    return all(
        marking[place] >= net["pre"][place][transition]
        for place in net["places"]
    )


def step_enabled(net, marking, transitions):
    transitions = tuple(transitions)
    if len(set(transitions)) != len(transitions):
        raise ValueError("step transitions must be distinct in this bounded specimen")
    return all(
        marking[place]
        >= sum(net["pre"][place][transition] for transition in transitions)
        for place in net["places"]
    )


def fire(net, marking, transition):
    if not enabled(net, marking, transition):
        raise ValueError(f"transition {transition!r} is not enabled")
    return {
        place: (
            marking[place]
            - net["pre"][place][transition]
            + net["post"][place][transition]
        )
        for place in net["places"]
    }


def fire_sequence(net, sequence):
    marking = dict(net["initial_marking"])
    for transition in sequence:
        marking = fire(net, marking, transition)
    return marking


def _marking_key(net, marking):
    return tuple(marking[place] for place in net["places"])


def reachable_labeled_edges(net):
    """Enumerate the sequential labeled reachability graph exactly."""
    initial = dict(net["initial_marking"])
    queue = deque([initial])
    seen = {_marking_key(net, initial)}
    edges = set()

    while queue:
        marking = queue.popleft()
        source = _marking_key(net, marking)
        for transition in net["transitions"]:
            if not enabled(net, marking, transition):
                continue
            target_marking = fire(net, marking, transition)
            target = _marking_key(net, target_marking)
            edges.add((source, transition, target))
            if target not in seen:
                seen.add(target)
                queue.append(target_marking)

    return tuple(sorted(edges))
