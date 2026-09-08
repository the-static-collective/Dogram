# H-REPRESENTATION-DUAL-DEGENERACY-001

Status: bounded research specimen; HOLD; no public operator promotion.

## Question

Can two H-representations describe the same feasible geometry and same primal optimum while changing the structure of lawful dual certificates?

## Frozen exact specimen

Minimal H-presentation of the triangle:

- `-x <= 0`;
- `-y <= 0`;
- `x + y <= 2`.

Redundant H-presentation adds:

- `x <= 2`.

The added inequality is redundant because the retained constraints already imply

`x <= x + y <= 2`

from `y >= 0`.

Therefore both systems define exactly the same triangle with vertices `(0,0)`, `(2,0)`, `(0,2)`.

For the fixed primal objective `max x`, both presentations have primal optimum value `2`, attained at `(2,0)`.

## Dual-certificate delta

Write the LP dual in the exact form

`min b^T lambda` subject to `A^T lambda = (1,0)` and `lambda >= 0`.

For the minimal presentation, the unique optimal multiplier vector is

`lambda = (0,1,1)`

with objective value `2`.

For the redundant presentation, every

`lambda(t) = (0,t,t,1-t)`, `0 <= t <= 1`,

is dual feasible and has objective value `2`.

Thus the feasible set, objective, primal optimum, and optimal value are unchanged, while the optimal dual-certificate set changes from a singleton to a continuum.

## Seals

- `CONSTRAINTS ARE A PRESENTATION; THE FEASIBLE SET IS THE DECLARED GEOMETRY.`
- `REDUNDANT INEQUALITY != NEW FEASIBLE WORLD.`
- `SAME FEASIBLE SET + SAME OBJECTIVE + SAME PRIMAL OPTIMUM != SAME DUAL CERTIFICATE SET.`
- `DUAL MULTIPLIERS ARE REPRESENTATION-SENSITIVE RECEIPTS.`
- `RECEIPT WHICH CONSTRAINT PRESENTATION THE CERTIFICATE CONSUMED.`

## Dogram boundary

- redundant constraint != redundant occurrence;
- binding != evidential;
- active constraint != causal mechanism;
- dual multiplier != authority weight;
- multiplier nonuniqueness != ambiguity in historical reality;
- feasible geometry != evidence surface;
- same optimum != same meaning;
- presentation delta != feasible-set delta.

## Literature basis

Paulraj et al. (2010), *Mathematical Problems in Engineering*, DOI `10.1155/2010/723402`, defines a redundant constraint as one removable without changing the feasible region and explicitly distinguishes weakly redundant constraints that can still be binding somewhere on the feasible set.

Buerger, Cannon & Kouvaritakis (2016), *International Journal of Robust and Nonlinear Control*, DOI `10.1002/rnc.3501`, treats degeneracy caused by linear dependence in active constraint sets and notes that optimal primal/dual quantities can become multivalued under such degeneracy.

Fabiani & Goulart (2024), *International Journal of Robust and Nonlinear Control*, DOI `10.1002/rnc.7315`, states that linear independence of active constraints yields a unique choice of Lagrange multipliers in the corresponding dual problem, providing the contrasting regular case.

No claim is made that these papers contain this exact Dogram fixture.

## Verification

The exact finite arithmetic was independently replayed with rational arithmetic before landing:

- both presentations define the same frozen triangle by the explicit implication `x<=x+y<=2`;
- primal optimum for `max x` is exactly `2`;
- minimal dual certificate `(0,1,1)` satisfies `A^T lambda=(1,0)` and has value `2`;
- redundant family `(0,t,t,1-t)` for `0<=t<=1` satisfies the same dual equality and has value `2` for every `t`.

Wolfram was attempted for independent verification but the connector returned a network error, so no Wolfram-verification claim is made.

## Scope

This slice is deliberately restricted to one exact two-dimensional LP specimen. It is not a general optimizer, redundancy detector, dual solver, KKT engine, sensitivity engine, or polyhedral library.

No `constraint@1`, `h_representation@1`, `dual@1`, `multiplier@1`, `degeneracy@1`, `optimizer@1`, or authority/evidence operator is promoted.

## Next frontier

The same geometry can admit different *minimal* presentations under scaling, row permutation, or positive rescaling of inequalities. A next bounded specimen should distinguish `CONSTRAINT IDENTITY` from `FACET IDENTITY`, and pressure whether normalized facet provenance is needed before comparing multiplier magnitudes across presentations.
