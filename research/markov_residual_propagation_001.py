"""MARKOV-RESIDUAL-PROPAGATION-001: exact finite-horizon perturbation receipts.

Research only. Probabilities are Fraction-valued. No occurrence/evidence semantics.
"""
from fractions import Fraction


def tv(p, q):
    return sum(abs(a-b) for a,b in zip(p,q)) / 2


def step(mu, P):
    n=len(mu)
    return tuple(sum(mu[i]*P[i][j] for i in range(n)) for j in range(n))


def dobrushin(P):
    return max(tv(P[i], P[j]) for i in range(len(P)) for j in range(len(P)))


def row_residual(P, Q):
    return max(tv(P[i], Q[i]) for i in range(len(P)))


def propagate(mu, P, Q, horizon):
    """Compare two declared kernels from the same initial law.

    Returns exact observed TV deltas and the standard recurrence envelope
    e_t <= eps * sum_{j=0}^{t-1} kappa^j, where kappa is Dobrushin(P).
    The envelope is a mathematical bound, not a semantic tolerance.
    """
    eps=row_residual(P,Q)
    kappa=dobrushin(P)
    p=q=tuple(mu)
    rows=[]
    bound=Fraction(0)
    for t in range(1,horizon+1):
        p=step(p,P); q=step(q,Q)
        bound=eps + kappa*bound
        rows.append({"t":t,"tv":tv(p,q),"bound":bound})
    return {"epsilon":eps,"kappa":kappa,"steps":rows}


def frozen_specimen(epsilon=Fraction(1,10), horizon=10):
    # Noncontractive P: identity. Q leaks epsilon from state 0 into absorbing 1.
    P=((Fraction(1),Fraction(0)),(Fraction(0),Fraction(1)))
    Q=((1-epsilon,epsilon),(Fraction(0),Fraction(1)))
    r=propagate((Fraction(1),Fraction(0)),P,Q,horizon)
    expected=1-(1-epsilon)**horizon
    assert r["kappa"] == 1
    assert r["steps"][-1]["tv"] == expected
    return r

if __name__ == "__main__":
    r=frozen_specimen()
    print("epsilon", r["epsilon"], "kappa", r["kappa"])
    for x in r["steps"]: print(x["t"], x["tv"], x["bound"])
