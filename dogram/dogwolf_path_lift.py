"""DOGWOLF-002: find a bounded quotient path without a concrete path lift.

Research only: declared transitions are possible edges, not actual occurrences.
The search checks quotient-class routes, not merely action-label languages.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from hashlib import sha256
import json

from .dogwolf_operation_preservation import probe_operation_preservation


@dataclass(frozen=True)
class PhantomPath:
    quotient_classes: tuple[str, ...]
    action_labels: tuple[str, ...]
    independent_edge_witnesses: tuple[tuple[str, str, str], ...]
    concrete_prefix: tuple[str, ...]
    reachable_at_join: tuple[str, ...]
    next_edge_sources: tuple[str, ...]
    join_class: str


@dataclass(frozen=True)
class PathLiftReceipt:
    input_sha256: str
    status: str  # phantom_found | no_phantom_within_bound | inconclusive
    max_depth: int
    max_paths: int
    examined_paths: int
    one_step_statuses: tuple[tuple[str, str], ...]
    one_step_input_sha256: str
    phantom: PhantomPath | None


def hunt_phantom_path(
    states: tuple[str, ...],
    quotient: tuple[str, ...],
    transitions: tuple[tuple[str, str, str], ...],
    *,
    max_depth: int = 3,
    max_paths: int = 4096,
) -> PathLiftReceipt:
    """BFS for the shortest quotient-class route without any concrete lift.

    Every quotient edge must be supported by a supplied concrete edge. A path
    is phantom when individually supported quotient edges do not compose into
    a single concrete state sequence matching all intermediate classes.
    The budget bounds candidate route expansions. An unfinished search is
    inconclusive; finite no-phantom results apply only through max_depth.
    """
    if type(states) is not tuple or not 1 <= len(states) <= 64 or any(type(s) is not str or not s for s in states) or len(set(states)) != len(states):
        raise ValueError("states must be 1..64 unique nonempty strings")
    if type(quotient) is not tuple or len(quotient) != len(states) or any(type(q) is not str or not q for q in quotient):
        raise ValueError("quotient must declare one nonempty string class per state")
    if type(transitions) is not tuple or len(transitions) > 512:
        raise ValueError("transitions must be a tuple of at most 512 edges")
    if type(max_depth) is not int or not 1 <= max_depth <= 6:
        raise ValueError("max_depth must be an integer in 1..6")
    if type(max_paths) is not int or not 0 <= max_paths <= 100000:
        raise ValueError("max_paths must be a nonnegative integer <= 100000")

    class_for = dict(zip(states, quotient))
    edges_by_class: dict[str, list[tuple[str, str, str]]] = {}
    edges_by_source: dict[str, list[tuple[str, str, str]]] = {}
    seen_edges: set[tuple[str, str, str]] = set()
    labels: set[str] = set()
    for edge in transitions:
        if type(edge) is not tuple or len(edge) != 3 or any(type(x) is not str or not x for x in edge):
            raise ValueError("each edge must be a triple of nonempty string labels")
        src, label, dst = edge
        if src not in class_for or dst not in class_for or edge in seen_edges:
            raise ValueError("every endpoint must be declared and edges must be unique")
        seen_edges.add(edge)
        labels.add(label)
        edges_by_class.setdefault(class_for[src], []).append(edge)
        edges_by_source.setdefault(src, []).append(edge)

    declared_labels = tuple(sorted(labels))
    # DOGWOLF-001: compare each action's complete one-step successor
    # quotient-class result table (the empty tuple means disabled).
    operation_tables = {
        label: tuple(
            tuple(sorted({class_for[dst] for src, act, dst in edges_by_source.get(state, ()) if act == label}))
            for state in states
        )
        for label in declared_labels
    }
    if not operation_tables:
        operation_tables = {"<no-declared-transitions>": tuple(() for _ in states)}
    old = probe_operation_preservation(states, quotient, operation_tables, max_pair_checks=2016)
    one_step = tuple((probe.operation, probe.status) for probe in old.probes)
    if any(status == "inconclusive" for _, status in one_step):
        raise AssertionError("the finite one-step check must be exhaustive")

    payload = {"schema": "dogram/dogwolf-path-lift/v0", "states": states, "quotient": quotient,
               "transitions": sorted(transitions), "max_depth": max_depth, "max_paths": max_paths}
    digest = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    class_members: dict[str, list[str]] = {}
    for state, klass in zip(states, quotient):
        class_members.setdefault(klass, []).append(state)
    # Canonical edge traversal makes witnesses independent of input edge order.
    for edge_list in edges_by_class.values():
        edge_list.sort()
    for edge_list in edges_by_source.values():
        edge_list.sort()
    transitions = tuple(sorted(transitions))

    # Each entry carries a route and a concrete witness for every reachable end.
    queue = deque(((klass,), (), {state: (state,) for state in members})
                  for klass, members in class_members.items())
    examined = 0
    while queue:
        classes, actions, frontier = queue.popleft()
        if len(actions) >= max_depth:
            continue
        klass = classes[-1]
        next_choices: dict[tuple[str, str], tuple[str, str, str]] = {}
        for edge in edges_by_class.get(klass, ()):
            src, label, dst = edge
            next_choices.setdefault((label, class_for[dst]), edge)
        for label, destination_class in sorted(next_choices):
            if examined >= max_paths:
                return PathLiftReceipt(digest, "inconclusive", max_depth, max_paths, examined,
                                       one_step, old.input_sha256, None)
            examined += 1
            next_frontier: dict[str, tuple[str, ...]] = {}
            for state, witness in frontier.items():
                for src, act, dst in edges_by_source.get(state, ()):
                    if act == label and class_for[dst] == destination_class:
                        next_frontier.setdefault(dst, witness + (dst,))
            route_classes = classes + (destination_class,)
            route_actions = actions + (label,)
            if not next_frontier:
                supporting_edges = tuple(
                    next(edge for edge in transitions
                         if class_for[edge[0]] == route_classes[i]
                         and edge[1] == route_actions[i]
                         and class_for[edge[2]] == route_classes[i + 1])
                    for i in range(len(route_actions))
                )
                outgoing_sources = tuple(sorted({src for src, act, dst in edges_by_class[klass]
                                                 if act == label and class_for[dst] == destination_class}))
                return PathLiftReceipt(
                    digest, "phantom_found", max_depth, max_paths, examined, one_step,
                    old.input_sha256,
                    PhantomPath(route_classes, route_actions, supporting_edges,
                                next(iter(frontier.values())), tuple(sorted(frontier)),
                                outgoing_sources, klass),
                )
            queue.append((route_classes, route_actions, next_frontier))
    return PathLiftReceipt(digest, "no_phantom_within_bound", max_depth, max_paths,
                           examined, one_step, old.input_sha256, None)


__all__ = ["PhantomPath", "PathLiftReceipt", "hunt_phantom_path"]
