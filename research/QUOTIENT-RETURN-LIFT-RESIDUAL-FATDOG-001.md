# QUOTIENT-RETURN / LIFT-RESIDUAL FATDOG-001

**Date:** 2026-08-31  
**Status:** RESEARCH + EXACT FINITE/GEOMETRIC PRESSURE · NO NEW PUBLIC OPERATOR  
**Runtime authority:** NONE  
**Parent surfaces:** `PRODUCTIVE-DESYNC-001`, `TRANSVERSE-GENERATORS-001`, `OMEGA-CYCLE-001`, `EXECUTION-CUT / OMEGA-QUOTIENT`, `PHASELIFT-FLOW-GAP`, `PLJ-TRIADIC-SCREW-ORTHOGONAL-LIFT-001`, `MADDDOGCLOWN-REPLAY-001`

> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**

---

## 0. Seed

The research question is:

> **When a bounded path closes under a declared quotient, what nontrivial lift or residual can remain in the finer carrier?**

The first correction is immediate:

```text
RETURN IS NOT A BOOLEAN.
```

A return is always return **under some declared relation**.

At minimum it depends on:

```text
anchor
path
quotient / decoder / target family
finer carrier cut
```

This packet does not claim that all quotient returns are instances of one physical mechanism. It records a shared calculation grammar across several independent Dogram specimens.

---

# 1 — RETURN-IS-A-RELATION-001

Let

```math
\pi:X\to Q
```

be a declared quotient, decoder, projection, or target map.

Let a bounded path be

```math
a \xrightarrow{\gamma} b.
```

Define a quotient-return by

```math
\boxed{
\operatorname{RETURN}_{\pi}(a,\gamma,b)
\iff
\pi(a)=\pi(b).
}
```

This does **not** imply

```math
a=b.
```

Therefore:

```text
EXACT RETURN
!=
QUOTIENT RETURN
```

Candidate seal:

> **RETURN MUST NAME WHAT IT RETURNED TO.**

## 1.1 Exact return

```math
b=a.
```

This is the strongest ordinary state-level return in the declared carrier.

## 1.2 Quotient return

```math
\pi(b)=\pi(a)
```

while possibly

```math
b\ne a.
```

The quotient closed. The finer carrier may remain open.

## 1.3 Path return

Even when endpoints are identical,

```math
a=b,
```

formation history can differ.

Existing Dogram law already preserves:

```text
SAME ENDPOINT != SAME APPROACH HISTORY
SAME RESULT != SAME EXECUTION
SAME SURFACE != SAME HISTORY
```

So exact endpoint return still does not imply history return.

---

# 2 — RETURN-REFINEMENT-001

Suppose two quotients are properly nested:

```math
\pi_c = f\circ \pi_f
```

where `pi_f` is finer and `pi_c` is coarser.

Then:

```math
\pi_f(a)=\pi_f(b)
\Rightarrow
\pi_c(a)=\pi_c(b).
```

So:

> **FINE RETURN IMPLIES COARSE RETURN.**

But the converse need not hold.

```math
\pi_c(a)=\pi_c(b)
\not\Rightarrow
\pi_f(a)=\pi_f(b).
```

Therefore a lawful return spectrum is monotone under quotient refinement:

```text
coarse return can break when more structure is retained
fine return cannot fail only because less structure is retained
```

Hard boundary:

```text
arbitrary unrelated decoders
!=
nested quotient refinement
```

Do not infer monotonicity unless the factorization relation is declared.

---

# 3 — RETURN-SPECTRUM-001

For one bounded history `gamma`, carry a finite declared family of return relations:

```text
phase_return
sheet_return
target_return
endpoint_return
execution_return
history_return
```

These are not automatically ordered unless their quotient relations are explicitly nested.

A specimen may lawfully report:

```text
phase_return     true
sheet_return     true
endpoint_return  false
history_return   false
```

or:

```text
target_return    true
execution_return false
```

The point is not to build one universal hierarchy. The point is to stop one Boolean `returned` field from silently standing in for several inequivalent predicates.

Candidate seal:

> **RETURN HAS A SPECTRUM OF CUTS.**

---

# 4 — PLJ QUOTIENT RETURN

