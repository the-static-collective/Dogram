# STRICT3-INTERCHANGE-FACTORIZATION-001

## Question

After `PARALLEL-COHERENCE-WITNESS-001`, can strict higher-dimensional composition itself collapse distinct supplied 3-cell factorization orders to one composite while the complete lower boundary is fixed?

## Bounded specimen

Use the four-element commutative monoid `Z2 x Z2` as the top-cell endomorphisms of a fully degenerate strict 3-category (one 0-cell, one 1-cell, one 2-cell). Give the top cells two unital composition operations and instantiate both as componentwise addition mod 2.

The kernel exhaustively checks all `4^4 = 256` quadruples for strict interchange, both unit laws, coincidence of the two operations, and commutativity.

Choose distinct 3-cells:

- `Gamma = (1,0)`
- `Delta = (0,1)`

Then the supplied ordered factorizations

- `("Gamma", "Delta")`
- `("Delta", "Gamma")`

are distinct receipts, but strict composition gives the same top-cell composite `(1,1)` in both orders. Their entire lower-dimensional boundary is identical because the model has a single 0-, 1-, and 2-cell.

## Delta

**SAME COMPLETE LOWER BOUNDARY + SAME STRICT 3-CELL COMPOSITE != SAME SUPPLIED 3-CELL FACTORIZATION.**

This is the Eckmann-Hilton pressure point: two unital compositions satisfying interchange collapse to one commutative operation. The algebra may therefore forget ordering information that a provenance receipt still needs to retain.

## Provenance

- Standard strict higher-category substrate: strict n-categories carry morphisms in dimensions with strict composition axioms. Leinster's review of Gurski's *Coherence in Three-Dimensional Category Theory*, DOI `10.1112/blms/bdv015`, provides the strict/weak 3-category context.
- Interchange is a genuine categorical law; Xantcha, *Gabriel 2-quivers for finitary 2-categories*, DOI `10.1112/jlms/jdv037`, gives explicit horizontal-composition calculations in 2-categorical presentations. The finite kernel here checks its own strict interchange identity exhaustively.
- Wolfram semantic lookup found no direct strict-3-category/computad evaluator. Its `MultiwaySystem` and equational-proof resources distinguish rewrite paths/branch resolutions from endpoint equality; this is treated only as a computational analogue, not proof of the higher-categorical claim.

## Refusal boundary

- 3-cell != occurrence.
- factorization order != historical chronology.
- strict composite equality != evidentiary equality.
- interchange != causal independence.
- commutativity != permission to discard supplied provenance.
- degenerate strict 3-category != claim that Dogram's world is strict or degenerate.
- structural equality != semantic truth or authority.

## Reproduce

```bash
python research/strict3_interchange_factorization_001.py
pytest -q tests/test_strict3_interchange_factorization_001.py
```

## Promotion

None. Research-only kernel, tests, fixture/receipt. No public operator or schema. The specimen argues for retaining factorization receipts even where a strict algebra computes them to the same result.
