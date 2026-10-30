# Making a library frame-exact [Toolkit]

A frame-by-frame render asks for frame N, possibly out of order, possibly in several processes, possibly twice. A library is fit for it only when its state at N can be produced without playing frames 0…N−1 in real time. There are three ways, in order of preference:

1. **Seek** — the library has a paused timeline with a `seek(time)`; the backbone or your code calls it.
2. **Compute from `t`** — the scene is a pure function `draw(t)`: positions come from formulas and seeded random numbers, nothing accumulates between frames.
3. **Bake** — anything that integrates over time (physics, particle simulations, smoothing) runs once, offline, at a fixed step, and writes a table `frame → state`; the page only reads `table[frame]`. This is what the lessons did for the poses of 3D characters [3D] (the `video-3d-animation` skill, `motion.md`).

Shaders, post-processing, Three.js looks, fluids and Hydra are in `gpu-effects.md`; Blender in `blender.md`.

Always banned inside the render: `Date.now()`, `performance.now()`, `requestAnimationFrame` loops, a library's own ticker, `setInterval`, unseeded `Math.random()`, network requests mid-render [Visual] [Popsci].

Where the time comes from:

- **Remotion:** `const frame = useCurrentFrame(); const { fps } = useVideoConfig(); const t = frame / fps;`
- **HyperFrames:** a paused GSAP timeline is seeked by the runtime. For a library HyperFrames does not seek, drive it from that timeline with one proxy tween whose `onUpdate` draws the state at the tween's time (the same proxy-tween device as in `video-render`, `seek-render.md` [Visual]), or listen to the runtime's `hf-seek` event, which carries `detail.time` and `detail.waitUntil(promise)` for asynchronous work. Check the installed `/hyperframes` skill for the current registration rules before relying on either.

## Seeded random numbers

Every library below that needs randomness gets it from one seeded generator, re-created from the seed for every frame, so that the sequence of numbers does not depend on which frames were drawn before:

```js
// mulberry32: tiny, fast, deterministic across machines
function rng(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
```

Per-object constants (start position, speed, phase) are drawn once from `rng(SEED)` at load; per-frame noise (grain, flicker) from `rng(SEED ^ frame)` [Popsci].

Give every element its own seed key rather than drawing all of them from one shared stream [Toolkit]: with a shared stream, an element that appears, disappears or draws one more stroke shifts the random numbers of everything drawn after it, and unrelated parts of the frame start to jump. Hash the key: `rng(hash(elementId) ^ boilIndex)`.

**Boiling lines** — the hand-drawn jitter of cartoons and sketches — come from changing the seed a few times a second, not every frame: `boilIndex = Math.floor(t * 12)` (12 Hz, "on twos" at 24 fps) [Toolkit]. The jitter is then lively but still a pure function of `t`.

## Anime.js (v4)

- Create every animation and timeline with `autoplay: false`; drive it with `.seek(ms)`.
- v4 is a namespace (`animate`, `createTimeline`, `stagger`), not the v3 `anime({ targets })` call; old snippets do not run.
- HyperFrames seeks Anime.js v4 only for instances pushed to `window.__hfAnime`; an instance not in that array stays at its first frame.
- In Remotion: build the timeline once (`useMemo`), then `tl.seek(frame / fps * 1000)` in a layout effect on every frame.
- `stagger({ from: 'random' })` and random values in keyframes must be replaced with values from the seeded generator.

## Springs instead of React Spring

React Spring advances its springs on `requestAnimationFrame`; a frame requested out of order gets whatever state the spring happened to be in. Replace it:

- Remotion: `spring({ frame, fps, config: { damping, stiffness, mass } })` — computed from the frame number.
- GSAP (HyperFrames): `elastic.out(1, 0.4)` or `back.out(1.7)` eases on a seeked tween.
- Anywhere: a closed-form damped spring, from rest at 0 to target 1:

