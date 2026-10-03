# LISTENER-DELTA-001 — Measure the Response Transform Without Measuring the Person

**Status:** EXACT INTERNAL INSTRUMENT · NO NEW PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DOGRAM MEASURES TRANSFORMS, NOT PEOPLE.**

## Question

Two declared first-listener identities hear a parent radio specimen in isolation.

A Haunted Phonograph proposal is explicitly admitted as a descendant specimen.

The same declared listener identities then encounter the descendant fresh.

The narrow Dogram question is:

> Given the four exact sealed first-response receipts, what finitely observable response structure changed between parent and descendant?

This instrument does not decide what the change means.

It does not decide whether the descendant is better.

It does not claim the audio transform caused the response transform.

## Required relation

The caller must already provide:

- parent window id;
- child window id;
- explicit human admission;
- Phonograph proposal receipt hash;
- the corresponding GENERATION-DELTA-001 receipt hash;
- exactly two sealed parent first responses;
- exactly two sealed descendant first responses.

The parent and descendant sets must contain the same listener identities.

Each listener descriptor must remain byte-equivalent at the structured JSON level across generations.

```text
LISTENER IDENTITY MUST HOLD
RESPONSE CONTENT MAY CHANGE
RESPONSE DELTA != PERSON DELTA
```

## Sealed-response verification

LISTENER-DELTA-001 independently verifies each Autodisco first-listen carrier.

It recomputes:

- `response_sha256` from the canonical response object;
- `first_response_id` from the canonical sealed-response body.

It also verifies:

- first-response schema;
- one pair id per generation;
- one audio digest per generation;
- exactly two distinct listener ids;
- binding to the declared parent or descendant window.

A text blob without intact first-listen identity is not admitted.

## What v0 measures

For each listener, Dogram builds a finite response profile containing:

- exact observation count;
- count by declared observation mode:
  - `OBSERVED`
  - `DERIVED`
  - `METAPHOR`
  - `INTERPRETATION`
- original observation text;
- whitespace-normalized, Unicode-normalized, case-folded observation text;
- exact observation vocabulary;
- lingering-intrigue boolean;
- closing-line text, normalized form, character count, and token count;
- model id;
- pair, window, audio, response, and first-response identities.

The per-listener delta then receipts:

- exact observations that persisted;
- exact observations that appeared;
- exact observations that disappeared;
- mode migrations where identical normalized text moved between declared modes;
- signed count delta for each mode;
- intrigue transition;
- closing-line equality and length deltas;
- exact lexical vocabulary persistence / appearance / disappearance;
- model identity continuity or change.

## Cohort measurement

After measuring both listeners independently, Dogram may report only exact finite intersections across those two deltas:

- changed axes shared by both;
- union of changed axes;
- exact newly appeared tokens shared by both;
- exact disappeared tokens shared by both;
- exact newly appeared normalized observations shared by both;
- number of listeners with measured response change.

This is not semantic consensus.

```text
LEXICAL OVERLAP != SEMANTIC AGREEMENT
SHARED CHANGE AXIS != SHARED MEANING
```

## Model continuity

The instrument does not silently assume the same generative model was used.

If a listener's `model_used` differs between parent and descendant, `model_used` becomes a changed axis.

The receipt still measures the response transform but explicitly preserves:

`stochastic_generation_effect_not_separated`

as a residual.

Even when the model id is unchanged, a new generative call is not a deterministic repeated measurement.

Therefore:

```text
RESPONSE DELTA != CAUSAL EFFECT
FIRST LISTEN != STABLE PREFERENCE
```

## Normalization boundary

Text normalization is intentionally mechanical:

1. Unicode NFKC normalization;
2. trim outer whitespace;
3. collapse internal whitespace runs;
4. Unicode case-fold.

There is:

- no embedding;
- no synonym expansion;
- no topic model;
- no sentiment model;
- no semantic classifier.

If one response says “pulse” and another says “beat,” v0 does not decide they mean the same thing.

That unresolved relation is a residual, not a failure.

## Classification

Per listener:

- `MEASURED_RESPONSE_CHANGE`
- `NO_MEASURED_RESPONSE_CHANGE`

The cohort receives the same two-valued classification based only on whether one or more declared axes changed.

The classification is not a score.

## Residuals

LISTENER-DELTA-001 explicitly leaves unresolved:

- semantic similarity;
- preference;
- musical value;
- any claim about listener essence or identity;
- causal attribution from audio delta to response delta;
- stochastic generation effects;
- unobserved listener context.

```text
RESIDUAL != FAILURE
UNMEASURED != ABSENT
DELTA != VALUE
```

## Relationship to GENERATION-DELTA-001

The two receipts remain separate.

```text
GENERATION-DELTA-001
    measures signal transform

LISTENER-DELTA-001
    measures sealed response transform
```

A future composition layer may place them beside one another.

It may not collapse them into:

```text
signal delta caused listener delta
```

without a separately justified experimental design.

## Laws

```text
DOGRAM MEASURES TRANSFORMS, NOT PEOPLE
RESPONSE DELTA != PERSON DELTA
RESPONSE DELTA != CAUSAL EFFECT
SIGNAL DELTA != LISTENER DELTA
LEXICAL OVERLAP != SEMANTIC AGREEMENT
FIRST LISTEN != STABLE PREFERENCE
DELTA != VALUE
RESIDUAL != FAILURE
DO NOT DECIDE WHAT IT MEANS
```

## Next lawful crossing

The next useful layer is not a bigger listener metric.

It is a **paired experiment receipt** that can place:

- one exact signal-delta receipt;
- one exact listener-delta receipt;
- the declared experiment conditions;

beside one another without inferring causation.

That would let the system ask:

> What changed in the artifact, and what changed in the observed responses?

while still refusing the stronger claim:

> Therefore this artifact change produced that response change.
