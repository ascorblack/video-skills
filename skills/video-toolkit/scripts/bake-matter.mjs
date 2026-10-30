// Bake a Matter.js scene into a per-frame table that a frame-by-frame render can read.
// The render never runs the physics: frame N draws table.frames[N].
//
// Usage: copy into the video project (imports resolve from the script's folder), then
//        npm i matter-js@0.20  &&  node scripts/bake-matter.mjs [fps] [seconds] [out.json]
// fps must divide into whole 1/120 s physics steps: 24, 30, 40, 60, 120.
// Prints the configuration, a progress line every second of video and a summary with a checksum:
// run it twice — the checksums must match.
import { createHash } from "node:crypto";
import { writeFileSync } from "node:fs";
import Matter from "matter-js";

const { Engine, Bodies, Composite, Body } = Matter;

const FPS = Number(process.argv[2] ?? 60);
const SECONDS = Number(process.argv[3] ?? 4);
const OUT = process.argv[4] ?? "physics.json";
const STEP_MS = 1000 / 120;                         // fixed physics step, independent of the video fps
const SUBSTEPS = Math.round(1000 / FPS / STEP_MS);   // 2 at 60 fps, 4 at 30 fps
const W = 1080, H = 1920, SEED = 7;

if (!Number.isFinite(FPS) || FPS <= 0 || !Number.isFinite(SECONDS) || SECONDS <= 0) {
  console.error("usage: node bake-matter.mjs [fps>0] [seconds>0] [out.json]");
  process.exit(2);
}

if (Math.abs(SUBSTEPS * STEP_MS - 1000 / FPS) > 1e-9) {
  throw new Error(`fps ${FPS} is not a whole number of ${STEP_MS.toFixed(3)} ms physics steps`);
}

// Seeded generator: the same seed gives the same scene on any machine.
function rng(seed) {
  return () => {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const R = rng(SEED);

const engine = Engine.create();
engine.gravity.y = 1;

const ground = Bodies.rectangle(W / 2, H - 40, W, 80, { isStatic: true, label: "ground" });
const walls = [
  Bodies.rectangle(-40, H / 2, 80, H, { isStatic: true }),
  Bodies.rectangle(W + 40, H / 2, 80, H, { isStatic: true }),
];
// Bodies are created in a fixed order: creation order is part of the simulation.
const boxes = Array.from({ length: 24 }, (_, i) => {
  const size = 60 + R() * 80;
  const b = Bodies.rectangle(120 + R() * (W - 240), -200 - i * 140, size, size,
    { restitution: 0.35, friction: 0.4, label: `box${i}` });
  Body.setAngle(b, R() * Math.PI);
  return b;
});
Composite.add(engine.world, [ground, ...walls, ...boxes]);

const round = (v, d = 2) => Math.round(v * 10 ** d) / 10 ** d;
const total = Math.round(FPS * SECONDS);
const frames = [];
console.log(`config: fps=${FPS} seconds=${SECONDS} frames=${total} step=${STEP_MS.toFixed(3)}ms ` +
  `substeps=${SUBSTEPS} bodies=${boxes.length} seed=${SEED} matter=${Matter.version}`);

for (let f = 0; f < total; f++) {
  // state at frame f is recorded before stepping, so frame 0 is the initial layout
  frames.push(boxes.map(b => [round(b.position.x), round(b.position.y), round(b.angle, 4)]));
  for (let s = 0; s < SUBSTEPS; s++) Engine.update(engine, STEP_MS);
  if ((f + 1) % FPS === 0) {
    const resting = boxes.filter(b => b.speed < 0.05).length;
    console.log(`t=${(f + 1) / FPS}s  resting ${resting}/${boxes.length}`);
  }
}

const table = {
  fps: FPS, width: W, height: H, seed: SEED,
  bodies: boxes.map(b => ({ label: b.label, size: round(Math.sqrt(b.area)) })), // square side, for drawing
  frames,                                            // frames[n][i] = [x, y, angle]
};
const json = JSON.stringify(table);
writeFileSync(OUT, json);
const sha = createHash("sha256").update(json).digest("hex").slice(0, 16);
console.log("--- summary ---");
console.log(`wrote ${OUT}: ${frames.length} frames x ${boxes.length} bodies, ${(json.length / 1024).toFixed(0)} KiB`);
console.log(`checksum ${sha} (must be identical on a second run)`);
