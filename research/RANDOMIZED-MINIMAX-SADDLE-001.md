# RANDOMIZED-MINIMAX-SADDLE-001

Status: bounded research slice. No public operator promotion.

## Question

Does the robust minimax value of a frozen finite decision problem depend only on its pure policy cost table and declared ambiguity set, or also on the admissible policy class?

## Frozen carrier

States: `s1,s2,s3`.

Pure state-cost vectors:

- `A=(2,2,7)`
- `B=(1,7,1)`
- `C=(5,5,1)`

Declared ambiguity polytope: convex hull of

- `p1=(3/5,1/5,1/5)`
- `p2=(1/5,3/5,1/5)`
- `p3=(1/5,1/5,3/5)`.

Expected cost is the exact affine pairing `R_pi(a)=pi dot c_a`. Therefore its maximum over the declared convex hull is attained at a vertex; the kernel receipts those declared vertices rather than inventing a prior.

## Pure-policy minimax

Expected costs at `(p1,p2,p3)` are:

- `A=(3,3,5)`, so `max A=5`;
- `B=(11/5,23/5,11/5)`, so `max B=23/5`;
- `C=(21/5,21/5,13/5)`, so `max C=21/5`.

Restricting admissible policies to the three pure rules therefore gives unique minimax policy `C` with value

`V_pure = 21/5`.

## Convexified policy class

Now change only the admissible policy class by permitting a declared randomized mixture of the same pure rules:

`m = (4/9) A + 0 B + (5/9) C`.

Its state-cost vector is exactly

`c_m=(11/3,11/3,11/3)`.

Hence its expected cost is `11/3` under every prior, including every point of the declared ambiguity polytope. This gives

`V_mixed <= 11/3`.

## Exact least-favorable witness

Declare

`pi*=(2/9,4/9,1/3)`.

It lies inside the ambiguity triangle with exact barycentric coordinates

`(1/18,11/18,1/3)`

relative to `(p1,p2,p3)`.

At `pi*`, all three pure policies tie:

`R_pi*(A)=R_pi*(B)=R_pi*(C)=11/3`.

Every randomized mixture of those policies therefore also has expected cost `11/3` at this same prior. Thus

`V_mixed >= 11/3`.

Combining the bounds closes an exact saddle:

`V_mixed = 11/3`.

The pure restriction creates a strict minimax gap

`21/5 - 11/3 = 8/15`.

## Delta

`SAME STATES + SAME PURE POLICY COST TABLE + SAME PRIOR AMBIGUITY SET != SAME MINIMAX VALUE AFTER CHANGING THE ADMISSIBLE POLICY CLASS.`

The only mathematical contract change is that convex mixtures of the already-declared pure policies become admissible.

## Earned mathals

- `ADMISSIBLE POLICY CLASS IS PART OF THE RECEIPT.`
- `CONVEXIFYING THE POLICY CLASS CAN CLOSE A MINIMAX GAP WITHOUT CHANGING THE STATE COST TABLE.`
- `A LEAST-FAVORABLE PRIOR IS A GAME WITNESS, NOT AN OCCURRENCE DISTRIBUTION.`
- `SADDLE CLOSURE RECEIPTS AN OPTIMIZATION EQUILIBRIUM; IT DOES NOT PROMOTE A POLICY.`

## Documented mathematics

This specimen sits inside classical statistical decision theory / zero-sum convex decision geometry.

- Hansen & Sargent (2023), *Journal of Applied Econometrics*, DOI `10.1002/jae.3010`: randomized decisions generate convex combinations of the acts induced by pure decisions. This supports treating policy randomization as an explicit enlargement/convexification of the admissible act class.
- Chamberlain (2001), *Journal of Applied Econometrics*, DOI `10.1002/jae.583`: minimax decision rules over a finite uncertainty family can be obtained through a least-favorable mixture/distribution, and a minimax rule is Bayes with respect to that least-favorable distribution.
- Andrews & Shapiro (2021), *Econometrica*, DOI `10.3982/ECTA18155`: robust Bayes/minimax criteria over convex classes of priors and minimax-theorem conditions are treated explicitly.

No claim is made that those papers contain this exact three-state fixture or the Dogram interpretation below.

## Dogram inference

For this frozen finite specimen, the minimax receipt is incomplete if it names the cost table and prior set but omits whether only pure policies or their convex mixtures were admissible. That is a decoder/optimization-contract delta, not an evidence or occurrence delta.

## Refusals

- `RANDOMIZED POLICY != HISTORICAL RANDOMNESS`.
- `LOWER MINIMAX VALUE != MORE TRUE`.
- `LEAST-FAVORABLE PRIOR != OCCURRENCE FREQUENCY`.
- `LEAST-FAVORABLE PRIOR != EVIDENCE`.
- `SADDLE POINT != AUTHORITY`.
- `CONVEXIFICATION != EVIDENCE EXPANSION`.
- `MIXED STRATEGY != REAL-WORLD MIXTURE` unless separately declared and sourced.
- `OPTIMAL UNDER DECLARED GAME != CANONICAL POLICY`.

## Verification / provenance

All arithmetic is exact `fractions.Fraction` arithmetic. The fixture and focused tests precede the production kernel in branch history.

Test-only head `af7574e4d6c4d5d743bdefce6bec64eea9ec913a` produced Dogram CI #544 RED at unit-test import with the expected `ModuleNotFoundError` before `dogram.randomized_minimax_saddle` existed.

Kernel head `9c4d697ff5bfd0124c229d71aa8739416dbfcd32` produced Dogram CI #545 GREEN.

Wolfram was attempted as an independent symbolic check but its connector returned an upstream 404, so no Wolfram-verification claim is made.

## HOLD

No `randomize@1`, `minimax@1`, `least_favorable_prior@1`, `saddle@1`, `policy_class@1`, `game@1`, or automatic policy chooser is promoted.

## Next frontier

The immediate geometry is now explicit enough to ask a sharper question: when the admissible policy class and ambiguity set are both convex, which parts of a saddle receipt are invariant under different finite generating sets for the same convex hull?

Candidate seal:

`GENERATORS ARE A PRESENTATION; THE CONVEX HULL IS THE DECLARED FEASIBLE GEOMETRY — RECEIPT WHICH ONE THE CALCULATION CONSUMED.`