The exact PLJ carrier is

```math
T(x)=Rx+h e_z,
```

where `R` is rotation by `2*pi/3` around the `z` axis.

For

```math
P_0=(r,0,0),
```

one triadic cycle is

```text
P_0 -> L_0 -> J_0 -> P_1
```

with

```math
P_1=P_0+3h e_z.
```

Under the `XY` projection

```math
\kappa(x,y,z)=(x,y),
```

we have

```math
\boxed{
\kappa(P_1)=\kappa(P_0)
}
```

while for `h != 0`

```math
\boxed{
P_1\ne P_0.
}
```

Therefore PLJ is an exact quotient-return specimen:

```text
projected phase closes
carrier lifts
```

The residual is explicitly

```math
\rho=3h e_z.
```

Repeated cycles give

```math
P_n=P_0+3nh e_z.
```

If the axial coordinate is ordinary `R` and `h != 0`, there is no nonzero finite `n` with

```math
P_n=P_0.
```

So:

```text
quotient return period = 1 complete triadic cycle
exact carrier return period = infinite / absent
```

This does not make a helix a mystical circle. It makes the distinction ordinary:

> **THE QUOTIENT CLOSES WHILE THE LIFT ACCUMULATES.**

---

# 5 — TRANSVERSE QUOTIENT RETURN

Current internal Dogram research uses

```math
G=\mathbb Z_m\times\mathbb Z_n
```

with synchronized motion

```math
\sigma=(1,1).
```

Let

```math
d=\gcd(m,n).
```

The synchronized quotient sheet coordinate is

```math
\phi(a,b)=a-b\pmod d.
```

A typed transverse cut is

```math
\alpha_r=(r,0).
```

It changes sheet coordinate by

```math
\phi(a+r,b)=\phi(a,b)+r\pmod d.
```

## 5.1 Complete synchronized orbit after one cut

The synchronized orbit length is

```math
L=\operatorname{lcm}(m,n).
```

Since `L` is divisible by both `m` and `n`, after one cut followed by one full synchronized orbit the state returns exactly to the post-cut anchor.

Thus one bounded `cut -> complete synchronized orbit` cycle acts on the starting state as

```math
\boxed{
C_r(a,b)=(a+r,b).
}
```

After `k` bounded cycles:

```math
\boxed{
C_r^k(a,b)=(a+kr,b).
}
```

and on the sheet quotient:

```math
\boxed{
\phi(C_r^k(a,b))
=
\phi(a,b)+kr\pmod d.
}
```

This turns the existing bounded-history semantics into an exact return calculation.

---

# 6 — LIFT-INDEX-RETURN-PERIOD-001

The first positive `k` for which the sheet returns is the least `k>0` satisfying

```math
kr\equiv0\pmod d.
```

Therefore:

```math
\boxed{
\Lambda
=
\frac{d}{\gcd(d,r)}.
}
```

Current `TRANSVERSE-GENERATORS-001` already calls this quantity the single-generator closure lift index.

Therefore, under the exact repeated-cycle semantics above:

```math
\boxed{
\text{single-generator closure lift index}
=
\text{quotient-sheet return period}.
}
```

This identity is stronger than a numerical coincidence: both sides are the order of `r` in the cyclic quotient group `Z_d`.

## 6.1 Design-time brute-force pressure

The formula was independently brute-forced for:

```text
m,n in 2..100
r in {-20,...,-1,1,...,20}
```

for `392,040` finite specimens.

Checked for every specimen:

```text
first brute-force sheet return period
== d / gcd(d,r)
```

No counterexample was found in that bounded pressure range.

This computational pressure is not a substitute for the elementary proof above; it is an implementation-oriented hostile control.

---

# 7 — EXACT-CARRIER-RETURN-PERIOD-001

A full carrier-state return under repeated bounded cycles requires

```math
kr\equiv0\pmod m.
```

Thus the exact carrier-return period is

```math
\boxed{
M
=
\frac{m}{\gcd(m,r)}.
}
```

Since `d | m`, quotient-sheet return is necessarily no later than exact state return.

Indeed:

```math
\boxed{
\Lambda\mid M.
}
```

So a quotient return can occur many times before the finer state returns.

