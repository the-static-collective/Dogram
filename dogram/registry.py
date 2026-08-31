from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .intrinsics.core import (
    core_add,
    core_get,
    core_gt,
    core_length,
    core_same,
    core_select_first,
    core_sub,
    set_difference,
    trace_compare_ordered,
)
from .intrinsics.graph import graph_apply_mutation, graph_query_paths, graph_reachable_pairs

Intrinsic = Callable[[tuple[Any, ...]], Any]


class RegistryLookupError(KeyError):
    pass


@dataclass(frozen=True)
class IntrinsicDescriptor:
    intrinsic_id: str
    deterministic: bool = True
    versioned: bool = True

    def to_data(self) -> dict[str, Any]:
        return {
            "intrinsic_id": self.intrinsic_id,
            "deterministic": self.deterministic,
            "versioned": self.versioned,
        }


class Registry:
    def __init__(self, entries: dict[str, Intrinsic]):
        self._entries = dict(entries)

    def ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._entries))

    def resolve(self, intrinsic_id: str) -> Intrinsic:
        try:
            return self._entries[intrinsic_id]
        except KeyError as exc:
            raise RegistryLookupError(intrinsic_id) from exc

    def describe(self, intrinsic_id: str) -> dict[str, Any]:
        if intrinsic_id not in self._entries:
            raise RegistryLookupError(intrinsic_id)
        return IntrinsicDescriptor(intrinsic_id).to_data()


def build_bootstrap_registry() -> Registry:
    return Registry(
        {
            "core.get@1": core_get,
            "core.same@1": core_same,
            "core.add@1": core_add,
            "core.sub@1": core_sub,
            "core.length@1": core_length,
            "core.gt@1": core_gt,
            "core.select_first@1": core_select_first,
            "trace.compare_ordered@1": trace_compare_ordered,
            "graph.apply_mutation@1": graph_apply_mutation,
            "graph.reachable_pairs@1": graph_reachable_pairs,
            "graph.query_paths@1": graph_query_paths,
            "set.difference@1": set_difference,
        }
    )
