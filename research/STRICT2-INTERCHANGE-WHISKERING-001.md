# STRICT2-INTERCHANGE-WHISKERING-001

Status: research-only / HOLD for public operator promotion.

## Question

Can four individually typed 2-cells admit two legal pasting orders whose equality depends on retaining the crossed-module action/whiskering term?

Yes. A finite exact specimen exists in the identity crossed module `S3 -> S3`.

## Documented mathematics

A crossed module consists of groups `H,G`, a boundary homomorphism `t:H->G`, and a `G`-action on `H` satisfying equivariance and the Peiffer identity. It determines a strict 2-group. In the standard semidirect-product presentation,

`(h,g) tensor (k,l) = (h * (g action k), g*l)`

and vertical composition is multiplication in `H` when source/target typing matches. The Peiffer condition is what makes horizontal and vertical composition satisfy the interchange law.

Relevant literature:

- Baez and Lauda, *Higher-Dimensional Algebra V: 2-Groups*, Theory and Applications of Categories 12 (2004), 423-491, arXiv:math/0307200.
- Porst, *Strict 2-Groups are Crossed Modules* (2008), explicit 2-equivalence between strict 2-groups and crossed modules.
- Recent explicit formulas appear in *Duality in monoidal categories*, Mathematische Zeitschrift (2026), DOI `10.1007/s00209-026-03983-z`, Remark 5.23.
- The role of the Peiffer condition in crossed-module/internal-category structure is treated in Mantovani and Metere (2010), *Theory and Applications of Categories*.

## Frozen crossed module

Use

- `H = S3`;
- `G = S3`;
- `t = id`;
- `G` acts on `H` by conjugation.

This is a crossed module because

`t(g h g^-1) = g t(h) g^-1`

and

`t(h1) action h2 = h1 h2 h1^-1`.

A 2-cell `(h,g)` has source `g` and target `h g`.

Composition convention in the executable fixture: `compose(left,right)` means apply `right` first, then `left`.

## Frozen four-cell specimen

Let

`a=(12)`, `b=(23)`, `e=id`.

Choose

- left-bottom: `(a,e) : e -> a`;
- left-top: `(e,a) : a -> a`;
- right-bottom: `(e,e) : e -> e`;
- right-top: `(b,e) : e -> b`.

Both vertical columns are typed.

### Route A: vertical, then horizontal

Vertical composition gives

- left column: `(a,e)`;
- right column: `(b,e)`.

Horizontal composition uses the action of the left source `e`, so the higher label is

`a * (e action b) = ab = (123)`.

### Route B: horizontal, then vertical

The lower horizontal composite is `(a,e)`.

For the upper horizontal composite the right-top label must be whiskered by the left-top source `a`:

`a action b = a b a^-1 = (13)`.

Thus the upper horizontal higher label is `(13)`, based at source `a`. Vertical composition with the lower row gives

`(13) * (12) = ab = (123)`.

Therefore the lawful strict-2-group interchange closes exactly:

`vertical-then-horizontal = horizontal-then-vertical = (123)`.

## Hostile actionless control

Now illegally replace horizontal semidirect composition by a direct-product rule that simply multiplies the two `H` labels and ignores the `G`-action.

The four individual cells remain the same and both pasting routes remain syntactically type-compatible in this frozen specimen.

But:

- naive vertical-then-horizontal gives `ab=(123)`;
- naive horizontal-then-vertical gives `ba=(132)`.

So the naive interchange residual is nonzero solely because the required whiskering/action was omitted.

This is stronger than merely observing that an action-sensitive horizontal product exists. It shows that the action term is required for a higher coherence law to be checkable and true.

## Dogram inference

Keeper:

> KEEP THE ACTION THAT MAKES THE SQUARE COMMUTE.

Bounded stronger form:

> SAME FOUR CELLS + SAME TYPING != SAME PASTING RESULT UNDER AN ILLEGAL COMPOSITION LAW.

And:

> INTERCHANGE IS A RECEIPT ABOUT TYPED COMPOSITION, NOT A LICENSE TO DROP WHISKERING.

The operative Dogram lesson is that individual receipts can be locally typed yet still be insufficient for multiway composition if the comparison drops the action/whiskering law that transports one higher label into the frame in which composition occurs.

## Refusals

- `INTERCHANGE CLOSURE != HISTORICAL OCCURRENCE`.
- `WHISKERING != CAUSAL TRANSPORT`.
- `G ACTION != REAL-WORLD ACTION`.
- `STRICT-2-GROUP COHERENCE != EVIDENCE`.
- `NONZERO NAIVE RESIDUAL != PHYSICAL DEFECT`.
- `ALGEBRAIC CLOSURE != TRUTH`.

## Runtime verdict

Research kernel only. No public Dogram dispatch or schema change.

Explicit HOLD:

- `interchange@1`
- `whisker@1`
- `strict2@1`
- `crossed_module@1`
- `2cell@1`

## Next frontier

The next non-redundant target is no longer another strict interchange example. The stronger frontier is to weaken strictness itself: find the smallest finite bicategorical/weak-2-group specimen where the two pasting routes do not agree literally but are related by an explicit associator or coherence 2-isomorphism. That would distinguish

`STRICT EQUALITY`

from

`COHERENT EQUIVALENCE WITH A RECEIPTED WITNESS`

without treating either as occurrence, evidence, or meaning.
