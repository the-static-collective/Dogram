# NAME-DECODER-PRESSURE-001

**Status:** durable Dogram research contract; decoder arithmetic only, no historical or theological authority.

## Purpose

Compare declared numerical/textual decoders over an exact ALEX-produced carrier while preserving which transformation state each decoder actually consumed.

## Input law

Dogram must not accept a naked label such as `Jesus` as sufficient provenance for a consequential result.

Minimum conceptual input:

```text
carrier_digest
carrier_text
transformation_receipt_refs[]
decoder_id
decoder_version
decoder_parameters
```

## Core non-collapses

```text
EXACT ARITHMETIC != HISTORICAL INTENT
DECODER HIT != DECODER UNIQUENESS
INVARIANCE != CAUSATION
NAME LABEL != DECODER INPUT
SAME TOTAL != SAME FORMATION
```

## First specimen family

Declared conventional mappings may produce values such as:

```text
ΙΗΣΟΥΣ -> 888     under declared Greek isopsephy
יהושע  -> 391     under declared standard Hebrew gematria
ישוע   -> 386     under declared standard Hebrew gematria
```

These are decoder-local calculations. Dogram's job is to receipt them exactly and compare what happens when the input form or decoder changes.

## Pressure axes

- exact input-state swap;
- Unicode-normalization swap;
- case/diacritic handling change;
- decoder-family swap;
- hostile/wrong decoder;
- control-name substitution;
- same-total/different-formation search;
- post-hoc decoder-family breadth.

## Suggested output classes

- `DECODER_LOCAL_EXACT`
- `FORM_DEPENDENT`
- `DECODER_DEPENDENT`
- `FAMILY_INVARIANT_CANDIDATE`
- `COMMON_CONTROL_HIT`
- `SELECTIVE_HIT_CANDIDATE`
- `POST_HOC_FLEXIBLE`
- `UNRESOLVED`

No output class means `historically intended`, `divine proof`, or `causal mechanism`.

## ALEX / Dogram membrane

```text
ALEX
  owns attestation + transformation ancestry
        ↓ exact carrier digest
Dogram
  owns deterministic decoder calculations + deltas
        ↓ calculation receipt
ALEX
  may PRESSURE the historical interpretation
```

Dogram must not mutate the upstream ALEX receipt.

## First executable question

After ALEX `NAME-ATTESTATION-001` and `ORTHO-LADDER-001` are stable, test whether existing Dogram primitives can express:

```text
DELTA(decoder(form_A), decoder(form_B))
```

and decoder-family rectangles without a new operator. Add a new operator only if an actual composition gap appears.

## Seal

> **THE NUMBER MAY CLOSE EXACTLY WHILE THE INTERPRETATION REMAINS OPEN.**
