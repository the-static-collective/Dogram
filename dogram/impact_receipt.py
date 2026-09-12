from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import sha256_json
from .graph import DirectedGraph, GraphInputError


@dataclass
class ImpactReceiptInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


def _path_or_none(graph: DirectedGraph, source: str, target: str) -> list[str] | None:
    if source not in graph.nodes or target not in graph.nodes:
        return None
    return graph.shortest_path(source, target)


def evaluate_impact_receipt(inputs: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    if not isinstance(inputs, dict):
        raise ImpactReceiptInputError("MALFORMED_INPUTS", "inputs must be an object")

    try:
        before = DirectedGraph.from_spec(inputs.get("baseline"))
        after = DirectedGraph.from_spec(inputs.get("candidate"))
    except GraphInputError as exc:
        raise ImpactReceiptInputError("INVALID_GRAPH", str(exc)) from exc

    queries = inputs.get("queries", [])
    if not isinstance(queries, list):
        raise ImpactReceiptInputError("INVALID_QUERIES", "queries must be a list")

    all_nodes = set(before.nodes) | set(after.nodes)
    query_reports: list[dict[str, Any]] = []
    for query in queries:
        if (
            not isinstance(query, list)
            or len(query) != 2
            or not all(isinstance(item, str) and item for item in query)
        ):
            raise ImpactReceiptInputError(
                "INVALID_QUERIES", "each query must be a [source,target] string pair"
            )
        source, target = query
        if source not in all_nodes or target not in all_nodes:
            raise ImpactReceiptInputError(
                "INVALID_QUERY_REFERENCE",
                "query nodes must exist in at least one compared graph",
            )

        path_before = _path_or_none(before, source, target)
        path_after = _path_or_none(after, source, target)
        query_reports.append(
            {
                "source": source,
                "target": target,
                "reachable_before": path_before is not None,
                "reachable_after": path_after is not None,
                "path_before": path_before,
                "path_after": path_after,
                "changed": path_before != path_after,
            }
        )

    before_nodes = set(before.nodes)
    after_nodes = set(after.nodes)
    before_edges = set(before.edges)
    after_edges = set(after.edges)
    before_pairs = {tuple(pair) for pair in before.reachable_pairs()}
    after_pairs = {tuple(pair) for pair in after.reachable_pairs()}

    result = {
        "graph_before_digest": sha256_json(before.to_spec()),
        "graph_after_digest": sha256_json(after.to_spec()),
        "node_delta": {
            "added": sorted(after_nodes - before_nodes),
            "removed": sorted(before_nodes - after_nodes),
        },
        "edge_delta": {
            "added": [list(edge) for edge in sorted(after_edges - before_edges)],
            "removed": [list(edge) for edge in sorted(before_edges - after_edges)],
        },
        "reachability_delta": {
            "gained": [list(pair) for pair in sorted(after_pairs - before_pairs)],
            "lost": [list(pair) for pair in sorted(before_pairs - after_pairs)],
        },
        "queries": query_reports,
    }

    consumed = ["inputs.baseline", "inputs.candidate"]
    if "queries" in inputs:
        consumed.append("inputs.queries")
    return result, consumed