```js
// zeta < 1: underdamped (overshoots); omega: natural frequency, rad/s
function springAt(t, omega = 12, zeta = 0.45) {
  if (t <= 0) return 0;
  if (zeta >= 1) return 1 - Math.exp(-omega * t) * (1 + omega * t);   // critically damped: no overshoot
  const wd = omega * Math.sqrt(1 - zeta * zeta);
  return 1 - Math.exp(-zeta * omega * t) *
    (Math.cos(wd * t) + (zeta * omega / wd) * Math.sin(wd * t));
}
```

### Springs by object class [Toolkit]

A fixed easing curve slides from A to B; motion with mass accelerates, overshoots a little and settles. Give each class of object its own spring and keep it the same for the whole video (record it in the style bible, `video-preproduction`):

| Object | Behaviour | Starting point for `springAt(t, omega, zeta)` | Overshoot, settles within 1 % |
|---|---|---|---|
| Small UI (toggles, chips, cursors' targets) | quick, almost no overshoot | `omega 22, zeta 0.85` | 0.6 %, 0.20 s |
| Panels, cards, windows | settle with a small overshoot | `omega 14, zeta 0.7` | 4.6 %, 0.47 s |
| Camera | a glide, overshoot invisible | `omega 6, zeta 1.0` (critically damped) | none, 1.1 s |
| Titles | land hard and hold long enough to be read | `omega 18, zeta 0.9`, then a hold [Visual] | 0.2 %, 0.28 s |
| Mascots, characters, playful props | bounce on purpose | `omega 10, zeta 0.35` | 31 %, 1.15 s |

The overshoot and settling times are computed from the formula above; the choice of numbers per class is a starting point, not a lesson: tune them on a strip of frames around the move (`scripts/sheet.sh video a:b`).

When the target changes several times (a cursor moving between buttons, a container changing width), do not restart one spring from zero — that jumps. Sum one spring per change, each starting at the moment of its change; the result is still a pure function of `t`:

```js
// changes: [{ t: 0, to: 0 }, { t: 1.2, to: 300 }, { t: 2.0, to: 120 }] — value starts at changes[0].to
function springTrack(t, changes, omega, zeta) {
  let v = changes[0].to;
  for (let i = 1; i < changes.length; i++) {
    const c = changes[i];
    v += (c.to - changes[i - 1].to) * springAt(t - c.t, omega, zeta);
  }
  return v;
}
```

## GSAP [Toolkit]

GSAP 3.13+ ships every former bonus plugin (SplitText, MorphSVG, DrawSVG, ScrambleText, CustomEase…) in the `gsap` npm package under Webflow's no-charge licence: free for commercial videos; it is not MIT, and the one forbidden use is building a no-code animation tool that competes with Webflow.

- Build one master timeline with `paused: true` and seek it with `tl.time(frame / fps)`. No `play()`, no `delayedCall()`, no free-standing `gsap.to()` outside the timeline; `gsap.ticker.remove(gsap.updateRoot)` freezes anything that slipped through.
- `from()` and `fromTo()` apply their start values lazily: call `tl.time(0)` once after building, before the first capture, or the first frame shows the end state.
- `stagger: { from: "random" }`, `"random(…)"` strings, `gsap.utils.random()` and `shuffle()` use unseeded `Math.random()` when the timeline is built: precompute the order with the seeded generator and pass explicit values, or seed `Math.random` while building.
- `ScrambleTextPlugin` is not frame-exact: random and dependent on the history of seeks. Write the decode effect as a function of (frame, character index, seed).
- `SplitText`: split after `await document.fonts.ready` (a fallback font gives other line breaks); turn off `autoSplit` re-splitting during the render; for line reveals use `mask: "lines"` and animate `yPercent` from 100.
- `time` ignores repeats, `totalTime` includes them, `progress` is 0–1 of one iteration: seek the master timeline by `time` and avoid `repeat: -1` in a render.
- In Remotion, `@remotion/gsap` (`useGsapTimeline`) rejects playback methods, callbacks and random strings, and does not support GSAP plugins: split text in React instead of SplitText.

## PixiJS (v8)

- `const app = new Application(); await app.init({ width, height, autoStart: false, background: '#000' });` — the shared ticker does not start; do not add ticker callbacks.
- On each frame: set positions, alphas, filter uniforms from `t`, then `app.render()` once.
- Load every texture before the first frame (`await Assets.load([...])`) and only then report the composition ready.
- Large particle counts: a `ParticleContainer` with particles positioned from formulas of `t`, not from velocities accumulated per tick.

## p5.js

- Instance mode, so that several sketches and the backbone do not fight over globals. In `setup`: `createCanvas(w, h); noLoop(); pixelDensity(1);`.
- Never use `frameCount`, `millis()` or `deltaTime`; keep a variable `t` set by the backbone and call `await p.redraw()` after setting it. In p5.js 2.x `redraw()` is asynchronous: it returns before `draw()` has run, so a frame captured without awaiting it shows the previous state. In HyperFrames hand the promise to the runtime: `detail.waitUntil(p.redraw())` inside the `hf-seek` listener.
- At the top of `draw()` call `randomSeed(SEED)` and `noiseSeed(SEED)`: otherwise the next frame continues the random sequence of whichever frame was drawn before, and two renders differ.
- p5.js is LGPL-2.1: record it in the asset list.
- **p5.brush** (painted, watercolour strokes) hooks p5's `randomSeed` and `noiseSeed`; without them its own generator is seeded from `Math.random()` at load. Seed per element and boil at 12 Hz (above). Software-rendered (SwiftShader) frames of the same `t` came out visually equal but not bit-identical: compare such renders by PSNR, not by checksums.

## Paper.js

- Do not use `view.onFrame` (it runs on the browser's loop). `autoUpdate = false` alone does not stop that loop — `onFrame` handlers keep firing; also call `paper.view.pause()`. Set `paper.view.autoUpdate = false`, change items from `t` (`path.segments`, `path.smooth()`, `item.position`), then `paper.view.update()`.
- For a "drawn line" effect use `path.getPointAt(path.length * p)` or a dash offset from `p`, where `p` comes from the frame.

## flubber [Toolkit]

`flubber.interpolate(fromPath, toPath, { maxSegmentLength })` returns a pure function `p → d` (0 ≤ p ≤ 1): build it once outside the frame function, call it per frame with an eased progress and set the `d` attribute. Also `separate` (one shape into many), `combine` (many into one), `interpolateAll` (N to N), `toCircle`/`toRect`/`fromCircle`/`fromRect`. The output is a polygon (`M…L…Z`): for large shapes at 1080×1920 set `maxSegmentLength` to 2–4 px (the default 10 shows facets). Only the first outer subpath is used — no holes. Never use d3 transitions from its demos. MIT, v0.4.2, finished and stable.

## Rough.js [Toolkit]

Hand-drawn shapes on SVG or canvas; a pure function of its arguments, no clock. MIT, v4.6.6.

- Pass a **non-zero integer `seed` on every call**: `seed: 0` (the default) or a missing seed falls back to `Math.random()`.
- Avoid `fillStyle: 'dots'`: it calls `Math.random()` even with a seed. `hachure`, `solid`, `zigzag`, `cross-hatch`, `dashed`, `zigzag-line` are deterministic.
- Boiling line: `seed = 1 + Math.floor(frame / HOLD) * 31 + id * 7919`, `HOLD` 5–8 frames at 60 fps.
- Draw-on: fix the seed while drawing, generate SVG paths, animate `strokeDashoffset` from `path.getTotalLength()` to 0 on the paused timeline.
- At 1080×1920 use `strokeWidth` 4–8 and `preserveVertices: true`. In Remotion render `generator.toPaths()` into `<path>` elements in JSX; in HyperFrames redraw synchronously in the seek handler, clearing the canvas first.
- Excalidraw draws with Rough.js, so its SVG export can be animated the same way (not tested).

## tsParticles and particles in general

tsParticles has no "go to frame N"; left alone it runs its own loop and a seeked render shows particles wherever the loop left them. v4 can be stepped by hand [Toolkit]:

```js
import { confetti } from "@tsparticles/confetti";
import { setRandom, setAnimationFunctions } from "@tsparticles/engine";

setRandom(rng(42));                                  // before anything is created
setAnimationFunctions(() => 1, () => {});            // swallow the engine's requestAnimationFrame loop
const fire = await confetti.create(canvas, {});
const container = await fire({ count: 80, spread: 90, startVelocity: 45, origin: { x: 0.5, y: 0.7 } });
container.pause();

function step() {                                    // one video frame
  const ms = 1000 / FPS;
  container.addLifeTime(ms);
  container.canvas.render.drawParticles({ value: ms, factor: 60 / FPS });
}
```

- Frame N = a fresh container + N steps. It is a replay, not random access: give each render worker a contiguous range and let it replay from 0, or bake positions.
- The engine draws on an `OffscreenCanvas`: wait two `requestAnimationFrame`s before capturing (in HyperFrames inside `detail.waitUntil`), an immediate read returned a stale frame.
- `container.canvas.render.drawParticles` is not documented API — pin the version (verified on `@tsparticles/confetti` 4.5.0: identical state and pixels across fresh pages). `fpsLimit` and `draw(force)` do not help: both still follow the wall clock.

For plain dust and sparks the analytic recipe below is cheaper and seeks freely:

- **Analytic particles** (preferred for dust, sparks, drifting dots): each particle gets constants from the seeded generator; its position at `t` is a formula, with wrap-around by modulo:

```js
const R = rng(42);
const P = Array.from({ length: 800 }, () => ({
  x: R() * W, y: R() * H, vx: (R() - 0.5) * 30, vy: -10 - R() * 40,
  phase: R() * Math.PI * 2, life: 2 + R() * 3,
}));
function particlesAt(t) {
  return P.map(p => {
    const age = (t + p.phase) % p.life;              // respawn cycle
    return {
      x: ((p.x + p.vx * t) % W + W) % W,
      y: ((p.y + p.vy * t) % H + H) % H,
      a: Math.sin(Math.PI * age / p.life),             // fade in and out
    };
  });
}
```

- **Baked** (for collisions, attraction, linked-dot networks): simulate at a fixed step offline and store positions per frame, as for physics below.

## Three.js

- Remotion: `@remotion/three` and `<ThreeCanvas>`; inside it, read `useCurrentFrame()` and set the camera and objects from it. Video textures through Remotion's own video components, not a playing `<video>`.
- HyperFrames: the runtime seeks Three.js through the `hf-seek` event. Render the scene inside the `hf-seek` handler for `detail.time`. Do not count on the runtime to wait for textures and models: its loading check reads counters that the stock `THREE.DefaultLoadingManager` keeps private, so load every asset yourself (`await loader.loadAsync(...)`) before reporting the composition ready, and pass any per-seek asynchronous work to `detail.waitUntil(promise)`.
- No `THREE.Clock`, no `clock.getDelta()`, no `controls.update()` with damping. Animated glTF: `mixer.setTime(t)`, never `mixer.update(delta)`.
- Camera paths: a `CatmullRomCurve3` sampled at an eased `p(t)`; look-at targets from the same `p`.
- Textures from canvases may arrive torn or black at frame capture when they live in GPU memory; keep them in CPU memory [Popsci] (the `video-render` skill).

More for Three.js — post-processing, ASCII renders, exploded views and cutaways, renderer settings for 1080×1920 — in `gpu-effects.md`.

## Theatre.js [Toolkit]

A keyframe timeline with a visual editor for camera paths and props. `@theatre/core` and `@theatre/r3f` are Apache-2.0; `@theatre/studio` (the editor) is AGPL-3.0 — use it only to author, never load it in the render page. Unmaintained since 2024 (last release 0.7.2; `@theatre/r3f` needs react-three-fiber v8).

- Seek: `sheet.sequence.position = seconds`, then read `obj.value` — synchronous, no ticker (verified in plain Node, out-of-order positions gave identical values).
- Never use `obj.onValuesChange`, `sequence.play()` or r3f `editable` in a render: they run on Theatre's ticker and coalesce seeks.
- Load the exported state with `getProject(id, { state })`. The state JSON can be written by hand, but 0.7.2 expects `keyframes` as an **array**; the `{byId, allIds}` shape of the unreleased main branch, a wrong object key or a wrong prop path all silently give the defaults — check one known value after loading.
- Worth it when a person wants to scrub and tweak a camera in the studio. For agent-only work a 30-line keyframe/Bézier function of your own is lighter.

## GL Transitions

- `npm i gl-transitions` gives an array of transitions: `{ name, glsl, params, license, … }`. Version 2.0 renamed everything to PascalCase (`crosswarp` → `CrossWarp`, `burn` → `FlashFade`, `fragment` → `Shatter`); older snippets with lowercase names do not resolve.
- Each shader implements `vec4 transition(vec2 uv)` and expects your wrapper to provide `uniform float progress`, `uniform float ratio`, and functions `getFromColor(uv)` / `getToColor(uv)` that sample the two scenes. The package also ships GLSL ES 3.00 variants (for `THREE.GLSL3`), SkSL and WGSL.
- `progress` comes from the frame: `p = clamp((frame - start) / length, 0, 1)`, eased. Both scenes must be textures of their own state at that same frame, not stills from before the join — otherwise the motion freezes for the length of the transition.
- Each transition carries its own `license` field: check it per shader, not per package.
- In HyperFrames prefer `@hyperframes/shader-transitions` (`init({ bgColor: "#000", scenes, transitions: [{ time, shader, duration }] })` — `bgColor` is required, 14 shaders, GSAP-driven, falls back to a plain cut without WebGL). In Remotion prefer `@remotion/transitions`; write your own WebGL pass only for a look neither has.

## Matter.js — bake

- Fixed step: `Engine.update(engine, 1000 / 60)` — the delta is in milliseconds and must never come from the clock. For a 30 fps video do two 1/60 steps per frame; for 60 fps, one.
- Same body creation order, same parameters, same version → same result on the same machine. Do not bake on one machine and re-simulate on another; ship the table.
- Bake all frames in one pass and write `[{ id, x, y, angle }]` per frame; the page draws the table. `scripts/bake-matter.mjs` is a working example.

## Rapier — bake

- For results identical across machines use the deterministic builds: `@dimforge/rapier3d-deterministic-compat` or `@dimforge/rapier2d-deterministic-compat` (the `-compat` builds embed the WASM; `await RAPIER.init()` first).
- `world.timestep = 1 / 60;` then `world.step()` once per step; never pass a measured delta.
- Record `body.translation()` and `body.rotation()` per frame into the table. In Rapier 3D the rotation is a quaternion — Three.js sets `mesh.position` and `mesh.quaternion` from it; in Rapier 2D it is an angle in radians — set `mesh.rotation.z`.
- Pin the exact version: a different Rapier version is a different simulation.

## Check that seeking really works

- Render the representative shot twice from clean processes and compare frame by frame: `scripts/compare-renders.sh a.mp4 b.mp4`. Any differing frame is a leak of clock or randomness.
- Render the same shot with frames requested in a different order (more workers, or a sub-range that starts mid-shot) and compare again: an accumulating state passes the first test and fails this one.
- Look at frames in the middle of motion, not only at the end states [Visual].
