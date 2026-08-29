# COMMON-CARRIER SUCCESSOR — 1700 / 1800

**Status:** FRONTIER MATHAL SLICE · RUNTIME CANDIDATES NOT YET ADMITTED

**Specimen:**

\[
1700 \rightarrow 1800
\]

The surface transition is `+100`. After peeling the maximal shared integer carrier, the transition is a single successor step:

\[
1700=100\cdot17,
\qquad
1800=100\cdot18.
\]

Therefore:

\[
\boxed{1700\rightarrow1800=100\cdot(17\rightarrow18)}
\]

The durable mathal is not the decimal appearance. It is the relation between **GCD carrier**, **difference**, and **primitive reduced pair**.

---

## 1. Exact receipts

Let

\[
a=1700,\qquad b=1800.
\]

Then

\[
g=\gcd(a,b)=100
\]

and

\[
\Delta=b-a=100.
\]

So this specimen satisfies

\[
\boxed{\Delta=g}.
\]

Dividing by the maximal shared carrier:

\[
\left(\frac ag,\frac bg\right)=(17,18).
\]

The reduced pair is adjacent:

\[
18-17=1,
\]

and coprime:

\[
\gcd(17,18)=1.
\]

Hence all integer scale shared by the original pair has been isolated into `g=100`.

**Keeper:**

> **ALL SHARED INTEGER SCALE IS IN THE CARRIER; THE REDUCED CHANGE IS ONE SUCCESSOR STEP.**

---

## 2. General theorem

For positive integers `a < b`, let

\[
g=\gcd(a,b).
\]

Write

\[
a=gm,\qquad b=gn,
\]

with

\[
\gcd(m,n)=1.
\]

Because

\[
b-a=g(n-m),
\]

we have

\[
\boxed{b-a=g \iff n-m=1}.
\]

Therefore:

\[
\boxed{
|b-a|=\gcd(a,b)
\iff
\text{the GCD-reduced pair differs by exactly one integer step}
}
\]

for distinct positive integers.

This gives an exact definition of a **primitive lattice successor**.

---

## 3. Coarsest shared lattice

`g = gcd(a,b)` is the largest positive integer spacing for which both values are lattice points:

\[
a,b\in g\mathbb Z.
\]

After quotienting by this shared scale, the specimen becomes

\[
17\rightarrow18.
\]

So the apparently large transition `1700 -> 1800` is one tick on its coarsest shared integer lattice.

This wording is structural rather than decimal-specific. The same reduction works in any numeral representation.

---

## 4. Canonical transition fingerprint

Define the GCD-normalized pair

\[
P(a,b)=\left(g,\frac ag,\frac bg\right),
\qquad g=\gcd(|a|,|b|).
\]

For the specimen:

\[
P(1700,1800)=(100,17,18).
\]

The **scale-free transition shape** is

\[
\pi(a,b)=\left(\frac ag,\frac bg\right).
\]

Thus

\[
\pi(1700,1800)=(17,18).
\]

Every positive integer rescaling has the same primitive shape:

\[
\pi(1700k,1800k)=(17,18)
\]

for every positive integer `k`.

This yields an exact equivalence relation for transition shape under common scaling:

\[
(a,b)\sim(ka,kb),\qquad k\in\mathbb Z_{>0}.
\]

The quotient representative is the coprime pair `(a/g,b/g)`.

**Runtime-relevant keeper:**

> **SEPARATE TRANSITION SHAPE FROM TRANSITION SCALE.**

---

## 5. Carrier-delta ratio

Define

\[
\rho(a,b)=\frac{b-a}{\gcd(|a|,|b|)}
\]

when `(a,b) != (0,0)`.

Because the GCD divides both values, `rho` is always an integer.

For the specimen:

\[
\rho(1700,1800)=1.
\]

Interpretation is purely calculational:

- `rho = 1`: one forward primitive-lattice step;
- `rho = -1`: one reverse primitive-lattice step;
- `|rho| > 1`: multiple reduced lattice steps;
- `rho = 0`: no change when the pair is equal and nonzero.

No semantic meaning is implied by these classifications.

---

## 6. Step view and center view

The same pair admits another exact coordinate system.

Midpoint:

\[
c=\frac{a+b}{2}=1750.
\]

Half-span:

\[
h=\frac{b-a}{2}=50.
\]

Therefore:

\[
a=c-h,
\qquad
b=c+h.
\]

So the same transition can be represented as either:

### Step coordinates

\[
(g,m,n)=(100,17,18)
\]

or

### Center-span coordinates

\[
(c,h)=(1750,50).
\]

These are distinct exact decoders of the same pair:

\[
\boxed{\text{STEP VIEW}\leftrightarrow\text{CENTER-SPAN VIEW}}.
\]

Dogram should not decide which view is meaningful. It can calculate both and preserve the transform receipt.

---

## 7. Hostile controls

### Control A — same GCD, multi-step

\[
1700\rightarrow1900
\]

gives

\[
\gcd=100,\qquad \Delta=200,\qquad \rho=2.
\]

