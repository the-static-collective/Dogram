# COCHAIN-WITNESS-NONUNIQUENESS-001

## Question

Can the same exact associator-table change admit more than one normalized 2-cochain witness, even after the endpoint 3-coboundary is held fixed?

## Frozen finite model

Work over `G = Z/3Z` with coefficients `H = Z/3Z` and trivial action.

For a normalized 2-cochain `beta`, use the inhomogeneous coboundary

`(delta beta)(g,h,k) = beta(h,k) - beta(g+h,k) + beta(g,h+k) - beta(g,h) mod 3`.

Freeze the first witness

- `beta1(1,1)=1`;
- `beta1=0` elsewhere.

Freeze the normalized carry 2-cocycle `c` by

- `c(g,h)=1` when representatives `g,h in {0,1,2}` satisfy `g+h >= 3`;
- `c=0` otherwise.

Then define `beta2 = beta1 + c mod 3`.

## Exact result

The witnesses are pointwise different:

- `supp(beta1) = {(1,1)->1}`;
- `supp(beta2) = {(1,1)->1,(1,2)->1,(2,1)->1,(2,2)->1}`.

Their difference is exactly `c`, supported on

- `(1,2)->1`;
- `(2,1)->1`;
- `(2,2)->1`.

Complete enumeration over all 27 triples verifies `delta c = 0`, so `c` is a normalized 2-cocycle.

Both witnesses nevertheless produce the same nonzero 3-coboundary, with support

- `(1,1,2)->2`;
- `(1,2,2)->1`;
- `(2,1,1)->1`;
- `(2,2,1)->2`.

Thus

`delta beta1 = delta beta2 != 0`

while

`beta1 != beta2`.

A complete enumeration of all `3^2 = 9` normalized 1-cochains finds no `gamma` with `delta gamma = c`. In this declared finite normalized model, the witness difference is therefore a nontrivial `H^2` residue rather than a lower-cochain reparameterization.

## Seals

**SAME PRESENTATION DELTA != SAME WITNESS.**

**FIXING THE ENDPOINT COBBOUNDARY DOES NOT FIX THE COCHAIN THAT PAYS FOR IT.**

**KEEP THE WITNESS DIFFERENCE; A COCYCLE RESIDUE CAN SURVIVE AFTER THE ENDPOINT DELTA IS HELD FIXED.**

## Provenance

Documented mathematics:

- Standard cochain-complex linearity gives `delta(beta2-beta1)=0` whenever `delta beta1 = delta beta2`; witness differences therefore lie in the 2-cocycle space.
- Group cohomology is cocycles modulo coboundaries; a cocycle not produced by a lower coboundary represents a nontrivial cohomology residue.
- Weak/coherent 2-group associators are encoded by 3-cocycles/cohomology classes, while 2-cochains occur as coherence/change-of-presentation data. Bhardwaj, Schafer-Nameki & Wu (2022), DOI `10.1002/prop.202200143`, gives a modern 2-group summary and explicitly uses 2-cochains whose coboundaries match declared 3-cocycle data.
- Armario & Flannery (2017), DOI `10.1002/jcd.21597`, states the standard finite-group `H^2 = Z^2/B^2` cocycle/coboundary quotient.

Exact finite inference:

- The particular `Z/3Z` pair above is a bounded Dogram specimen verified by complete finite enumeration.
- Wolfram Language independently reproduced the carry support, zero 2-cocycle residual on all 27 triples, the identical four-entry nonzero coboundaries of `beta1` and `beta2`, and the absence of a normalized 1-cochain cobounding to `c` among all 9 candidates.

No claim is made that this finite witness pair is canonical or uniquely minimal.

## Boundaries / refusals

- COCHAIN WITNESS != HISTORICAL PATH.
- SAME ENDPOINT DELTA != SAME CAUSAL PROCESS.
- NONTRIVIAL H2 RESIDUE != HIDDEN CAUSE.
- COCYCLE DIFFERENCE != EVIDENCE DIFFERENCE.
- COHOMOLOGY CLASS != AUTHORITY CLASS.
- WITNESS NONUNIQUENESS != SEMANTIC AMBIGUITY.
- PENTAGON/COCHAIN COHERENCE != TRUTH.

## Promotion verdict

Research slice only. Do not promote `cochain_witness@1`, `h2_residue@1`, `cocycle_difference@1`, `associator_change@1`, or any evidence/occurrence/causal/semantic/authority surface.

## Strongest next frontier

Hold the two endpoint associator tables and the witness-difference cohomology class fixed, then search for distinct witness histories/compositions whose *composed* 2-cochain receipts agree only after a higher coherence relation. That would pressure the difference between endpoint witness equality and path/composition equality without silently identifying either with history.
