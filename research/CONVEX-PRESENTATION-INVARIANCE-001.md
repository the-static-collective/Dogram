# CONVEX-PRESENTATION-INVARIANCE-001

Status: bounded research specimen; HOLD; no public operator promotion.

## Question

Can two finite generator lists present the same convex feasible geometry while generator-sensitive summaries differ?

## Frozen exact specimen

Minimal presentation:

`G = {(0,0),(2,0),(0,2)}`.

Redundant presentation:

`G' = G union {(1,1)}`.

The extra point is redundant because

`(1,1) = 1/2 (2,0) + 1/2 (0,2)`.

Therefore `conv(G)=conv(G')`, the same closed triangle.

For every declared linear support direction in the fixture, the support value agrees under both presentations. This is the finite receipt for the fact that linear optimization consumes the feasible hull, not the accidental presence of a redundant generator.

But uniform averaging over the listed generators differs:

- `mean(G)=(2/3,2/3)`;
- `mean(G')=(3/4,3/4)`.

So a generator list is not silently a probability law. Adding a feasible redundant point changes the presentation-sensitive average while leaving the feasible convex geometry fixed.

## Seals

- `GENERATORS ARE A PRESENTATION; THE CONVEX HULL IS THE DECLARED FEASIBLE GEOMETRY.`
- `REDUNDANT GENERATOR != NEW FEASIBLE GEOMETRY.`
- `UNIFORM OVER GENERATORS != UNIFORM OVER THE POLYTOPE.`
- `A GENERATOR LIST != A PRIOR DISTRIBUTION.`
- `RECEIPT WHETHER THE CALCULATION CONSUMED THE PRESENTATION OR THE HULL.`

## Dogram boundary

- convex membership != occurrence;
- feasible != evidenced;
- extreme point != authority;
- optimization optimum != truth;
- redundant representation != redundant real-world event;
- presentation delta != feasible-set delta;
- an averaging rule requires its own declared measure/weights.

## Literature basis

Centore (2020), *Coloration Technology*, DOI `10.1111/cote.12497`, explicitly notes that generating sets for a convex polytope are not unique and that interior/superfluous generating points may be present without changing the polytope.

Said & Wegman (2009), *WIREs Computational Statistics*, DOI `10.1002/wics.16`, reviews linear-programming feasible regions as convex polytopes and the role of extreme points/basic feasible solutions in linear optimization.

Sung & Maravelias (2007), *AIChE Journal*, DOI `10.1002/aic.11167`, explicitly distinguishes V-representations by vertices/generating feasible points from H-representations by inequalities.

No claim is made that these papers contain this Dogram fixture or interpretation.

## Scope

The kernel is deliberately limited to this frozen two-dimensional triangle. It is not a general hull package, probability engine, prior estimator, sampler, optimizer, or policy chooser.

No `convex_hull@1`, `generator@1`, `polytope@1`, `measure@1`, `prior@1`, or `optimize@1` promotion.

## Next frontier

Two different presentations can describe the same feasible set not only by redundant V-generators but by distinct H-representations with redundant inequalities. The next useful specimen should test whether a receipt can distinguish `PRESENTATION EQUIVALENCE` from `GEOMETRIC EQUALITY` without committing to a canonical representation.
