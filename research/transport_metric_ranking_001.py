from fractions import Fraction
from itertools import permutations

STATES = (0, 1, 2, 3)
PI = (0, 1, 3, 2)   # swap 2<->3
RHO = (0, 2, 1, 3)  # swap 1<->2


def line_metric(coords):
    return tuple(tuple(abs(coords[i] - coords[j]) for j in STATES) for i in STATES)


def metric_ok(d):
    return all(d[i][i] == 0 for i in STATES) and all(
        d[i][j] == d[j][i] and (i == j or d[i][j] > 0) and
        all(d[i][j] <= d[i][k] + d[k][j] for k in STATES)
        for i in STATES for j in STATES
    )


def uniform_permutation_cost(perm, d):
    return sum((Fraction(d[i][perm[i]], 4) for i in STATES), Fraction(0))


def specimen():
    # Both are pullbacks of Euclidean distance on R under injective embeddings,
    # hence metrics; metric_ok independently checks all finite axioms.
    d_left = line_metric((0, 1, 7, 3))
    d_right = line_metric((0, 1, 3, 7))
    out = {
        "pi": PI,
        "rho": RHO,
        "d_left": d_left,
        "d_right": d_right,
        "metrics_valid": metric_ok(d_left) and metric_ok(d_right),
        "left_costs": (uniform_permutation_cost(PI, d_left), uniform_permutation_cost(RHO, d_left)),
        "right_costs": (uniform_permutation_cost(PI, d_right), uniform_permutation_cost(RHO, d_right)),
    }
    out["ranking_reverses"] = out["left_costs"][0] < out["left_costs"][1] and out["right_costs"][0] > out["right_costs"][1]
    return out


if __name__ == "__main__":
    print(specimen())
