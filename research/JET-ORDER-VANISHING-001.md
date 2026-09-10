# JET-ORDER-VANISHING-001

Status: bounded research specimen; no public operator promotion.

## Question

Can two degenerate critical germs agree on a declared low-order jet while differing at the first order where any local Taylor information appears, and what survives an explicitly declared local reparameterization?

## Frozen specimen

At zero, compare

- `f(x)=x^3`;
- `g(x)=x^4`.

Their complete declared 2-jets agree:

`j^2 f(0) = j^2 g(0) = (0,0,0)`.

Thus value, gradient, and Hessian all collide at the declared decoder depth.

But the first nonzero derivative orders differ:

- `ord_0(f)=3`, with `f'''(0)=6`;
- `ord_0(g)=4`, with `g''''(0)=24`.

Core seal:

`SAME DECLARED k-JET != SAME HIGHER-ORDER GERM.`

More specifically:

`SAME VALUE + SAME GRADIENT + SAME HESSIAN CAN HIDE DIFFERENT FIRST NONZERO JET ORDERS.`

## Coordinate hostile control

Declare the local coordinate germ

`phi(z)=2z+z^2`.

It fixes zero and has `phi'(0)=2 != 0`, so it is locally invertible at zero.

Exact finite composition gives

`f(phi(z)) = 8z^3 + 12z^4 + 6z^5 + z^6`,

`g(phi(z)) = 16z^4 + 32z^5 + 24z^6 + 8z^7 + z^8`.

Therefore the first nonzero orders remain exactly `3` and `4`, while the raw leading derivatives change:

- `(f o phi)'''(0)=48 = 6 * 2^3`;
- `(g o phi)''''(0)=384 = 24 * 2^4`.

This isolates the distinction:

`ORDER OF VANISHING SURVIVES THIS LOCAL DIFFEOMORPHISM; RAW LEADING DERIVATIVE MAGNITUDE DOES NOT.`

The kernel explicitly refuses a coordinate map whose linear coefficient vanishes; that case is not a local diffeomorphism and can change order by ramification (for example `x^3 o z^2 = z^6`).

## Documented mathematics

This slice uses standard jet/germ and singularity-theory mathematics.

- Nguyen, Ruas & Trivedi, *Proceedings of the London Mathematical Society* 121 (2020), DOI `10.1112/plms.12310`, define smooth function germs, diffeomorphism-germ right equivalence, k-jets, and finite determinacy; their classification framework also treats the lowest-degree homogeneous part as an invariant in the stated equivalence setting.
- Liu et al., *Complexity* (2021), DOI `10.1155/2021/6695461`, explicitly define the k-jet as Taylor expansion through degree k and identify the lowest nonzero homogeneous degree as the multiplicity/order datum used in function-germ classification.
- Brodersen, *Proceedings of the London Mathematical Society* 75, DOI `10.1112/S0024611597000397`, defines finite determinacy by equality of sufficiently high finite jets followed by equivalence, which is precisely why equality of an arbitrarily chosen low-order jet is not silently promoted to germ equivalence.

No cited source is claimed to contain this exact frozen `x^3` / `x^4` fixture.

## Dogram inference

For Dogram, a truncated derivative surface is a declared probe depth. A collision at depth `k` says only that the probe retained no separating information through that order. It does not license identity, equivalence, occurrence, causation, or evidence claims.

Durable candidate mathals:

- `KEEP THE JET ORDER IN THE RECEIPT.`
- `SAME k-JET != SAME GERM.`
- `FIRST NONZERO ORDER CAN SURVIVE A LOCAL REPARAMETERIZATION WHILE ITS RAW COEFFICIENT MOVES.`
- `A DECODER THAT STOPS BEFORE THE FIRST NONZERO TERM HAS NOT OBSERVED THE SINGULARITY ORDER.`

## Refusals

- `JET COLLISION != OCCURRENCE IDENTITY`.
- `HIGHER ORDER != MORE TRUE`.
- `MULTIPLICITY != IMPORTANCE`.
- `SINGULARITY TYPE != CAUSAL TYPE`.
- `LOCAL DIFFEOMORPHISM != HISTORICAL TRANSFORMATION`.
- `COORDINATE-INVARIANT ORDER != EVIDENCE INVARIANT`.
- `FINITE DETERMINACY != AUTOMATICALLY ESTABLISHED`.
- `SAME TRUNCATED JET != RIGHT EQUIVALENCE` unless a separate determinacy theorem and its hypotheses are actually supplied.

## Verification

All fixture arithmetic is finite and exact. The kernel uses only Python stdlib `Fraction` and integer factorials; polynomial composition is recomputed from the frozen coefficient lists.

Wolfram was attempted as an independent symbolic verifier during the research pass but returned an upstream 502. No Wolfram-verification claim is made.

## HOLD

Do not promote `jet@1`, `germ@1`, `multiplicity@1`, `singularity@1`, `finite_determinacy@1`, `right_equivalence@1`, or automatic reparameterization/equivalence inference.

## Next frontier

The next meaningful pressure test is not merely order 5. It is **finite determinacy versus infinite flat residue** in the smooth category: construct two `C-infinity` germs with every finite derivative equal at zero while differing away from zero, e.g. zero versus a flat germ such as `exp(-1/x^2)` extended by zero. That would separate

`SAME ALL FINITE JETS AT A POINT`

from

`SAME LOCAL FUNCTION GERM`

while forcing the receipt to distinguish analytic from smooth categories. The candidate seal is:

`THE INFINITE TAYLOR RECEIPT CAN STILL MISS A SMOOTH FLAT RESIDUE. RECEIPT THE REGULARITY CATEGORY.`
