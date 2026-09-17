from __future__ import annotations

from collections.abc import Iterable, Mapping


def receipt_successor_incidence(
    representative_successors: Mapping[str, Iterable[str]],
) -> dict[str, object]:
    """Receipt exact representative-successor incidence and its coarse modal summaries."""
    if not representative_successors:
        raise ValueError("representative family must be non-empty")

    representatives = {
        str(representative): sorted(set(successors))
        for representative, successors in representative_successors.items()
    }
    representatives = dict(sorted(representatives.items()))
    successor_sets = [set(successors) for successors in representatives.values()]
    may = set().union(*successor_sets)
    must = set.intersection(*successor_sets)
    incidence = [
        {"representative": representative, "successor": successor}
        for representative, successors in representatives.items()
        for successor in successors
    ]

    return {
        "experiment": "SUCCESSOR-INCIDENCE-001",
        "representatives": representatives,
        "incidence": incidence,
        "may": sorted(may),
        "must": sorted(must),
        "member_sizes": sorted(len(successors) for successors in representatives.values()),
        "authority": "none",
    }