Reduced pair:

\[
17\rightarrow19.
\]

Not a primitive successor.

### Control B — same surface delta, different primitive step count

\[
1750\rightarrow1850
\]

has

\[
\gcd=50,\qquad \Delta=100,\qquad \rho=2.
\]

The raw `+100` surface is therefore insufficient to classify the structural step.

### Control C — nearby values, weaker shared carrier

\[
1701\rightarrow1800
\]

has

\[
\gcd=9,\qquad \Delta=99,\qquad \rho=11.
\]

The clean one-step structure disappears.

### Control D — reverse traversal

\[
1800\rightarrow1700
\]

has

\[
\rho=-1.
\]

Same primitive adjacency, opposite orientation.

### Control E — scale sibling

\[
3400\rightarrow3600
\]

has

\[
\gcd=200
\]

and reduces to

\[
17\rightarrow18.
\]

This must share the same scale-free transition fingerprint as the original specimen.

---

## 8. Candidate Dogram runtime applications

These are **candidate executable surfaces**, not admitted operators.

### 8.1 `primitive_pair(a, b)`

Compute:

```text
g = gcd(abs(a), abs(b))
primitive = (a / g, b / g)
```

Receipt fields could include:

```text
input_pair
carrier_gcd
primitive_pair
reconstructs_exactly
```

The transform is lossless when the carrier is retained:

\[
(a,b)=g\cdot\pi(a,b).
\]

### 8.2 `lattice_step(a, b)`

Compute:

```text
carrier_gcd
raw_delta
reduced_delta = raw_delta / carrier_gcd
orientation
primitive_pair
```

Possible structural labels:

```text
FORWARD_UNIT_STEP
REVERSE_UNIT_STEP
MULTISTEP
STATIONARY
UNDEFINED_ZERO_PAIR
```

These are arithmetic classifications only.

### 8.3 `transition_fingerprint(a, b)`

Expose a canonical fingerprint that separates scale from shape:

```text
scale = gcd(abs(a), abs(b))
shape = primitive_pair(a, b)
step = reduced_delta
```

This can support exact deduplication of transitions that differ only by a common integer scale.

Example:

```text
1700 -> 1800
3400 -> 3600
85   -> 90
```

all reduce to

```text
17 -> 18
```

while preserving distinct carrier scales.

### 8.4 Transition clustering

A corpus of numeric transitions can be grouped by primitive pair rather than raw magnitude.

This could reveal repeated transformation shapes across different scales without asserting that the source phenomena are semantically related.

### 8.5 Pre-comparison normalization

Before comparing two numeric transitions, Dogram can compute both raw and primitive representations.

This prevents two opposite mistakes:

```text
same raw delta => same structural transition
```

and

```text
different raw magnitude => different transition shape
```

Neither implication is valid in general.

### 8.6 Regeneration check

The normalized receipt can require exact reconstruction:

\[
g\cdot(m,n)\stackrel{?}{=}(a,b).
\]

That makes GCD peeling a good specimen for the broader Dogram principle that a compression should retain enough receipt information to regenerate its input exactly when the transform claims to be lossless.

### 8.7 Center-span sibling receipt

Using exact rational arithmetic, Dogram can also expose:

```text
center = (a + b) / 2
half_span = (b - a) / 2
```

and verify:

```text
left  = center - half_span
right = center + half_span
```

This supplies a second reversible representation against which the primitive-pair representation can be pressure-tested.

---

## 9. Candidate admission order

If runtime implementation is later approved, the smallest useful order is:

1. `primitive_pair(a,b)` — exact canonical reduction;
2. `lattice_step(a,b)` — classify reduced displacement;
3. `transition_fingerprint(a,b)` — package scale and shape for corpus comparison;
4. center-span transform — exact sibling representation using rational arithmetic.

The first implementation should remain standard-library, deterministic, exact, and receipt-producing.

No automatic semantic equivalence should be inferred from matching fingerprints.

---

## 10. Non-collapses

```text
SAME DELTA != SAME PRIMITIVE STEP
SAME PRIMITIVE STEP != SAME SCALE
SAME PRIMITIVE SHAPE != SAME SEMANTIC PROCESS
GCD CARRIER != CAUSAL CARRIER
NUMERIC NORMALIZATION != HISTORICAL EXPLANATION
STEP VIEW != CENTER-SPAN VIEW
```

The word `carrier` in this slice means **shared integer factor only** unless another typed layer explicitly establishes a different relation.

---

## 11. Seal

\[
\boxed{1700\rightarrow1800=100\cdot(17\rightarrow18)}
\]

\[
\boxed{\Delta=\gcd=100}
\]

\[
\boxed{\rho=1}
\]

> **PEEL THE COMMON CARRIER, AND THE BIG MOVE BECOMES ONE SMALL STEP.**

And the runtime-facing form:

> **PRESERVE THE SCALE. CANONICALIZE THE SHAPE. SHOW THE RECEIPT. DO NOT DECIDE WHAT IT MEANS.**
