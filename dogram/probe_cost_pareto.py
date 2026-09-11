from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from numbers import Real
from typing import Hashable, Mapping


ProbeValue = Hashable


@dataclass(frozen=True)
class ProbeCostParetoReceipt:
    states: tuple[str, ...]
    target_pair: tuple[str, str]
    costs: dict[str, float]
    separating_probes: tuple[str, ...]
    information_minimal_separators: tuple[str, ...]
    cost_minimal_separators: tuple[str, ...]
    pareto_separators: tuple[str, ...]
    dominance_edges: tuple[tuple[str, str], ...]


def _require_hashable(value: ProbeValue) -> None:
    try:
        hash(value)
    except TypeError as exc:
        raise ValueError("probe outputs must be hashable") from exc


def factorization_map(
    stronger_outputs: tuple[ProbeValue, ...],
    weaker_outputs: tuple[ProbeValue, ...],
) -> tuple[tuple[ProbeValue, ProbeValue], ...] | None:
    """Return a finite witness that weaker factors through stronger, if one exists."""

    if len(stronger_outputs) != len(weaker_outputs):
        raise ValueError("probe output tuples must have equal length")

    witness: dict[ProbeValue, ProbeValue] = {}
    for stronger, weaker in zip(stronger_outputs, weaker_outputs):
        _require_hashable(stronger)
        _require_hashable(weaker)
        if stronger in witness and witness[stronger] != weaker:
            return None
        witness[stronger] = weaker
    return tuple(sorted(witness.items(), key=lambda item: repr(item[0])))


def probe_refines(
    stronger_outputs: tuple[ProbeValue, ...],
    weaker_outputs: tuple[ProbeValue, ...],
) -> bool:
    return factorization_map(stronger_outputs, weaker_outputs) is not None


def dominates(
    candidate_outputs: tuple[ProbeValue, ...],
    candidate_cost: Real,
    other_outputs: tuple[ProbeValue, ...],
    other_cost: Real,
) -> bool:
    """Return exact information-cost Pareto dominance for two declared probes.

    Candidate dominates other only if it is at least as informative by deterministic
    factorization and no more costly, with at least one strict improvement. Cost is
    an independently declared coordinate; refinement never manufactures a cost.
    """

    for cost in (candidate_cost, other_cost):
        if not isinstance(cost, Real) or isinstance(cost, bool) or not isfinite(float(cost)) or cost < 0:
            raise ValueError("costs must be finite nonnegative real numbers")

    if not probe_refines(candidate_outputs, other_outputs):
        return False

    same_information = probe_refines(other_outputs, candidate_outputs)
    cheaper = candidate_cost < other_cost
    strictly_more_informative = not same_information
    return candidate_cost <= other_cost and (cheaper or strictly_more_informative)


def analyze_probe_costs(
    states: tuple[str, ...],
    probes: Mapping[str, tuple[ProbeValue, ...]],
    costs: Mapping[str, Real],
    target_pair: tuple[str, str],
) -> ProbeCostParetoReceipt:
    """Analyze separating probes under independent information and cost orders."""

    if not states or len(set(states)) != len(states):
        raise ValueError("states must be nonempty and unique")
    if len(target_pair) != 2 or target_pair[0] == target_pair[1]:
        raise ValueError("target_pair must contain two distinct states")
    if any(state not in states for state in target_pair):
        raise ValueError("target_pair states must belong to states")
    if not probes:
        raise ValueError("at least one probe is required")
    if set(costs) != set(probes):
        raise ValueError("costs must be declared for exactly the supplied probes")

    probe_items = tuple(probes.items())
    normalized_costs: dict[str, float] = {}
    for name, outputs in probe_items:
        if not isinstance(name, str) or not name:
            raise ValueError("probe names must be nonempty strings")
        if len(outputs) != len(states):
            raise ValueError("each probe must provide one output per state")
        for output in outputs:
            _require_hashable(output)

        cost = costs[name]
        if not isinstance(cost, Real) or isinstance(cost, bool) or not isfinite(float(cost)) or cost < 0:
            raise ValueError("costs must be finite nonnegative real numbers")
        normalized_costs[name] = float(cost)

    strict_refinements: set[tuple[str, str]] = set()
    for stronger_name, stronger_outputs in probe_items:
        for weaker_name, weaker_outputs in probe_items:
            if stronger_name == weaker_name:
                continue
            if probe_refines(stronger_outputs, weaker_outputs) and not probe_refines(
                weaker_outputs, stronger_outputs
            ):
                strict_refinements.add((stronger_name, weaker_name))

    state_index = {state: index for index, state in enumerate(states)}
    left_index = state_index[target_pair[0]]
    right_index = state_index[target_pair[1]]
    separating_probes = tuple(
        name
        for name, outputs in probe_items
        if outputs[left_index] != outputs[right_index]
    )

    information_minimal = tuple(
        name
        for name in separating_probes
        if not any(
            other != name
            and other in separating_probes
            and (name, other) in strict_refinements
            for other in separating_probes
        )
    )

    if separating_probes:
        minimum_cost = min(normalized_costs[name] for name in separating_probes)
        cost_minimal = tuple(
            name for name in separating_probes if normalized_costs[name] == minimum_cost
        )
    else:
        cost_minimal = ()

    dominance_edges: list[tuple[str, str]] = []
    for candidate in separating_probes:
        for other in separating_probes:
            if candidate == other:
                continue
            if dominates(
                probes[candidate], normalized_costs[candidate],
                probes[other], normalized_costs[other],
            ):
                dominance_edges.append((candidate, other))

    pareto = tuple(
        name
        for name in separating_probes
        if not any(other == name for _, other in dominance_edges)
    )

    return ProbeCostParetoReceipt(
        states=states,
        target_pair=target_pair,
        costs=normalized_costs,
        separating_probes=separating_probes,
        information_minimal_separators=information_minimal,
        cost_minimal_separators=cost_minimal,
        pareto_separators=pareto,
        dominance_edges=tuple(dominance_edges),
    )


__all__ = [
    "ProbeCostParetoReceipt",
    "analyze_probe_costs",
    "dominates",
    "factorization_map",
    "probe_refines",
]
