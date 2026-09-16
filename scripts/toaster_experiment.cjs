// Opt-in local integration. Process/IO capability stays outside dogram/.
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs/promises");
const path = require("node:path");
const { execFileSync } = require("node:child_process");

const CELLS = ["00", "01", "10", "11"];
const SAMPLER = {
  id: "gray32x18-6fps-q16/v0", width: 32, height: 18, fps: 6,
  pixel_format: "gray", quantization_step: 16,
  filter: "fps=6,scale=32:18:flags=area,format=gray",
};
const sha = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");
const git = (root, ...args) => execFileSync("git", ["-C", root, ...args], { encoding: "utf8" }).trim();
const json = async (file) => JSON.parse(await fs.readFile(file, "utf8"));
const writeJson = async (file, value) => fs.writeFile(file, `${JSON.stringify(value, null, 2)}\n`, { flag: "wx" });

function parseArgs(argv) {
  const options = { seed: "dogram-toaster-pair-001" };
  for (let i = 0; i < argv.length; i += 2) {
    const name = argv[i];
    if (!["--toaster", "--out", "--audio", "--seed"].includes(name) || !argv[i + 1] || argv[i + 1].startsWith("--")) {
      throw new Error("Usage: node scripts/toaster_experiment.cjs --toaster CHECKOUT --out NEW_DIRECTORY [--audio CLIP] [--seed SEED]");
    }
    options[name.slice(2)] = argv[i + 1];
  }
  if (!options.toaster || !options.out) throw new Error("--toaster and --out are required");
  return options;
}

function withoutAxes(score) {
  const common = structuredClone(score);
  delete common.motion.grammar;
  delete common.camera.grammar;
  return common;
}

function assertFactorial(cells) {
  for (const key of CELLS) {
    assert.deepEqual(withoutAxes(cells[key].score), withoutAxes(cells["00"].score), "undeclared score drift");
    assert.equal(cells[key].score.motion.grammar, key[0] === "0" ? "still" : "drift");
    assert.equal(cells[key].score.camera.grammar, key[1] === "0" ? "locked" : "orbit");
    assert.equal(cells[key].score.temporalDensity, "frozen");
    assert.equal(cells[key].timeline.patches.length, 0, "resolver introduced additional patches");
  }
}

