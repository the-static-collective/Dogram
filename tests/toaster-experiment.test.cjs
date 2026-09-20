const test = require("node:test");
const assert = require("node:assert/strict");
const { assertFactorial, parseArgs, CELLS, SAMPLER } = require("../scripts/toaster_experiment.cjs");

function rectangle() {
  return Object.fromEntries(CELLS.map((key) => [key, {
    score: { seed: "same", temporalDensity: "frozen", motion: { grammar: key[0] === "0" ? "still" : "drift", amplitude: 0.4 },
      camera: { grammar: key[1] === "0" ? "locked" : "orbit" } }, timeline: { patches: [] },
  }]));
}

test("factorial guard rejects hidden nuisance drift and resolver patches", () => {
  assert.doesNotThrow(() => assertFactorial(rectangle()));
  const drift = rectangle();
  drift["11"].score.motion.amplitude = 0.5;
  assert.throws(() => assertFactorial(drift), /undeclared score drift/);
  const patched = rectangle();
  patched["01"].timeline.patches.push({ atTick: 100 });
  assert.throws(() => assertFactorial(patched), /additional patches/);
  const wrong = rectangle();
  wrong["10"].score.motion.grammar = "still";
  assert.throws(() => assertFactorial(wrong));
});

test("argument parser treats paths as inert values and rejects unknown switches", () => {
  assert.equal(parseArgs(["--toaster", "a path", "--out", "another path"]).toaster, "a path");
  for (const args of [[], ["--toaster"], ["--toaster", "a", "--out", "b", "--execute", "anything"]]) {
    assert.throws(() => parseArgs(args));
  }
});

test("Node sampler exactly matches the Python observation contract", () => {
  assert.deepEqual(SAMPLER, {
    id: "gray32x18-6fps-q16/v0", width: 32, height: 18, fps: 6,
    pixel_format: "gray", quantization_step: 16,
    filter: "fps=6,scale=32:18:flags=area,format=gray",
  });
});
