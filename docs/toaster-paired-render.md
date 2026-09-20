# Toaster paired-render experiment v0

This gives Dogram one recurring job: measure what happens when two declared
Toaster score controls are combined. Everything runs locally from separate
checkouts. No plugin connection, server, shared database, pip/npm installation,
or repository merge is required by the experiment itself.

## Run

Prerequisites: Python 3.12+, Node 24+, Git, and FFmpeg/ffprobe usable by Toaster
(including libass and libx264). Toaster's installed static binaries also work;
its existing `FULL_MEASURE_FFMPEG` / `FULL_MEASURE_FFPROBE` overrides are honored.
The binaries' version strings are retained. Commands below run from Dogram.

```bash
# Synthetic four-second sine control: four actual production renders.
python -m scripts.toaster_report ../toaster-run-001 --toaster ../the-haunted-toaster

# A real audio excerpt; 1–30 seconds keeps the first experiment bounded.
python -m scripts.toaster_report ../toaster-run-song --toaster ../the-haunted-toaster --audio ../clip.wav --seed song-001

# Verify retained artifact hashes and recompute all calculations without rendering.
python -m scripts.toaster_report ../toaster-run-001
```

Use quotes for paths containing spaces. On Windows, use the available Python
3.12+ command (for example `py -3.12`) in place of `python`. Windows execution
has not been witnessed by this slice. The output parent must exist and the run
directory must not exist. Partial runs are retained for diagnosis; retry in a
new directory. A failed/incomplete render never produces a completed manifest
or an `OK` comparison. Toaster must be a clean git checkout; a separate clean
worktree can be used alongside ongoing development.

## Frozen comparison

| Cell | A: `motion.grammar` | B: `camera.grammar` |
| --- | --- | --- |
| 00 | still | locked |
| 01 | still | orbit |
| 10 | drift | locked |
| 11 | drift | orbit |

The adapter uses Toaster's own `createVisualScore`, constraints validator,
`resolve`, and production `renderVideo`. The same seed, source bytes, analysis,
remaining score fields, output geometry and transport are shared. It verifies
score equality after removing just the two declared fields. Temporal density
is `frozen`, and every resolved timeline must contain zero patches.

The renderer receives the accepted score and its exact resolved timeline.
Nothing edits a timeline after resolution. Native sidecars and video receipts
remain Toaster-owned. `plan.json` is written before rendering, and its raw-byte
SHA-256 binds the completed `render-manifest.json`.

This first adapter intentionally exercises Toaster's v1 compatibility score
path, with `porchlight.v1.json`, a declared 640×360 / 24 fps derivative of
`toaster-raster-1.json`, and the delivery transport. It does not claim coverage
of the current six-up UI, newer renderer profiles, video pantry, or every
compositional variable. It calls the renderer directly and is not UI KEEP.

**Two changed score inputs does not imply only two changed output mechanisms.**
Toaster seeds typography from score identity. That identity changes across the
rectangle. The experiment measures the full production consequence, including
typography and compression, and preserves their evidence. It does not isolate
the optical effect of motion from every downstream consequence.

## Fixed observation

Every output video is decoded with the same declared filter:

```text
fps=6,scale=32:18:flags=area,format=gray
```

All resulting frames are retained as `.gray` bytes. All four sample counts
must match; short, incomplete, or unequal observations are refused.

- **Temporal change:** sum of absolute differences between corresponding
  grayscale pixels in adjacent frames, divided by `(frames - 1) * pixels * 255`.
  This is an exact rational of decoded integer pixels, not optical flow.
- **Duplicate fraction:** `(frame count - unique quantized frames) / frame count`.
  Each pixel is quantized by integer division by 16. SHA-256 frame signatures
  are retained; equality in the calculation uses the quantized bytes.
- **Split-luma coverage:** each frame's left-half and right-half mean luma
  occupy one of 16 bins each. Receipt the visited pairs and their count over
  the declared capacity of 256. This is deliberately a coarse observation,
  not the coverage of all possible visual states.
- **Smallest sampled period:** the smallest lag with at least two complete
  periods and agreement across every retained quantized frame. `null` means
  no period was witnessed within this window and decoder, not nonperiodicity.

For each of the first three metrics, retain a normal `dogram.specimen/v0`
rectangle and its `dogram.receipt/v0`, with exact mixed delta
`f11 - f10 - f01 + f00`. No ranking, favorite, optimum, novelty verdict or
automatic mutation follows. Sampling can alias motion; quantization and
averaging can erase differences. More visited bins need not look better.

## Retained artifacts and replay

Each new run directory contains:

- the frozen plan and copied/generated source audio;
- four MP4s with native score, timeline, video-receipt and Dogram trace sidecars;
- four grayscale observation files;
- the completed manifest with raw-file SHA-256 bindings;
- `report.json`, containing all observations, public specimens, calculation
  receipts, artifact identities and scope limits;
- `report.md`, a human-readable summary.

The Python analyzer checks plan and artifact hashes, accepted-render status,
source/build identity, score/timeline binding, the timeline's canonical body
hash, output transport/geometry, and observation size before calculating.
Reanalysis is deterministic for the same inputs and analysis code. Existing
different reports are never overwritten. The report records analysis source
hashes; the plan records the Node adapter hash and Toaster commit. Hashes bind
artifacts, not authorship or external truth. Reanalysis verifies retained
samples; it does not independently decode the video again.

Nothing in this adapter adds a public Dogram operator. Rendering/processes
live under `scripts/`; the numerical observation kernel under `dogram/` remains
stdlib-only and inert. Ordinary `python -m dogram.cli` behavior is unchanged.

## Verification

```bash
python -m unittest tests.test_render_observation tests.test_toaster_report
node --test tests/toaster-experiment.test.cjs
```

Controls cover still/alternating/nonperiodic sequences, quantization loss,
exact interaction and no-op axes, unequal/missing cells, nuisance score drift,
unexpected patches, tampered source/frames/plan, failed renders, wrong build or
score bindings, and path escapes. Full production rendering is an opt-in
integration check, not a network-dependent CI requirement.

The next useful step is a user-chosen excerpt and multiple predeclared seeds,
then looking at the videos alongside these observations. A future field-only
observation needs an explicit boundary that excludes typography. Neither
larger motion nor a nonzero rectangle is automatically an improvement.
