# BANACH-SECTION-OBSTRUCTION-001

## Status

Research-only theorem-gated specimen. No public operator promotion.

## Frozen sequence

Consider the Banach-space short exact sequence

`0 -> c0 -> l_infinity -> l_infinity/c0 -> 0`,

with canonical quotient map

`q : l_infinity -> l_infinity/c0`.

As a sequence of plain real vector spaces, it splits: every short exact sequence of vector spaces admits a linear section after choosing a complement/basis extension.

The stronger Banach-space question is different: does there exist a **bounded linear** section

`s : l_infinity/c0 -> l_infinity`

with

`q o s = id`?

## Exact obstruction implication

Assume such a bounded linear section `s` exists. Define

`P = I - s o q`.

Then for every `k in ker(q)=c0`,

`P(k)=k-s(q(k))=k`.

For every `x`,

`q(P(x))=q(x)-q(s(q(x)))=q(x)-q(x)=0`,

so `P(x)` lies in `c0`.

Therefore `P` is a bounded linear projection of `l_infinity` onto `c0`; equivalently, `c0` would be complemented in `l_infinity`.

Phillips' classical result says that `c0` is **not** complemented in `l_infinity`. Hence the assumed bounded linear section cannot exist.

Thus the same underlying exact sequence has the category delta

`ALGEBRAIC SECTION EXISTS`

but

`BOUNDED LINEAR SECTION DOES NOT EXIST`.

## Dogram seals

- `ALGEBRAIC LIFT EXISTS != BOUNDED LINEAR LIFT EXISTS.`
- `RECEIPT THE MORPHISM CLASS.`
- `A SECTION IN ONE CATEGORY NEED NOT BE A SECTION IN A STRONGER CATEGORY.`
- `SURJECTIVE CONTINUOUS LINEAR MAP != BOUNDEDLY SPLIT QUOTIENT.`
- `P = I - s q` IS THE OBSTRUCTION RECEIPT CONNECTING A RIGHT INVERSE TO COMPLEMENTABILITY.
- `THEOREM-GATED INFINITE CLAIM != FINITE COMPUTATIONAL PROOF.`

## Documented mathematics

1. **Algebraic splitting.** Short exact sequences of vector spaces split algebraically: a surjection admits a linear right inverse after choosing a vector-space complement / extending a basis.
2. **Section-complement equivalence in Banach spaces.** If a quotient `q : X -> X/Y` admits a bounded linear right inverse `s`, then `P=I-sq` is a bounded projection onto `Y`; conversely a bounded complement gives a bounded section. Thus bounded splitting is equivalent to complementability of the kernel.
3. **Phillips non-complementation.** The classical Phillips result gives that `c0` is not complemented in `l_infinity`, so the canonical quotient onto `l_infinity/c0` has no bounded linear section.
4. **Sobczyk contrast.** Sobczyk's theorem says every copy of `c0` in a separable Banach superspace is complemented (indeed with controlled projection norm). `l_infinity` is nonseparable, so the Phillips obstruction marks a real category/ambient-space boundary rather than a contradiction.

Useful sources:

- A. Sobczyk, *Projection of the space (m) on its subspace (c0)*, Bull. Amer. Math. Soc. 47 (1941), 938-947, DOI `10.1090/S0002-9904-1941-07593-2`.
- F. Cabello Sanchez, J. M. F. Castillo, D. Yost, *Sobczyk's Theorems from A to B*, Extracta Mathematicae 15 (2000), 391-420; explicitly contrasts the separable complementability theorem with `c0` not complemented in `l_infinity`.
- A. Molto, *On a theorem of Sobczyk*, Bull. Australian Math. Soc. (2009); notes an easy proof of the Phillips result and discusses the nonseparable boundary.
- F. Cabello Sanchez and J. M. F. Castillo, *Complemented Subspaces of Banach Spaces*, in *Homological Methods in Banach Space Theory* (Cambridge, 2023), DOI `10.1017/9781108778312.003`.

No source is claimed to contain Dogram's exact theorem-gated receipt structure.

## Inference

For Dogram, the durable architectural inference is that **the admissible morphism class is part of the mathematical input**. A reconstruction/lift valid after forgetting topology may disappear when continuity or boundedness is required.

This supports the general receipt law:

`SAME OBJECTS + SAME SET MAP + STRONGER MORPHISM CONTRACT CAN CHANGE EXISTENCE.`

It does not license calling one category more true than another.

## Boundary / refusals

- `ALGEBRAIC SECTION != PHYSICALLY REALIZABLE LIFT`.
- `BOUNDED SECTION != EVIDENCE`.
- `UNCOMPLEMENTED != HIDDEN OCCURRENCE`.
- `TOPOLOGICAL OBSTRUCTION != CAUSAL OBSTRUCTION`.
- `NONSEPARABLE != UNOBSERVABLE`.
- `NO BOUNDED LINEAR SECTION != NO SET-THEORETIC SECTION`.
- `NO BOUNDED LINEAR SECTION != NO NONLINEAR CONTINUOUS SECTION` unless separately proved.
- `CATEGORY DELTA != TRUTH DELTA`.

## Executable boundary

The kernel deliberately does **not** fake a finite proof of Phillips' infinite-dimensional theorem. It only:

- replays the exact identity `P=I-sq` and why a bounded section implies a bounded projection onto the kernel;
- refuses the algebraic-splitting conclusion unless the vector-space splitting theorem is explicitly declared;
- refuses the bounded-nonsplitting conclusion unless Phillips non-complementation is explicitly declared;
- records the resulting category delta once both theorem bases are supplied.

## HOLD

No `banach@1`, `bounded_section@1`, `complemented@1`, `quotient@1`, `topological_split@1`, `reconstruct@1`, or evidence/authority semantics promotion.

## Next frontier

The stronger next question is quantitative rather than merely existential: finite-dimensional quotients always admit bounded linear sections, but the **best section/projection norm can depend strongly on the geometry and dimension**. A bounded family whose optimal projection constants diverge would separate

`SECTION EXISTS FOR EACH FINITE SPECIMEN`

from

`UNIFORM BOUND EXISTS ACROSS THE FAMILY`.

Candidate seal:

`POINTWISE EXISTENCE != UNIFORM CONTROL. KEEP THE CONSTANT IN THE RECEIPT.`
