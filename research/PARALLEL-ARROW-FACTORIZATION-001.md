# PARALLEL-ARROW-FACTORIZATION-001

## Question

After `FACTORIZATION-PATH-001`, can the factorization residual survive even when the **entire object sequence is held fixed** and neither path uses an identity arrow?

Yes.

## Frozen specimen

Use the one-object groupoid `B(V4)` of the Klein four group

`V4 = {(0,0),(1,0),(0,1),(1,1)}`

with componentwise addition modulo 2. Let

- `e=(0,0)`
- `a=(1,0)`
- `b=(0,1)`.

Every arrow has source and target `X`, so both length-two paths have the same object sequence

`X -> X -> X`.

Compare:

- path A: `(a,a)`
- path B: `(b,b)`.

Both supplied arrows are nonidentity and

`a∘a=e=b∘b`,

but `(a,a) != (b,b)`.

Therefore

**SAME OBJECTS + SAME COMPOSITE != SAME ARROW FACTORIZATION.**

The delta cannot be attributed to endpoints, intermediate objects, path length, or identity padding. It is arrow-level path data.

## Documented mathematics

This is ordinary finite group/category mathematics. A group is a one-object groupoid; a free/path category retains composable arrow strings before any equations identify their composites. Poinsot & Caenepeel (2013), DOI `10.1155/2013/370618`, explicitly construct free categories from directed graphs with morphisms given by finite composable paths and distinguish those paths from their image under a composition functor. Their locally finite-category treatment also counts distinct factorizations of a single arrow.

Wolfram's `AbstractCategory` documentation independently exposes the same structural distinction: morphism associations can contain parallel morphisms and composite morphisms, while explicit morphism equivalences are additional declared data rather than consequences of sharing endpoints.

## Dogram inference

If a receipt needs supplied factorization provenance, object sequence plus composite is insufficient. Preserve the ordered arrow path, or preserve an explicitly declared quotient/equivalence of paths.

This does **not** yet justify a public 2-cell operator. It only earns the next question: when two parallel paths are deliberately identified by a declared relation, what receipt must survive that identification?

## Refusal boundary

- `ARROW != OCCURRENCE`
- `PATH != HISTORICAL PATH`
- `SAME COMPOSITE != SAME PROVENANCE`
- `SAME OBJECT SEQUENCE != SAME ARROW SEQUENCE`
- `STRUCTURAL LOOP != CAUSAL LOOP`
- `ALGEBRAIC EQUALITY != EVIDENTIARY EQUALITY`

## Reproduction

```bash
python research/parallel_arrow_factorization_001.py
pytest -q tests/test_parallel_arrow_factorization_001.py
```

The kernel uses only Python's standard library and exact mod-2 arithmetic.