This gives a precise answer to:

```text
returned to coherence — but how much return debt remains?
```

---

# 8 — RETURN-DEBT-001

For the finite single-generator transverse specimen, define

```math
\boxed{
\mu
=
\frac{M}{\Lambda}.
}
```

Because `Lambda | M`, `mu` is a positive integer.

Interpretation is deliberately narrow:

```text
mu = number of quotient-return periods inside one exact carrier-return period
```

It is not a universal measure of coherence, quality, development, spiritual growth, or dimensionality.

## 8.1 `Z_6 x Z_9`, `r=1`

```math
d=\gcd(6,9)=3.
```

Therefore:

```math
\Lambda=3/\gcd(3,1)=3.
```

Exact carrier return:

```math
M=6/\gcd(6,1)=6.
```

So:

```math
\boxed{
\mu=2.
}
```

After 3 bounded cycles:

```text
sheet returned
carrier state not returned
```

After 6:

```text
sheet returned
carrier state returned
```

This is a clean hostile specimen for any untyped Boolean `returned_to_coherence` field.

## 8.2 `Z_8 x Z_12`, `r=4`

```math
d=4.
```

The cut is quotient-inert because

```math
4\equiv0\pmod4.
```

Hence

```math
\Lambda=1.
```

The sheet reports return every bounded cycle.

But exact carrier return is

```math
M=8/\gcd(8,4)=2.
```

Thus

```math
\mu=2.
```

The quotient can say `returned` at every cycle while the full state alternates between two distinct points.

This is the sharpest simple reason not to treat quotient coherence as global state closure.

---

# 9 — RETURN-RESIDUAL-001

For generic carriers, a lawful return receipt must preserve what changed outside the quotient.

The minimum safe shape is not necessarily numeric subtraction.

Use:

```text
quotient_before
quotient_after
finer_before
finer_after
path_receipt
```

If

```text
quotient_before == quotient_after
```

while

```text
finer_before != finer_after
```

then the specimen has a quotient return with a nontrivial finer residual.

Do **not** assume a canonical expression such as

```math
b-a
```

unless the carrier declares an algebra in which that operation is lawful.

Candidate seal:

> **NO DECLARED RESIDUAL ALGEBRA -> KEEP BEFORE/AFTER, DO NOT INVENT SUBTRACTION.**

---

# 10 — RETURN-COCYCLE-001 — CONDITIONAL

A stronger algebra becomes available only when extra structure is declared.

Suppose:

1. each relevant fiber carries a declared group or torsor action;
2. transport along base paths is defined;
3. closed quotient loops induce a well-defined fiber action;
4. composition order is explicitly fixed.

Then a closed quotient loop `gamma` may produce a residual element

```math
g_\gamma
```

such that

```math
b=g_\gamma\cdot a.
```

Under compatible path concatenation, these residuals may compose.

Only then does holonomy/monodromy/cocycle language become potentially lawful.

Hard refusal:

```text
QUOTIENT RETURN ALONE
!=
HOLONOMY
```

and:

```text
NO TRANSPORT LAW
-> DO NOT CALL THE RESIDUAL HOLONOMY
```

Dogram should prefer a generic `return_residual` research term until the necessary structure is independently present.

---

# 11 — INVERSE-IS-NOT-MEMORY CONTROL

Existing `MADDDOGCLOWN-REPLAY-001` already pressure-tested the dangerous pretty version.

For stateless invertible transport:

```math
T^{-1}T x=x.
```

Exact inverse transport by itself creates no residual.

A nonzero return residual needs at least one declared source such as:

```text
noncommutation / changed order
explicit memory / retained state
coupling
loss
projection
quotient
non-inverse return map
```

Therefore:

> **A RETURN RESIDUAL MUST BE EARNED BY DECLARED PATH-DEPENDENT STRUCTURE.**

Do not infer memory merely because a path was described as forward/backward or interior/exterior.

---

# 12 — OMEGA AS TARGET-QUOTIENT RETURN

Current `OMEGA-CYCLE-001` can produce:

```text
selected result before == selected result after
```

while preserving differences in:

```text
program digest
execution digest
step trace
consumed input addresses
fuel remaining
```

