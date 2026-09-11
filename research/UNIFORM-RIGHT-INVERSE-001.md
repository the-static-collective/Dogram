# UNIFORM-RIGHT-INVERSE-001

Status: research-only / no public operator promotion

## Question

Can every member of a normalized finite-dimensional family admit a bounded linear right inverse while no single operator-norm bound works uniformly across the family?

Yes.

## Frozen family

For every integer `n >= 1`, equip the domain and codomain with Euclidean norms and define

`A_n : R^3 -> R^2`

by

`A_n(x,y,z) = (x, y/n)`.

Its nonzero singular values are exactly `1` and `1/n`, hence

`||A_n||_2 = 1`

for every `n`.  The forward family is therefore normalized in operator norm.

A canonical linear section is

`S_n(u,v) = (u, n v, 0)`.

Direct substitution gives

`A_n S_n = I_(R^2)`.

Thus every family member has a bounded linear right inverse.

## Exact lower bound for every right inverse

Let `S` be any linear right inverse of `A_n` and let `e_2=(0,1)`.
Write

`S(e_2)=(a,b,c)`.

Since `A_n S(e_2)=e_2`, the second coordinate forces

`b/n = 1`, hence `b=n`.

Therefore

`||S||_2 >= ||S(e_2)||_2 >= n`.

The canonical `S_n` has singular values `1` and `n`, so

`||S_n||_2=n`.

Therefore the best possible right-inverse norm is exactly

`inf{||S||_2 : A_n S = I} = n = 1/sigma_min(A_n)`.

## Uniform-control failure

Every `n` has a bounded section, but the optimal constants are

`1,2,3,...`.

For any proposed finite bound `C`, choose an integer `n>C` (the executable kernel uses `floor(C)+1`, with the obvious `n=1` control below one). Then every right inverse of `A_n` has norm strictly larger than `C`.

Hence

`FOR ALL n EXISTS bounded S_n`

but not

`EXISTS C FOR ALL n EXISTS S_n with ||S_n|| <= C`.

Core seals:

- `POINTWISE BOUNDED SECTION EXISTS != UNIFORMLY BOUNDED FAMILY OF SECTIONS EXISTS.`
- `KEEP THE CONDITIONING CONSTANT IN THE RECEIPT.`
- `NORMALIZED FORWARD OPERATOR NORM != UNIFORM INVERSE CONTROL.`
- `FOR EVERY PROPOSED BOUND C, AN EXPLICIT PARAMETER n>C DEFEATS IT.`

## Literature basis

The linear-algebra substrate is standard. For a matrix with singular values `sigma_1 >= ... >= sigma_r > 0`, the Moore-Penrose pseudoinverse replaces the nonzero singular values by their reciprocals and has spectral norm `1/sigma_r`; see Kilicman, Al-Zhour & Domoshnitsky (2011), DOI `10.1155/2011/536935`. For a full-row-rank (surjective) matrix, `A A^dagger = I`, so the pseudoinverse is a right inverse; Zhou & Soleymani (2014), DOI `10.1155/2014/498016`, state this explicitly. Auras et al. (2024), DOI `10.1002/gamm.202470003`, describe finite-dimensional inverse ill-conditioning by the ratio of largest to smallest singular value and the reciprocal singular factors appearing in the pseudoinverse. Osinsky (2023), DOI `10.1002/nla.2525`, gives explicit epsilon-families whose pseudoinverse norms scale like inverse powers of a small singular parameter.

No source is claimed to contain this exact `R^3 -> R^2` Dogram fixture or its receipt language.

## Relation to BANACH-SECTION-OBSTRUCTION-001 (#97)

#97 is an existence/nonexistence boundary in the Banach category: an algebraic section may exist while no bounded linear section exists.

This slice is deliberately different. Every map here is finite-dimensional and has bounded sections. The delta is quantitative and uniform:

`SECTION EXISTS AT EACH PARAMETER != ONE CONSTANT CONTROLS ALL SECTIONS ACROSS THE FAMILY.`

This finite family does **not** prove, approximate, or explain Phillips' theorem by itself. It only freezes the separate mathematical distinction between pointwise existence and uniform norm control.

## Executable boundary

The stdlib-only kernel uses exact `Fraction` arithmetic. It:

- applies `A_n` and the canonical section exactly;
- records the singular-value/operator-norm formulas for the frozen diagonal family;
- receipts the basis-vector lower-bound witness forcing every right inverse to have norm at least `n`;
- records attainment by the canonical section;
- constructs an explicit `n` defeating any supplied rational uniform bound.

The kernel does not implement a general SVD, generalized-inverse package, Banach-space engine, optimizer, evidence model, or authority model.

## Refusals

- `LARGE SECTION NORM != LARGE EVIDENCE`.
- `ILL-CONDITIONED != FALSE`.
- `UNIFORM BOUND FAILURE != OCCURRENCE FAILURE`.
- `PARAMETER LIMIT != HISTORICAL LIMIT`.
- `RIGHT-INVERSE COST != AUTHORITY WEIGHT`.
- `SMALL SINGULAR VALUE != LOW TRUTH`.
- `NUMERICAL INSTABILITY != CAUSAL INSTABILITY`.
- `FINITE-DIMENSIONAL BLOWUP != PROOF OF INFINITE-DIMENSIONAL NONCOMPLEMENTATION`.

## HOLD

No `condition_number@1`, `uniform_section@1`, `right_inverse@1`, `pseudoinverse@1`, `stability@1`, `ill_conditioned@1`, or reconstruction-policy promotion.

## Next frontier

The live next distinction is perturbative rather than existential:

`SMALL FORWARD-OPERATOR DELTA != SMALL RIGHT-INVERSE DELTA NEAR RANK LOSS.`

For example, compare neighboring normalized maps whose smallest singular value approaches zero and receipt how inverse sensitivity scales. A stronger version would distinguish pointwise continuity on the fixed-rank stratum from failure of uniform continuity as rank loss is approached.

Candidate seal:

`KEEP THE DISTANCE TO SINGULARITY IN THE RECEIPT.`
