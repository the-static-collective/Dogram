from __future__ import annotations

from typing import Any

from ..graph import DirectedGraph, GraphInputError
from .core import IntrinsicRefusal, _arity


def graph_apply_mutation(args: tuple[Any, ...]) -> dict[str, Any]:
    _arity(args, 2)
    graph_spec, mutation = args
    if not isinstance(mutation, dict):
        raise IntrinsicRefusal("MALFORMED_MUTATION", "mutation must be an object")
    try:
        graph = DirectedGraph.from_spec(graph_spec)
        kind = mutation.get("kind")
        if kind == "ADD_NODE" and set(mutation) == {"kind", "node"}:
            graph = graph.add_node(mutation["node"])
        elif kind == "REMOVE_NODE" and set(mutation) == {"kind", "node"}:
            graph = graph.remove_node(mutation["node"])
        elif kind == "ADD_EDGE" and set(mutation) == {"kind", "source", "target"}:
            graph = graph.add_edge(mutation["source"], mutation["target"])
        elif kind == "REMOVE_EDGE" and set(mutation) == {"kind", "source", "target"}:
            graph = graph.remove_edge(mutation["source"], mutation["target"])
        else:
            raise IntrinsicRefusal("MALFORMED_MUTATION", "unsupported graph mutation")
    except GraphInputError as exc:
        raise IntrinsicRefusal("INVALID_GRAPH", str(exc)) from exc
    return graph.to_spec()


def graph_reachable_pairs(args: tuple[Any, ...]) -> list[list[str]]:
    _arity(args, 1)
    try:
        return DirectedGraph.from_spec(args[0]).reachable_pairs()
    except GraphInputError as exc:
        raise IntrinsicRefusal("INVALID_GRAPH", str(exc)) from exc


def graph_query_paths(args: tuple[Any, ...]) -> list[dict[str, Any]]:
    _arity(args, 2)
    graph_spec, queries = args
    if not isinstance(queries, list):
        raise IntrinsicRefusal("INVALID_QUERIES", "queries must be a list")
    try:
        graph = DirectedGraph.from_spec(graph_spec)
        reports: list[dict[str, Any]] = []
        for query in queries:
            if not isinstance(query, list) or len(query) != 2 or not all(isinstance(x, str) and x for x in query):
                raise IntrinsicRefusal("INVALID_QUERIES", "each query must be [source,target]")
            source, target = query
            path = graph.shortest_path(source, target)
            reports.append(
                {
                    "source": source,
                    "target": target,
                    "reachable": path is not None,
                    "path": path,
                }
            )
        return reports
    except GraphInputError as exc:
        raise IntrinsicRefusal("INVALID_GRAPH", str(exc)) from exc
