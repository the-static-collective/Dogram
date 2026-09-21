from fractions import Fraction as F


def disagreement(plan):
    return sum(sum(row) for row in plan) - sum(plan[i][i] for i in range(len(plan)))


def transport_cost(plan, metric):
    n = len(plan)
    return sum(plan[i][j] * metric[i][j] for i in range(n) for j in range(n))


def marginals(plan):
    n = len(plan)
    left = tuple(sum(plan[i][j] for j in range(n)) for i in range(n))
    right = tuple(sum(plan[i][j] for i in range(n)) for j in range(n))
    return left, right


def specimen():
    z = F(0); t = F(1, 3)
    pi01 = ((z,t,z),(t,z,z),(z,z,t))
    pi12 = ((t,z,z),(z,z,t),(z,t,z))
    # Declared path metric on positions 0--1--2 with unequal edge lengths 1 and 2.
    d = ((F(0),F(1),F(3)),(F(1),F(0),F(2)),(F(3),F(2),F(0)))
    return {
        "pi01": pi01,
        "pi12": pi12,
        "metric": d,
        "marginals_pi01": marginals(pi01),
        "marginals_pi12": marginals(pi12),
        "disagreement_pi01": disagreement(pi01),
        "disagreement_pi12": disagreement(pi12),
        "cost_pi01": transport_cost(pi01,d),
        "cost_pi12": transport_cost(pi12,d),
    }


if __name__ == "__main__":
    print(specimen())
