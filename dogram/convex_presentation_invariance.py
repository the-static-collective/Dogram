"""Bounded exact research kernel for CONVEX-PRESENTATION-INVARIANCE-001.

This module intentionally handles only a frozen two-dimensional triangle specimen.
It is not a general convex-hull or optimization engine.
"""

from fractions import Fraction


def _q(value):
    return value if isinstance(value, Fraction) else Fraction(value)


def convex_combination(points, weights):
    if len(points) != len(weights) or not points:
        raise ValueError("points and weights must be nonempty and aligned")
    qweights = tuple(_q(weight) for weight in weights)
    if any(weight < 0 for weight in qweights) or sum(qweights) != 1:
        raise ValueError("weights must be a convex combination")
    dimension = len(points[0])
    if any(len(point) != dimension for point in points):
        raise ValueError("points must share a dimension")
    return tuple(
        sum(weight * _q(point[index]) for point, weight in zip(points, qweights))
        for index in range(dimension)
    )


def support_value(generators, direction):
    if not generators:
        raise ValueError("generators must be nonempty")
    if any(len(point) != len(direction) for point in generators):
        raise ValueError("direction dimension must match generators")
    return max(
        sum(_q(x) * _q(d) for x, d in zip(point, direction))
        for point in generators
    )


def uniform_generator_mean(generators):
    if not generators:
        raise ValueError("generators must be nonempty")
    dimension = len(generators[0])
    if any(len(point) != dimension for point in generators):
        raise ValueError("generators must share a dimension")
    n = Fraction(len(generators), 1)
    return tuple(sum(_q(point[i]) for point in generators) / n for i in range(dimension))


def _inside_frozen_triangle(point):
    x, y = map(_q, point)
    return x >= 0 and y >= 0 and x + y <= 2


def verify_same_triangle_hull(minimal_generators, redundant_generators):
    expected_vertices = {(Fraction(0), Fraction(0)), (Fraction(2), Fraction(0)), (Fraction(0), Fraction(2))}
    minimal = {tuple(map(_q, point)) for point in minimal_generators}
    redundant = tuple(tuple(map(_q, point)) for point in redundant_generators)
    if minimal != expected_vertices:
        raise ValueError("minimal_generators must be the frozen triangle vertices")
    if not expected_vertices.issubset(set(redundant)):
        raise ValueError("redundant presentation must retain all frozen extreme points")
    if any(not _inside_frozen_triangle(point) for point in redundant):
        raise ValueError("all redundant generators must lie in the frozen triangle")
    extras = tuple(sorted(set(redundant) - expected_vertices))
    return {
        "same_hull": True,
        "extreme_points": tuple(sorted((int(x), int(y)) for x, y in expected_vertices)),
        "redundant_points": tuple((int(x), int(y)) for x, y in extras),
    }
