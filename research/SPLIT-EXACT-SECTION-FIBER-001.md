# SPLIT-EXACT-SECTION-FIBER-001

## Status

Research-only bounded exact specimen. No public operator promotion.

## Frozen specimen

Work over `Q`.

Let `E = Q^2`, `Q0 = Q`, and define the surjective linear map

`T : E -> Q0`, `T(a,b)=a`.

Its kernel is exactly

`K = {(0,k) : k in Q}`.

For every scalar `c in Q`, define

`s_c(q)=(q,cq)`.

Then

`T(s_c(q)) = q`,

so every `s_c` is a linear right inverse / section of the same fixed quotient map.

For `c != d`,

`s_c(q)-s_d(q)=(0,(c-d)q) in K`.

Thus changing the section changes only the kernel component forgotten by `T`.

For the frozen input `q=3/2`:

- `s_0(q)=(3/2,0)`;
- `s_1(q)=(3/2,3/2)`;
- `s_2(q)=(3/2,3)`;

and all three project to exactly `3/2`.

## Exact-sequence reading

The specimen realizes the split short exact sequence

`0 -> K -> E -> Q0 -> 0`.

The quotient/projection is fixed. A section is additional data.

For this finite-dimensional specimen, all linear sections are exactly the family `s_c`: a linear section is determined by its value at `1`, and the right-inverse condition forces that value to be `(1,c)` for a unique `c`.

Equivalently, after choosing one base section `s_0`, every other linear section is

`s_0 + u`

with `u : Q0 -> K` linear. Hence the set of linear splittings is an affine family modeled on `Hom(Q0,K)`; there is no preferred origin supplied by the quotient map itself.

## Dogram seals

- `A QUOTIENT FORGETS THE KERNEL; A SPLITTING CHOOSES A COMPLEMENT.`
- `SECTION != CANONICAL SECTION.`
- `DIFFERENCE OF SECTIONS LANDS IN THE KERNEL.`
- `RECONSTRUCTION CHOICE IS EXTRA STRUCTURE.`
- `SAME QUOTIENT VALUE != SAME LIFT.`
- `RIGHT INVERSE != INVERSE.`

## Boundary / refusals

- `KERNEL COMPONENT != HIDDEN OCCURRENCE`.
- `CHOOSING A SECTION != RECOVERING HISTORY`.
- `SPLITTING != EVIDENCE`.
- `QUOTIENT CLASS != AUTHORITY CLASS`.
- `NONCANONICAL != ARBITRARY WITHOUT RECEIPT`; a chosen section may satisfy independently declared constraints.
- `ALGEBRAIC SPLITTING != TOPOLOGICAL/CONTINUOUS SPLITTING`; topology can add real obstructions and must be receipted separately.

## Relation to TAYLOR-MAP-FIBER-001

Borel's theorem supplies surjectivity of the smooth Taylor map, and flat germs form its kernel. This slice does **not** claim that the infinite-dimensional Taylor sequence has every stronger topological splitting property one might ask for. Instead it freezes the algebraic distinction in the smallest exact model where it can be recomputed exhaustively:

`quotient data + existence of lifts != canonical reconstruction rule`.

That distinction is the only promoted research conclusion.

## Literature basis

- Barostichi, Cordaro & Petronilho (2013), DOI `10.1002/mana.201200231`: classical Borel theorem as arbitrary formal Taylor data realizable by a smooth function; also treats the Borel map as a continuous linear map between Frechet spaces in its setting.
- Dierolf & Sieg (2012), DOI `10.1002/mana.201100325`: split short exact sequences as the minimal exact structure in additive categories and topological exactness in locally convex/Frechet settings.
- Jurco & Vysoky (2019), DOI `10.1002/prop.201910024`: explicit geometric examples where an exact sequence admits splittings and changing the splitting changes auxiliary data, illustrating that splitting is chosen structure rather than the quotient itself.
- Jimenez-Garrido, Sanz & Schindl (2020), DOI `10.1002/mana.201800465`: Borel-map surjectivity via existence of right inverses in ultraholomorphic classes, reinforcing the distinction between surjectivity and a selected extension operator.

No source is claimed to contain this exact `Q^2 -> Q` fixture or the Dogram interpretation.

## HOLD

No `quotient@1`, `kernel@1`, `section@1`, `split_exact@1`, `reconstruct@1`, `canonical_lift@1`, or authority/evidence semantics promotion.

## Next frontier

The finite-dimensional vector-space sequence always splits algebraically, so the next genuinely stronger frontier is to add topology or norm constraints and ask when a surjective map admits a **continuous/bounded** linear section. Candidate seal:

`ALGEBRAIC LIFT EXISTS != CONTINUOUS LIFT EXISTS.`

That frontier should be entered only with a bounded counterexample or a theorem-gated specimen; do not infer topological reconstruction from algebraic exactness.
