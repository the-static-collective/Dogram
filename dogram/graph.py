from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any


class GraphInputError(ValueError):
    pass


@dataclass(frozen=True)
class DirectedGraph:
    nodes: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]

    @classmethod
    def from_spec(cls, spec: dict[str, Any]) -> "DirectedGraph":
        if not isinstance(spec, dict) or not isinstance(spec.get("nodes"), list) or not isinstance(spec.get("edges"), list):
            raise GraphInputError("graph must contain nodes and edges lists")
        nodes = spec["nodes"]
        if any(not isinstance(n, str) or not n for n in nodes) or len(nodes) != len(set(nodes)):
            raise GraphInputError("nodes must be unique non-empty strings")
        edge_pairs: list[tuple[str, str]] = []
        for edge in spec["edges"]:
            if not isinstance(edge, list) or len(edge) != 2 or not all(isinstance(x, str) and x for x in edge):
                raise GraphInputError("edges must be [source,target] string pairs")
            edge_pairs.append((edge[0], edge[1]))
        if len(edge_pairs) != len(set(edge_pairs)):
            raise GraphInputError("edges must be unique")
        node_set = set(nodes)
        if any(a not in node_set or b not in node_set for a, b in edge_pairs):
            raise GraphInputError("edge endpoints must exist")
        return cls(tuple(sorted(nodes)), tuple(sorted(edge_pairs)))

    def to_spec(self) -> dict[str, Any]:
        return {"nodes": list(self.nodes), "edges": [[a, b] for a, b in self.edges]}

    def _neighbors(self, node: str) -> list[str]:
        return sorted(b for a, b in self.edges if a == node)

    def shortest_path(self, source: str, target: str) -> list[str] | None:
        if source not in self.nodes or target not in self.nodes:
            raise GraphInputError("source and target must exist")
        if source == target:
            return [source]
        queue = deque([[source]])
        seen = {source}
        while queue:
            path = queue.popleft()
            for nxt in self._neighbors(path[-1]):
                if nxt in seen:
                    continue
                new_path = path + [nxt]
                if nxt == target:
                    return new_path
                seen.add(nxt)
                queue.append(new_path)
        return None

    def reachable(self, source: str, target: str) -> bool:
        return self.shortest_path(source, target) is not None

    def reachable_pairs(self) -> list[list[str]]:
        pairs: list[list[str]] = []
        for source in self.nodes:
            for target in self.nodes:
                if source != target and self.reachable(source, target):
                    pairs.append([source, target])
        return pairs

    def remove_node(self, node: str) -> "DirectedGraph":
        if node not in self.nodes:
            raise GraphInputError("node does not exist")
        return DirectedGraph.from_spec({"nodes": [n for n in self.nodes if n != node], "edges": [[a, b] for a, b in self.edges if a != node and b != node]})

    def remove_edge(self, source: str, target: str) -> "DirectedGraph":
        if (source, target) not in self.edges:
            raise GraphInputError("edge does not exist")
        return DirectedGraph.from_spec({"nodes": list(self.nodes), "edges": [[a, b] for a, b in self.edges if (a, b) != (source, target)]})

    def add_node(self, node: str) -> "DirectedGraph":
        if not isinstance(node, str) or not node or node in self.nodes:
            raise GraphInputError("node already exists or is invalid")
        return DirectedGraph.from_spec({"nodes": [*self.nodes, node], "edges": [[a, b] for a, b in self.edges]})

    def add_edge(self, source: str, target: str) -> "DirectedGraph":
        if source not in self.nodes or target not in self.nodes:
            raise GraphInputError("edge endpoints must exist")
        if (source, target) in self.edges:
            raise GraphInputError("edge already exists")
        return DirectedGraph.from_spec({"nodes": list(self.nodes), "edges": [[a, b] for a, b in self.edges] + [[source, target]]})
