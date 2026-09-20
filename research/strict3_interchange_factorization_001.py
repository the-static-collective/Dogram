"""STRICT3-INTERCHANGE-FACTORIZATION-001.

A finite degenerate strict-3-category top-cell specimen.
This is structural algebra only: no occurrence/evidence/causal semantics.
"""
from itertools import product

CELLS = tuple(product(range(2), repeat=2))
UNIT = (0, 0)
GAMMA = (1, 0)
DELTA = (0, 1)


def compose_0(x, y):
    """First top-cell composition; Z2 x Z2 addition."""
    return ((x[0] + y[0]) % 2, (x[1] + y[1]) % 2)


def compose_1(x, y):
    """Second top-cell composition; same carrier, independently checked."""
    return ((x[0] + y[0]) % 2, (x[1] + y[1]) % 2)


def verify_strict_interchange_specimen():
    unit_0 = all(compose_0(UNIT, x) == x == compose_0(x, UNIT) for x in CELLS)
    unit_1 = all(compose_1(UNIT, x) == x == compose_1(x, UNIT) for x in CELLS)
    interchange = all(
        compose_1(compose_0(a, b), compose_0(c, d))
        == compose_0(compose_1(a, c), compose_1(b, d))
        for a, b, c, d in product(CELLS, repeat=4)
    )
    operations_coincide = all(compose_0(a, b) == compose_1(a, b) for a, b in product(CELLS, repeat=2))
    commutative = all(compose_0(a, b) == compose_0(b, a) for a, b in product(CELLS, repeat=2))

    path_left = ("Gamma", "Delta")
    path_right = ("Delta", "Gamma")
    composite_left = compose_0(GAMMA, DELTA)
    composite_right = compose_0(DELTA, GAMMA)

    return {
        "carrier_size": len(CELLS),
        "quadruples_checked": len(CELLS) ** 4,
        "unit_0": unit_0,
        "unit_1": unit_1,
        "interchange": interchange,
        "operations_coincide": operations_coincide,
        "commutative": commutative,
        "same_boundary": True,
        "path_left": path_left,
        "path_right": path_right,
        "paths_distinct": path_left != path_right,
        "composite_left": composite_left,
        "composite_right": composite_right,
        "same_composite": composite_left == composite_right,
    }


if __name__ == "__main__":
    print(verify_strict_interchange_specimen())
