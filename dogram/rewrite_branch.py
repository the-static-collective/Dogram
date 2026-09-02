from __future__ import annotations

from dataclasses import dataclass
from collections import deque


@dataclass
class RewriteInputError(ValueError):
    reason_code: str
    residual: str

    def __str__(self) -> str:
        return self.residual


@dataclass(frozen=True)
class RewriteBranchAnalysis:
    start: str
    rules: tuple[tuple[str, str], ...]
    immediate_successors: tuple[str, ...]
    reachable_states: tuple[str, ...]
    normal_forms: tuple[str, ...]
    rewrite_edges: tuple[tuple[str, str], ...]

    @property
    def reachable_state_count(self) -> int:
        return len(self.reachable_states)

    @property
    def unique_normal_form(self) -> bool:
        return len(self.normal_forms) == 1

    def to_data(self) -> dict[str, object]:
        return {
            "start": self.start,
            "rules": [list(rule) for rule in self.rules],
            "immediate_successors": list(self.immediate_successors),
            "reachable_states": list(self.reachable_states),
            "normal_forms": list(self.normal_forms),
            "rewrite_edges": [list(edge) for edge in self.rewrite_edges],
            "reachable_state_count": self.reachable_state_count,
            "unique_normal_form": self.unique_normal_form,
        }


def _validate(start: str, rules: tuple[tuple[str, str], ...]) -> None:
    if not isinstance(start, str):
        raise RewriteInputError("INVALID_START", "start must be a string")
    if not isinstance(rules, tuple):
        raise RewriteInputError("INVALID_RULES", "rules must be a tuple of (lhs, rhs) pairs")

    for rule in rules:
        if (
            not isinstance(rule, tuple)
            or len(rule) != 2
            or not isinstance(rule[0], str)
            or not isinstance(rule[1], str)
        ):
            raise RewriteInputError(
                "INVALID_RULE", "each rule must be a tuple of two strings"
            )
        lhs, rhs = rule
        if lhs == "":
            raise RewriteInputError("EMPTY_LHS", "rule lhs must not be empty")
        if len(rhs) >= len(lhs):
            raise RewriteInputError(
                "NON_DECREASING_RULE",
                f"rule {lhs!r} -> {rhs!r} must strictly decrease string length",
            )


def _successors(term: str, rules: tuple[tuple[str, str], ...]) -> tuple[str, ...]:
    successors: set[str] = set()
    for lhs, rhs in rules:
        start = 0
        while True:
            index = term.find(lhs, start)
            if index < 0:
                break
            successors.add(term[:index] + rhs + term[index + len(lhs) :])
            start = index + 1
    return tuple(sorted(successors))


def analyze_rewrite_branch(
    start: str, rules: tuple[tuple[str, str], ...]
) -> RewriteBranchAnalysis:
    """Enumerate the finite rewrite graph reachable from one declared start term.

    Every rule must strictly decrease string length. That restriction guarantees
    termination for this bounded research kernel; the result does not claim
    global confluence of the rewrite system outside the declared start term.
    """

    _validate(start, rules)

    immediate = _successors(start, rules)
    queue: deque[str] = deque([start])
    seen: set[str] = {start}
    edges: set[tuple[str, str]] = set()
    normal_forms: set[str] = set()

    while queue:
        term = queue.popleft()
        next_terms = _successors(term, rules)
        if not next_terms:
            normal_forms.add(term)
            continue
        for target in next_terms:
            edges.add((term, target))
            if target not in seen:
                seen.add(target)
                queue.append(target)

    return RewriteBranchAnalysis(
        start=start,
        rules=rules,
        immediate_successors=immediate,
        reachable_states=tuple(sorted(seen)),
        normal_forms=tuple(sorted(normal_forms)),
        rewrite_edges=tuple(sorted(edges)),
    )


__all__ = [
    "RewriteBranchAnalysis",
    "RewriteInputError",
    "analyze_rewrite_branch",
]
