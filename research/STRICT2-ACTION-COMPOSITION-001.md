# STRICT2-ACTION-COMPOSITION-001

Status: research-only / HOLD for public operator promotion.

## Question

Can two finite higher-composition specimens preserve the same outer 1-dimensional product and the same higher labels while differing only because the declared 1-dimensional action context changes the legal 2-dimensional composition?

Yes, in a minimal finite strict-2-group specimen.

## Documented mathematics

A crossed module `(G,H,t,alpha)` consists of groups `G,H`, a homomorphism `t:H->G`, and an action of `G` on `H` by automorphisms satisfying equivariance and the Peiffer identity. A crossed module determines a strict 2-group. In the standard semidirect-product presentation, horizontal/tensor composition is

`(h,g) tensor (h',g') = (h * alpha(g,h'), g*g')`.

See:

- John C. Baez and Aaron D. Lauda, *Higher-Dimensional Algebra V: 2-Groups*, Theory and Applications of Categories 12 (2004), 423-491, arXiv:math/0307200.
- *Duality in monoidal categories*, Mathematische Zeitschrift (2026), DOI `10.1007/s00209-026-03983-z`, Definition 5.22 and Remark 5.23, which state the crossed-module axioms and the strict-2-group tensor formula explicitly.

## Frozen crossed module

Use additive notation:

- `H = Z/3Z`;
- `G = Z/2Z`;
- `t(h)=0` for every `h`;
- `0 in G` acts identically on `H`;
- `1 in G` acts by inversion: `h -> -h mod 3`.

This is a crossed module:

1. The action is by automorphisms of `Z/3Z`.
2. Boundary equivariance is automatic because `t` is trivial and `G` is abelian.
3. The Peiffer condition reduces to `h' = h+h'-h`, because `t(h)=0` acts trivially and `H` is abelian.

No physical, causal, semantic, or historical interpretation is attached to these groups.

## Exact hostile pair

Hold the higher labels fixed:

`h_left = h_right = 1 in Z/3Z`.

Hold the total outer `G` product fixed at zero, but change the internal factorization.

### Control A: even factorization

`g_left=0`, `g_right=0`.

The declared horizontal composite is

`1 + (0 action 1) = 1 + 1 = 2 mod 3`,

and the outer product is

`0+0=0 mod 2`.

### Control B: odd factorization

`g_left=1`, `g_right=1`.

The declared action sends the right label `1` to `-1=2 mod 3`, so

`1 + (1 action 1) = 1 + 2 = 0 mod 3`,

while the outer product remains

`1+1=0 mod 2`.

Therefore

`SAME OUTER G PRODUCT + SAME H LABELS != SAME STRICT-2-GROUP H COMPOSITE`.

The exact higher-composite delta, using `odd-even mod 3`, is

`0-2 = 1 mod 3`.

## Hostile naive control

If the action is illegally discarded and the two `H` labels are composed as a direct product/additive sum, both cases return

`1+1=2 mod 3`.

That calculation erases the actual semidirect-product distinction.

Keeper:

> THE ACTION CONTEXT IS PART OF THE COMPOSITION RECEIPT.

Stronger bounded form:

> DO NOT REPLACE A SEMIDIRECT PRODUCT WITH A DIRECT PRODUCT BECAUSE THE OUTER PRODUCT AGREES.

## Dogram inference

The result is not merely that a higher cell can carry an extra label. The *law of composition itself* consumes lower-dimensional context.

This extends the previous face-lift frontier:

`same boundary image -> possibly different higher lifts -> higher lifts themselves compose using declared lower-dimensional action`.

Thus an endpoint-only or outer-boundary-only receipt can be insufficient even when every individual higher label is preserved.

## Refusals

- `HIGHER COMPOSITE != HISTORICAL OCCURRENCE`.
- `G ACTION != CAUSAL ACTION`.
- `SEMIDIRECT PRODUCT != MECHANISM`.
- `SAME OUTER PRODUCT != SEMANTIC EQUIVALENCE`.
- `DIFFERENT 2-COMPOSITES != DIFFERENT REAL-WORLD EVENTS`.
- `STRICT-2-GROUP COHERENCE != TRUTH`.

## Runtime verdict

Research kernel only. No public Dogram dispatch or schema change.

Explicit HOLD:

- `strict2@1`
- `horizontal_compose@1`
- `crossed_module@1`
- `semidirect@1`
- `interchange@1`

## Next frontier

The next non-redundant target is an exact **interchange-law / two-way pasting** specimen: four 2-cells with both horizontal and vertical composition available, where a naive bookkeeping scheme loses the action/whiskering needed for the two legal pasting orders to agree. The goal would be a receipt showing what data must be retained for interchange to be checkable, not merely another example of action-sensitive multiplication.