async function run(options) {
  const toaster = path.resolve(options.toaster);
  const app = path.join(toaster, "src/full-measure");
  const out = path.resolve(options.out);
  const commit = git(toaster, "rev-parse", "HEAD");
  if (git(toaster, "status", "--porcelain")) throw new Error("Use a clean Toaster checkout so its commit identifies the consumed code.");
  const generation = require(path.join(app, "src/generation/index.cjs"));
  const { toGenerationAnalysis } = require(path.join(app, "src/candidate-session.cjs"));
  const { inspectAudio } = require(path.join(app, "src/render/analyze.cjs"));
  const { renderVideo } = require(path.join(app, "src/render/render.cjs"));
  const { hashFile } = require(path.join(app, "src/render/receipt.cjs"));
  const { resolveFfmpeg, resolveFfprobe, runProcess } = require(path.join(app, "src/render/tooling.cjs"));
  const constraints = await json(path.join(app, "constraints/porchlight.v1.json"));
  const profile = await json(path.join(app, "profiles/toaster-raster-1.json"));
  // Explicit compatibility specimen, not a claim about the current UI profile.
  profile.canvas = { width: 640, height: 360, fps: 24 };
  await fs.mkdir(out); // Never reuse a directory containing an earlier run.
  const audio = path.join(out, options.audio ? `source${path.extname(options.audio)}` : "source.wav");
  if (options.audio) await fs.copyFile(path.resolve(options.audio), audio);
  else await runProcess(resolveFfmpeg(), ["-nostdin", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i",
    "sine=frequency=137:duration=4:sample_rate=48000", "-c:a", "pcm_s16le", audio]);
  const analysis = await inspectAudio(audio);
  if (!(analysis.duration >= 1 && analysis.duration <= 30)) throw new Error("Use an audio excerpt between 1 and 30 seconds.");
  const sourceHash = await hashFile(audio);
  const generationAnalysis = toGenerationAnalysis(analysis);
  const cells = {};
  for (const key of CELLS) {
    const { score } = generation.createVisualScore({
      seed: options.seed, constraints,
      overrides: {
        topology: "linear", temporalDensity: "frozen",
        motion: { grammar: key[0] === "0" ? "still" : "drift" },
        camera: { grammar: key[1] === "0" ? "locked" : "orbit" },
        material: { texture: "clean" }, palette: { logic: "garment" },
      },
    });
    cells[key] = { score, timeline: generation.resolve(generationAnalysis, score, constraints, profile) };
  }
  assertFactorial(cells);
  const renderConfig = {
    presetId: "porchlight", title: "Dogram paired-control specimen", artist: "The Static Collective",
    lyrics: "", width: 640, height: 360, fps: 24, outputProfileId: "delivery",
  };
  const version = async (binary) => (await runProcess(binary, ["-version"])).stdout.split(/\r?\n/)[0];
  const artifact = async (file) => ({ path: path.basename(file), sha256: await hashFile(file) });
  const plan = {
    schema: "dogram.toaster-plan/v0", experiment_id: options.seed,
    axes: { a: { path: "motion.grammar", levels: ["still", "drift"] }, b: { path: "camera.grammar", levels: ["locked", "orbit"] } },
    source: await artifact(audio), source_kind: options.audio ? "user-audio-excerpt" : "synthetic-sine-control",
    toaster: { commit, clean: true }, node: process.version, adapter_sha256: sha(await fs.readFile(__filename)),
    tools: { ffmpeg: await version(resolveFfmpeg()), ffprobe: await version(resolveFfprobe()) },
    scope: "Full production output, including score-identity-dependent typography; not isolated optical motion.",
    sampler: SAMPLER, render_config: renderConfig, constraints, profile, generation_analysis: generationAnalysis,
    cells: Object.fromEntries(CELLS.map((key) => [key, {
      score: cells[key].score, score_address: cells[key].timeline.scoreAddress,
      timeline_hash: cells[key].timeline.timelineHash,
    }])),
  };
  const planPath = path.join(out, "plan.json");
  await writeJson(planPath, plan); // Freeze the observation before any render.
  const planHash = await hashFile(planPath);
  const manifest = { schema: "dogram.toaster-render-manifest/v0", plan_sha256: planHash, cells: {} };
  for (const key of CELLS) {
    assert.equal(await hashFile(audio), sourceHash, "source changed during experiment");
    process.stdout.write(`Rendering ${key}: ${cells[key].score.motion.grammar} × ${cells[key].score.camera.grammar}\n`);
    const result = await renderVideo({ ...renderConfig, audioPath: audio, outputPath: path.join(out, `${key}.mp4`),
      analysis, visualScore: cells[key].score, resolvedTimeline: cells[key].timeline });
    const receipt = await json(result.receiptPath);
    assert.equal(receipt.validation?.accepted, true);
    assert.equal(receipt.source.sha256, sourceHash);
    assert.equal(receipt.canonicalExecution.scoreAddress, plan.cells[key].score_address);
    assert.equal(receipt.canonicalExecution.timelineHash, plan.cells[key].timeline_hash);
    assert.equal(receipt.build.commit, commit);
    const framesPath = path.join(out, `${key}.gray`);
    await runProcess(resolveFfmpeg(), ["-nostdin", "-hide_banner", "-loglevel", "error", "-i", result.outputPath,
      "-map", "0:v:0", "-vf", SAMPLER.filter, "-an", "-f", "rawvideo", "-pix_fmt", "gray", framesPath]);
    manifest.cells[key] = {};
    for (const [name, file] of Object.entries({ video: result.outputPath, receipt: result.receiptPath,
      score: result.scorePath, timeline: result.timelinePath, frames: framesPath })) {
      manifest.cells[key][name] = await artifact(file);
    }
  }
  assert.equal(await hashFile(planPath), planHash, "plan changed during experiment");
  assert.equal(await hashFile(audio), sourceHash, "source changed during experiment");
  assert.equal(git(toaster, "rev-parse", "HEAD"), commit, "Toaster checkout changed during experiment");
  if (git(toaster, "status", "--porcelain")) throw new Error("Toaster checkout became dirty during experiment");
  await writeJson(path.join(out, "render-manifest.json"), manifest);
  process.stdout.write(`Four accepted renders retained in ${out}\n`);
}

if (require.main === module) {
  run(parseArgs(process.argv.slice(2))).catch((error) => {
    process.stderr.write(`${error.stack || error.message}\nNo completed experiment manifest was certified. Use a new output directory to retry.\n`);
    process.exitCode = 1;
  });
}
module.exports = { CELLS, SAMPLER, assertFactorial, parseArgs };
