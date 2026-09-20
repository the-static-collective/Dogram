# PARALLEL-COHERENCE-WITNESS-001

Status: bounded research specimen; no public operator proposed.

## Question

After `PARALLEL-EQUIVALENCE-WITNESS-001` preserves two distinct 2-dimensional witnesses `alpha,beta : aa => bb`, what is lost if a later calculation records only that those witnesses are coherent/equivalent?

## Frozen specimen

Take two distinct parallel 2-cells

```
alpha, beta : aa => bb
```

and freely supply two distinct parallel 3-cell generators

```
Gamma, Delta : alpha ==> beta.
```

Their complete 2-dimensional boundaries agree, but `Gamma != Delta` as supplied generators. Therefore the statement/relation "alpha is coherent with beta" does not determine which 3-cell witnessed it.

**Seal: SAME WITNESS EQUIVALENCE != SAME COHERENCE WITNESS.**

This is intentionally a free finite computadic/globular specimen: distinct named generators remain distinct unless an additional higher relation identifies them. It does not claim a novel theorem.

## Delta

`PARALLEL-EQUIVALENCE-WITNESS-001` separates an equality/result from its 2-dimensional derivation witness. This slice repeats the hostile test one dimension higher: even source 2-cell + target 2-cell + the fact that a coherence exists do not reconstruct the supplied coherence witness.

The minimal receipt therefore has three separately addressable layers: (1) underlying paths/1-cells, (2) equality/rewrite witnesses/2-cells, and (3) coherence witnesses/3-cells. Quotienting a layer is permitted only by an explicit declared relation; it does not retroactively erase supplied lower-dimensional receipts.

## Documented mathematics

Higher-category theory replaces equations by higher morphisms/homotopies and then imposes coherence laws at the next dimension. Jurco, Saemann, Schreiber & Wolf (2019), DOI 10.1002/prop.201910001, describe this ladder explicitly: equations become homotopies and coherence concerns higher homotopies. Xantcha (2015), DOI 10.1112/jlms/jdv037, develops 2-quivers/quiver 2-categories with separately supplied relations, supporting the presentation-oriented boundary used here.

Scholar Gateway search performed 2026-09-20: 10 passages / 10 articles (2009-2026). Wolfram semantic lookup returned no direct computad result; its multiway documentation does independently distinguish branch pairs from their resolutions, which is only an analogy here, not evidence for the higher-category claim.

## Inference for Dogram

If Dogram ever retains a declaration that two derivation witnesses are equivalent, the declaration's witness should not be silently collapsed into the boolean fact of equivalence when provenance matters. Preserve the supplied higher cell or explicitly declare the quotient that forgets it.

## Refusal boundary

- `2-CELL != OCCURRENCE`
- `3-CELL != OCCURRENCE`
- `SAME 2-CELL BOUNDARY != SAME 3-CELL`
- `COHERENCE != EVIDENCE`
- `PARALLEL HIGHER CELLS != HISTORICAL ALTERNATIVES`
- `HIGHER-DIMENSIONAL RELATION != SEMANTIC TRUTH`
- `STRUCTURAL COMPOSITION != CAUSAL COMPOSITION`

## Reproduce

```bash
python research/parallel_coherence_witness_001.py
pytest -q tests/test_parallel_coherence_witness_001.py
```

The kernel is standard-library-only and exhaustive for this frozen finite generator set.

## Next hostile frontier

Do not climb dimensions merely because we can. The next earned test is *composition*: whisker/compose `Gamma` and `Delta` in a tiny strict 3-category and test whether distinct 3-dimensional factorizations can have the same composite and complete lower-dimensional boundary. If that collision survives, investigate interchange/coherence receipts before proposing any public higher-cell operator.