This has the same abstract quotient shape:

```math
\pi_T(e_0)=\pi_T(e_1)
```

under a selected result/target quotient while

```math
e_0\ne e_1
```

at the execution cut.

Do not call this the same mechanism as PLJ or the transverse group model.

Lawful common statement:

> **A COARSE DECLARED TARGET MAY RETURN WHILE THE FINER EXECUTION RECEIPT DOES NOT.**

The existing `EXECUTION-CUT / OMEGA-QUOTIENT` design is the correct future runtime seam for this family.

This packet does not modify `omega.py`.

---

# 13 — PRODUCTIVE-DESYNC BOOLEAN PRESSURE

Current internal research classification accepts:

```text
returned_to_coherence: bool
```

as a supplied fact.

The new return calculus shows why this field must remain local and explicitly scoped.

The same bounded history can be:

```text
returned under quotient sheet
not returned under exact carrier state
not returned under formation history
```

or:

```text
returned under declared target
not returned under execution footprint
```

Therefore a future executable honing should not silently reinterpret the existing Boolean globally.

Candidate stronger conceptual shape:

```text
return_anchor
return_relation / quotient_id
return_before
return_after
returned_under_relation
```

Potentially plus:

```text
finer_residual
```

No executable change is admitted by this research packet.

---

# 14 — RETURN-WORD-001

The single-generator formula does not automatically generalize to a multi-generator family as one scalar period.

Let quotient generators be

```math
r_1,\ldots,r_k\in\mathbb Z_d.
```

Their generated subgroup determines **potential closure**.

But an actual bounded history is an ordered word

```math
w=(r_{i_1},r_{i_2},\ldots,r_{i_N}).
```

Its quotient displacement is

```math
\Delta_\phi(w)
=
\sum_{j=1}^N r_{i_j}\pmod d
```

for this abelian cyclic quotient specimen.

Return of the actual word requires

```math
\Delta_\phi(w)=0.
```

The subgroup generated by all admitted generators may be the full quotient while the declared word has not returned yet.

Therefore:

```text
GENERATOR CLOSURE
!=
DECLARED WORD
!=
ACTUAL HISTORY
```

This is the return-calculus restatement of the existing Dogram law:

```text
ONE CROSSING != GENERATOR CLOSURE
POTENTIAL REACHABILITY != ACTUAL HISTORY
```

---

# 15 — RETURN PERIOD VS REACHABILITY

For the single-generator transverse model, one exact quantity currently carries two related roles:

```text
Lambda = number of quotient sheets in the generated cyclic orbit
Lambda = period required for that cyclic quotient orbit to return
```

These coincide because the orbit is cyclic and generated by one element.

Do not universalize this coincidence.

In a more general finite group action:

```text
orbit cardinality
```

and:

```text
return period of a particular word / transformation
```

need not be interchangeable without the relevant action/orbit-stabilizer assumptions.

Candidate refusal:

> **ORBIT SIZE IS NOT A UNIVERSAL SYNONYM FOR RETURN PERIOD.**

---

# 16 — POINT-HORIZON COMPATIBILITY

`POINT-HORIZON-001` already preserves:

```text
arrived history -> situated point -> available actions -> explicit action -> next point
```

with:

```text
KNOWN-LATER-ABOUT(t) != AVAILABLE-AT(t)
```

Return calculus adds no backward leakage.

A later point may establish that an earlier trajectory eventually returned under some quotient.

That does not make the future return available at the earlier cut.

So:

```text
EVENTUAL RETURN
!=
RETURN KNOWN AT DEPARTURE
```

and:

```text
RETURN PERIOD OF THE DYNAMICS
!=
FUTURE EVENT ALREADY WITNESSED
```

This chronology guard should remain explicit in any later orchestration.

---

# 17 — NINE HOSTILE CONTROLS

The research survives only if these refusals remain visible.

## H1 — exact inverse

```text
T followed by T^-1
-> exact state return
-> zero residual unless separate memory is declared
```

## H2 — coarse quotient hides change

```text
pi(a) = pi(b)
a != b
```

Valid quotient return; invalid exact-return claim.

## H3 — quotient-inert cut

`Z_8 x Z_12`, `r=4`:

