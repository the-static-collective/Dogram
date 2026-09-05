# SHEAF-LAPLACIAN-ENERGY-001

Status: bounded research specimen. No public operator.

## Question

Can two finite cellular-sheaf specimens have the exact same global-section space while assigning different exact Laplacian energy and nonzero spectral data to off-section cochains?

Yes.

## Frozen carrier

Use the three-vertex path `0 -- 1 -- 2`, one-dimensional real stalks, and positive integer edge scales `(p,q)`. Define the degree-0 coboundary

`delta(x0,x1,x2) = (p(x1-x0), q(x2-x1))`.

For every positive `p,q`,

`ker(delta) = span{(1,1,1)}`.

Thus the global-section subspace and nullity are unchanged by these declared edge reweightings.

The sheaf Laplacian is `L = delta^T delta`:

```
[p^2        -p^2          0]
[-p^2  p^2 + q^2      -q^2]
[0           -q^2       q^2]
```

and

`det(lambda I - L) = lambda (lambda^2 - 2(p^2+q^2) lambda + 3p^2q^2)`.

## Control

`(p,q)=(1,1)` gives

```
L = [[ 1,-1, 0],
     [-1, 2,-1],
     [ 0,-1, 1]]
```

with characteristic polynomial

`lambda^3 - 4 lambda^2 + 3 lambda`,

trace `4`, nonzero-eigenvalue product `3`, and probe energy for `x=(1,0,0)` equal to `1`.

## Hostile specimen

`(p,q)=(2,1)` gives

```
L = [[ 4,-4, 0],
     [-4, 5,-1],
     [ 0,-1, 1]]
```

with the exact same global-section subspace `span{(1,1,1)}` and nullity `1`, but characteristic polynomial

`lambda^3 - 10 lambda^2 + 12 lambda`,

trace `10`, nonzero-eigenvalue product `12`, and the same probe `x=(1,0,0)` has energy `4`.

Therefore:

`SAME GLOBAL SECTION SPACE != SAME OFF-SECTION LAPLACIAN GEOMETRY.`

and, more cautiously,

`COHOMOLOGICAL FEASIBILITY DOES NOT DETERMINE THE DECLARED CONSISTENCY ENERGY.`

## Why this is not RETURN-GLUING-OBSTRUCTION-001 again

`RETURN-GLUING-OBSTRUCTION-001` changes the restriction system in a way that changes global-section capacity/nullity. This specimen holds the entire degree-0 global-section subspace fixed and changes only the weighted Laplacian geometry seen away from that kernel.

The delta therefore lives strictly below/alongside the binary gluing question: exact feasibility agrees while non-harmonic spectral data differ.

## Literature basis

Hansen & Ghrist, *Toward a spectral theory of cellular sheaves*, Journal of Applied and Computational Topology 3 (2019), 315-358, DOI `10.1007/s41468-019-00038-7`, develops cellular-sheaf Laplacians, identifies the harmonic/kernel layer with sheaf cohomology, and explicitly distinguishes weighted constant sheaves that are isomorphic as sheaves but not unitarily so. It also emphasizes that normalization is properly viewed as a reweighting of stalk inner products rather than a purely combinatorial operation on a fixed Laplacian.

That distinction matters here: the edge scales are part of the declared weighted/inner-product receipt. They are not silently promoted to new topology, evidence, or mechanism.

## Dogram pressure

Documented mathematics:
- `ker(L)=ker(delta)` for this finite real cochain model;
- the nonzero spectrum of `L=delta^T delta` carries information not exhausted by kernel dimension;
- weighted cellular sheaves can preserve section structure while changing unitary/spectral geometry.

Dogram inference:
- a binary pass/fail global-section receipt can discard exact off-kernel structure;
- if a calculation consumes a metric, weighting, normalization, or stalk inner product, that choice belongs in the decoder receipt;
- identical nullspaces do not license identical energy or spectral claims.

Speculation / HOLD:
- whether such spectral gaps should eventually serve as a generic Dogram notion of robustness, confidence, tension, or inconsistency margin is not established here;
- no application-domain semantics are inferred from larger or smaller eigenvalues.

## Explicit refusals

- `SAME GLOBAL SECTION SPACE != SAME EVIDENCE`;
- `LAPLACIAN ENERGY != HISTORICAL CONFLICT`;
- `SPECTRAL GAP != CONFIDENCE`;
- `NONZERO EIGENVALUE != CAUSAL FORCE`;
- `WEIGHT CHANGE != OCCURRENCE`;
- `SHEAF ISOMORPHISM != UNITARY EQUIVALENCE`;
- `ALGEBRAIC STIFFNESS != TRUTH`.

## HOLD

No `sheaf_laplacian@1`, `spectral_gap@1`, `consistency_energy@1`, `robustness@1`, `weighted_sheaf@1`, or public dispatch/schema promotion.

## Strongest next frontier

Do not simply add a larger graph. The next earned question is whether two specimens can preserve not only the same global-section space but also the same low-order spectral summaries (for example nullity and trace) while differing in a higher spectral invariant or localized energy receipt. That would pressure which spectral summaries are genuinely lossless for the bounded question being asked.
