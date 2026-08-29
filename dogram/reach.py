from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import sha256_json
from .graph import DirectedGraph, GraphInputError


@dataclass
class ReachInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


def _apply_mutation(graph: DirectedGraph, mutation: dict[str, Any]) -> DirectedGraph:
    if not isinstance(mutation, dict) or not isinstance(mutation.get("op"), str):
        raise ReachInputError("UNSUPPORTED_MUTATION", "mutation must name an operation")
    op = mutation["op"]
    try:
        if op == "ADD_NODE" and isinstance(mutation.get("node"), str):
            return graph.add_node(mutation["node"])
        if op == "REMOVE_NODE" and isinstance(mutation.get("node"), str):
            return graph.remove_node(mutation["node"])
        if op == "ADD_EDGE" and isinstance(mutation.get("source"), str) and isinstance(mutation.get("target"), str):
            return graph.add_edge(mutation["source"], mutation["target"])
        if op == "REMOVE_EDGE" and isinstance(mutation.get("source"), str) and isinstance(mutation.get("target"), str):
            return graph.remove_edge(mutation["source"], mutation["target"])
    except GraphInputError as exc:
        raise ReachInputError("INVALID_GRAPH_REFERENCE", str(exc)) from exc
    if op not in {"ADD_NODE", "REMOVE_NODE", "ADD_EDGE", "REMOVE_EDGE"}:
        raise ReachInputError("UNSUPPORTED_MUTATION", f"unsupported mutation {op}")
    raise ReachInputError("INVALID_GRAPH_REFERENCE", "mutation references are malformed")


def evaluate_reach(inputs: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    if not isinstance(inputs, dict):
        raise ReachInputError("MALFORMED_INPUTS", "inputs must be an object")
    try:
        before = DirectedGraph.from_spec(inputs.get("graph"))
    except GraphInputError as exc:
        raise ReachInputError("INVALID_GRAPH", str(exc)) from exc
    after = _apply_mutation(before, inputs.get("mutation"))
    queries = inputs.get("queries")
    if not isinstance(queries, list):
        raise ReachInputError("INVALID_GRAPH_REFERENCE", "queries must be a list")

    reports: list[dict[str, Any]] = []
    for query in queries:
        if not isinstance(query, list) or len(query) != 2 or not all(isinstance(x, str) for x in query):
            raise ReachInputError("INVALID_GRAPH_REFERENCE", "query must be [source,target]")
        source, target = query
        if source not in before.nodes or target not in before.nodes:
            raise ReachInputError("INVALID_GRAPH_REFERENCE", "query nodes must exist before mutation")
        path_before = before.shortest_path(source, target)
        path_after = after.shortest_path(source, target) if source in after.nodes and target in after.nodes else None
        reachable_before = path_before is not None
        reachable_after = path_after is not None
        reports.append({
            "source": source,
            "target": target,
            "reachable_before": reachable_before,
            "reachable_after": reachable_after,
            "changed": reachable_before != reachable_after,
            "path_before": path_before,
            "path_after": path_after,
        })

    result = {
        "graph_before_digest": sha256_json(before.to_spec()),
        "graph_after_digest": sha256_json(after.to_spec()),
        "mutation": inputs["mutation"],
        "queries": reports,
    }
    return result, ["inputs.graph", "inputs.mutation", "inputs.queries"]