```text
sheet return every cycle
state return every 2 cycles
```

Kills global interpretation of a coarse return Boolean.

## H4 — coprime synchronized world

If

```math
\gcd(m,n)=1,
```

there is only one synchronized quotient sheet.

Sheet-return becomes trivial and cannot by itself establish useful lift.

## H5 — multi-generator closure without historical return

Full generated subgroup may exist while the actual bounded word has nonzero displacement.

Potential closure is not realized return.

## H6 — same endpoint, different path

Exact endpoint return can coexist with different approach/execution history.

Endpoint closure does not erase formation.

## H7 — unrelated decoders

Agreement under one decoder and disagreement under another do not define refinement unless one factors through the other.

No fake return lattice.

## H8 — no fiber law

If fibers lack declared algebra/transport, preserve before/after values.

No invented holonomy.

## H9 — target chosen after outcomes

If the quotient/target is selected adaptively to force a return verdict, the return claim does not have a stable predeclared relation.

```text
TARGET THAT MOVES WITH THE ANSWER CANNOT PAY FOR RETURN.
```

---

# 18 — RESEARCH RECEIPT SHAPE

A reusable research-only return receipt should carry at least:

```text
specimen_id
anchor_before
anchor_after
path_receipt
quotient_id
quotient_before
quotient_after
returned_under_quotient
finer_before
finer_after
finer_relation
residual_representation
```

Optional finite-dynamics fields when lawfully defined:

```text
quotient_return_period
exact_return_period
return_debt
historical_reach_count
closure_reach_count
```

Optional group-action fields only when declared:

```text
fiber_action_id
transport_law_id
residual_group_element
composition_order
```

Required refusal surface:

```text
return_under_quotient != global equivalence
residual != meaning
reachability gain != desirability
quotient closure != historical occurrence
```

---

# 19 — DOGRAM HONING CANDIDATES

Research survivors:

1. `RETURN-IS-A-RELATION-001`
2. `QUOTIENT-RETURN-001`
3. `RETURN-REFINEMENT-001`
4. `RETURN-SPECTRUM-001`
5. `LIFT-INDEX-RETURN-PERIOD-001`
6. `EXACT-CARRIER-RETURN-PERIOD-001`
7. `RETURN-DEBT-001`
8. `RETURN-RESIDUAL-001`
9. `RETURN-WORD-001`

Conditional survivor:

```text
RETURN-COCYCLE-001
```

only when a lawful fiber/transport algebra exists.

Hard correction:

```text
NO-FIBER-LAW-NO-HOLONOMY-001
```

---

# 20 — RUNTIME VERDICT

**NO NEW PUBLIC OPERATOR.**

Do not add:

```text
return@1
holonomy@1
monodromy@1
lift@1
coherence@1
```

from this packet.

The existing public four-operator floor remains sufficient for first frozen specimen lowering:

```text
delta@1
rectangle@1
ablate@1
reach@1
```

The existing internal transverse kernel already computes the finite algebra needed for the strongest first specimen.

A future executable honing may refine the internal productive-desync return receipt, but only after separate implementation review.

`omega.py` remains untouched by this packet.

---

# 21 — FATDOG COMPRESSION

```text
RETURN IS NOT A BOOLEAN.
RETURN MUST NAME ITS QUOTIENT.

CLOSED BELOW
CAN REMAIN OPEN ABOVE.

THE QUOTIENT MAY RETURN
WHILE THE CARRIER LIFTS.

THE CARRIER MAY RETURN
WHILE THE HISTORY DIFFERS.

ONE GENERATOR'S LIFT INDEX
CAN ALSO BE ITS QUOTIENT RETURN PERIOD
WHEN THE DECLARED ACTION IS CYCLIC.

GENERATOR CLOSURE
!= DECLARED WORD
!= ACTUAL HISTORY.

NO FIBER LAW
-> NO HOLONOMY CLAIM.
```

## Seal

> **A RETURN CAN BE A LIFT.**
>
> **WHAT CLOSED, UNDER WHICH CUT, AND WHAT REMAINED OUTSIDE THE CLOSURE?**
>
> **DO THE MATH. SHOW THE DELTA. KEEP THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**
