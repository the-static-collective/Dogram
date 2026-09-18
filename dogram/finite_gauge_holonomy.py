from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence

Permutation = tuple[int, ...]
Edge = tuple[str, str]


def _validate_permutation(value: Permutation) -> None:
    if not value:
        raise ValueError("permutation must be non-empty")
    if tuple(sorted(value)) != tuple(range(1, len(value) + 1)):
        raise ValueError("invalid permutation image tuple")


def compose(left: Permutation, right: Permutation) -> Permutation:
    """Return left after right (left o right) using 1-indexed image tuples."""
    _validate_permutation(left)
    _validate_permutation(right)
    if len(left) != len(right):
        raise ValueError("permutations must have the same degree")
    return tuple(left[right[index] - 1] for index in range(len(left)))


def inverse(value: Permutation) -> Permutation:
    _validate_permutation(value)
    result = [0] * len(value)
    for index, image in enumerate(value, start=1):
        result[image - 1] = index
    return tuple(result)


def identity(degree: int) -> Permutation:
    if degree <= 0:
        raise ValueError("degree must be positive")
    return tuple(range(1, degree + 1))


def product(values: Iterable[Permutation], *, degree: int | None = None) -> Permutation:
    items = list(values)
    if not items:
        if degree is None:
            raise ValueError("degree is required for an empty product")
        return identity(degree)
    result = identity(len(items[0]))
    for value in items:
        result = compose(result, value)
    return result


def permutation_group_closure(generators: Sequence[Permutation]) -> tuple[Permutation, ...]:
    if not generators:
        raise ValueError("at least one generator is required")
    degree = len(generators[0])
    for generator in generators:
        _validate_permutation(generator)
        if len(generator) != degree:
            raise ValueError("generators must have the same degree")

    discovered = {identity(degree)}
    frontier = [identity(degree)]
    generators_with_inverses = list(generators) + [
        inverse(generator) for generator in generators
    ]

    while frontier:
        current = frontier.pop()
        for generator in generators_with_inverses:
            candidate = compose(current, generator)
            if candidate not in discovered:
                discovered.add(candidate)
                frontier.append(candidate)

    return tuple(sorted(discovered))


def conjugacy_orbit(
    element: Permutation,
    group_elements: Sequence[Permutation],
) -> tuple[Permutation, ...]:
    _validate_permutation(element)
    orbit = {
        compose(compose(group_element, element), inverse(group_element))
        for group_element in group_elements
    }
    return tuple(sorted(orbit))


def gauge_transform_edges(
    edges: Mapping[Edge, Permutation],
    vertex_gauges: Mapping[str, Permutation],
) -> dict[Edge, Permutation]:
    transformed: dict[Edge, Permutation] = {}
    for (source, target), transport in edges.items():
        try:
            source_gauge = vertex_gauges[source]
            target_gauge = vertex_gauges[target]
        except KeyError as error:
            raise ValueError(f"missing gauge for vertex {error.args[0]}") from error
        transformed[(source, target)] = compose(
            compose(source_gauge, transport),
            inverse(target_gauge),
        )
    return transformed


def holonomy(
    edges: Mapping[Edge, Permutation],
    directed_cycle: Sequence[Edge],
) -> Permutation:
    if not directed_cycle:
        raise ValueError("directed cycle must be non-empty")

    for index, edge in enumerate(directed_cycle):
        next_edge = directed_cycle[(index + 1) % len(directed_cycle)]
        if edge[1] != next_edge[0]:
            raise ValueError("directed_cycle is not contiguous and closed")

    try:
        transports = [edges[edge] for edge in directed_cycle]
    except KeyError as error:
        raise ValueError(f"missing transport for edge {error.args[0]}") from error

    return product(transports)
