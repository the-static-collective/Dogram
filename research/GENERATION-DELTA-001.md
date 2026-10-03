# GENERATION-DELTA-001 — Measure the Descendant Without Grading It

**Status:** EXACT INTERNAL INSTRUMENT · NO NEW PUBLIC OPERATOR  
**Runtime authority:** NONE

> **DOGRAM MEASURES TRANSFORMS, NOT PEOPLE.**

## Question

A bounded radio specimen is answered by Haunted Phonograph. A human may explicitly admit the proposal audition as a new radio specimen.

The narrow Dogram question is:

> Given the exact parent and descendant PCM carriers plus the declared admission relation, what finitely measurable signal properties changed?

This instrument does not decide whether the change is good, musical, meaningful, faithful, interesting, or desirable.

## Required relation

The caller must already provide:

- parent window id;
- child window id;
- relation = `ADMITTED_PROPOSAL_AS_NEW_AUDIO_SPECIMEN`;
- human_action = `explicit-admit`;
- proposal receipt hash;
- audition digest.

Dogram does not create or authorize that relation.

```text
ADMISSION != MEASUREMENT
MEASUREMENT != AUTHORITY
```

## Carrier floor

Both carriers must be exact bounded:

- WAV;
- 44.1 kHz;
- stereo;
- signed 16-bit PCM;
- content-addressed by SHA-256.

The instrument measures each carrier independently and then computes child - parent.

## Measured axes

The v0 signal profile contains only finite integer quantities:

- frame count;
- floor duration in milliseconds plus exact frame remainder;
- RMS amplitude for four equal temporal quarters;
- peak absolute amplitude;
- zero-crossing activity on the left channel, in parts per million.

The delta receipts:

- signed scalar differences;
- signed quartile-vector differences;
- changed axes;
- unchanged axes;
- classification = `MEASURED_CHANGE` or `NO_MEASURED_CHANGE`.

The classification means only whether these declared axes changed.

## Residuals

The following remain explicitly unresolved:

- pitch or key;
- harmony;
- source instrumentation;
- semantic meaning;
- musical value;
- listener effect.

```text
RESIDUAL != FAILURE
UNMEASURED != ABSENT
MEASURED CHANGE != MUSICAL MEANING
DELTA != VALUE
```

## Lineage

The receipt carries both exact window identities and the explicit transform relation. The child cannot impersonate an origin.

```text
DESCENDANT != PARENT
ANCESTRY != AUTHORITY
A DERIVED CARRIER MUST NOT IMPERSONATE AN ORIGIN
```

## Why this is not audio analysis theater

GENERATION-DELTA-001 does not estimate source tempo, chord progression, genre, mood, authorship, or quality.

It intentionally stays below those claims.

Its job is to say things like:

```text
duration: -250 ms
quartile RMS: [+2810, +3194, +2901, +2550]
peak: +9102
zero-crossing activity: +48211 ppm
```

and then stop.

## Next lawful crossing

Once parent and descendant each have real First-Listen Radio witnesses, a separate layer may compare listener-response transforms while preserving:

```text
SIGNAL DELTA != LISTENER DELTA
LISTENER DELTA != VALUE
OBSERVATION != ESSENCE
```

Dogram can measure those declared differences later. It should not infer them from PCM alone.
