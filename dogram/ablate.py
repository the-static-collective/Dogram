from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import sha256_json
from .graph import DirectedGraph, GraphInputError


@dataclass
class AblateInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


def _reachable_or_false(graph: DirectedGraph, source: str, target: str) -> bool:
    if source not in graph.nodes or target not in graph.nodes:
        return False
    return graph.reachable(source, target)


def evaluate_ablate(inputs: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    if not isinstance(inputs, dict):
        raise AblateInputError("MALFORMED_INPUTS", "inputs must be an object")
    try:
        before = DirectedGraph.from_spec(inputs.get("graph"))
    except GraphInputError as exc:
        raise AblateInputError("INVALID_GRAPH", str(exc)) from exc
    target = inputs.get("target")
    if not isinstance(target, dict):
        raise AblateInputError("MISSING_ABLATION_TARGET", "target must be an object")
    kind = target.get("kind")
    try:
        if kind == "node" and isinstance(target.get("node"), str):
            node = target["node"]
            if node not in before.nodes:
                raise AblateInputError("MISSING_ABLATION_TARGET", "node target does not exist")
            after = before.remove_node(node)
            removed = {"kind": "node", "node": node}
        elif kind == "edge" and isinstance(target.get("source"), str) and isinstance(target.get("target"), str):
            source = target["source"]
            destination = target["target"]
            if (source, destination) not in before.edges:
                raise AblateInputError("MISSING_ABLATION_TARGET", "edge target does not exist")
            after = before.remove_edge(source, destination)
            removed = {"kind": "edge", "source": source, "target": destination}
        else:
            raise AblateInputError("MISSING_ABLATION_TARGET", "unsupported ablation target")
    except GraphInputError as exc:
        raise AblateInputError("MISSING_ABLATION_TARGET", str(exc)) from exc

    before_pairs = {tuple(pair) for pair in before.reachable_pairs()}
    after_pairs = {tuple(pair) for pair in after.reachable_pairs()}
    lost = [list(pair) for pair in sorted(before_pairs - after_pairs)]
    gained = [list(pair) for pair in sorted(after_pairs - before_pairs)]

    requested = inputs.get("requested_targets", [])
    if not isinstance(requested, list):
        raise AblateInputError("INVALID_REQUESTED_TARGETS", "requested_targets must be a list")
    reports: list[dict[str, Any]] = []
    for query in requested:
        if not isinstance(query, list) or len(query) != 2 or not all(isinstance(x, str) for x in query):
            raise AblateInputError("INVALID_REQUESTED_TARGETS", "each requested target must be [source,target]")
        source, destination = query
        reports.append({"source": source, "target": destination, "reachable_before": _reachable_or_false(before, source, destination), "reachable_after": _reachable_or_false(after, source, destination)})

    result = {
        "removed_component": removed,
        "graph_before_digest": sha256_json(before.to_spec()),
        "graph_after_digest": sha256_json(after.to_spec()),
        "lost_reachability": lost,
        "gained_reachability": gained,
        "requested_targets": reports,
    }
    consumed = ["inputs.graph", "inputs.target"]
    if "requested_targets" in inputs:
        consumed.append("inputs.requested_targets")
    return result, consumed
