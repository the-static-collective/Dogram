# TOASTER-PAIRED-RENDER-001

Status: experimental local application; no public operator promotion.
Date: 2026-09-16.

## Question and implementation

Can Dogram measure a predeclared four-cell Toaster experiment on real production
outputs while retaining accepted execution identities and refusing broken
handoffs? Yes, for the bounded compatibility specimen below.

`scripts/toaster_experiment.cjs` consumes a clean local Toaster checkout.
`scripts/toaster_report.py` validates the retained handoff and calls the pure
`dogram/render_observation.py` kernel, lowering three metrics to `rectangle@1`.
See [the run guide](../docs/toaster-paired-render.md).

## Source cut

- Dogram base: `ac7b9a71571308b265de96934855b85a182fe03b`.
- Toaster: `e8e8fb0fa3c13c98aae8c3ca5e98cb4de9f19031`, clean isolated checkout.
- Node `v24.19.0`; Python `3.12.14`; system FFmpeg `6.1.1-3ubuntu5`.
- Source: locally generated 4-second, 137 Hz sine, 48 kHz PCM WAV.
- Seed: `dogram-toaster-pair-001`.
- Accepted v1 compatibility scores: motion `still/drift` × camera `locked/orbit`.
- Temporal density frozen, no resolver patches, linear topology, clean material,
  garment palette, porchlight constraints, explicitly derived 640×360 / 24 fps
  raster-1 profile, delivery transport.
- Observation declared before renders: 6 fps, 32×18 grayscale, quantization 16.

The full production frame includes score-identity-dependent typography. This
is not an isolated optical motion experiment or a current beta UI witness.

## Observed result

| Cell | Frames | Unique quantized frames | Visited split-luma states / 256 | Sampled period |
| --- | ---: | ---: | ---: | --- |
| still / locked | 24 | 24 | 3 | none witnessed |
| still / orbit | 24 | 24 | 2 | none witnessed |
| drift / locked | 24 | 24 | 2 | none witnessed |
| drift / orbit | 24 | 24 | 2 | none witnessed |

Exact mixed differences (`11 - 10 - 01 + 00`):

- temporal change: `113/3378240`;
- duplicate fraction: `0`;
- split-luma coverage: `1/256`.

Two independently completed four-render runs produced identical observed
pixels, all four video byte hashes, and Dogram calculation receipts. The compact
[measured fixture](fixtures/toaster_paired_render_001.json) retains observations,
public specimens, their receipts, video hashes and plan/manifest hashes.
Full binary run bundles are separate artifacts, not committed to the source tree.

## Counterevidence retained

An intermediate rerun was refused with `artifact hash mismatch: 00.mp4`.
The baseline MP4 had 262192 bytes, lacked its `moov` atom, and differed from both
the render receipt and completed manifest, which recorded the same full-video
hash as the successful runs. The exact origin of the post-observation truncation
is unresolved. No repair of hashes, replacement of video bytes or weakening of
validation was used. A fresh complete run passed.

This demonstrates refusal of that corrupted handoff; it does not establish the
cause of the file corruption or universal filesystem reliability.

## Interpretation

Observed: the metrics distinguish some effects and collapse others on this
particular specimen. A nonzero mixed difference is a property of the measured
rectangle. It is not a significance test, aesthetic score, or attribution to
one physical mechanism. The baseline visiting more coarse bins is not evidence
that it is a better or more varied video.

Next question: do the differences persist across a user-chosen audio excerpt
and several predeclared seeds, and do those differences matter to a viewer?

## Verification and impact

- Python suite: 405 tests passed.
- Node adapter controls: 3 tests passed.
- Python compileall, Node syntax check, and git diff whitespace check passed.
- Real production rendering: two complete four-cell runs, exact measured replay;
  one additional run refused because its retained video was corrupted.
- No Toaster code, canonical profile, accepted sidecar schema, UI, release,
  package version, or public Dogram operator was changed.
- Linux local execution witnessed; Windows and packaged Electron not witnessed.
- Runtime effects are opt-in: render/read local files and write a new run directory.
- No network access in the experiment, automatic mutation, merge, release,
  publication, creative ranking, or new authority surface.

**SHOW THE MEASURED DELTA. KEEP THE OBSERVATION THAT MADE IT VISIBLE.**
