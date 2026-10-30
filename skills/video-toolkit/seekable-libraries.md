# Making a library frame-exact [Toolkit]

A frame-by-frame render asks for frame N, possibly out of order, possibly in several processes, possibly twice. A library is fit for it only when its state at N can be produced without playing frames 0…N−1 in real time. There are three ways, in order of preference:

1. **Seek** — the library has a paused timeline with a `seek(time)`; the backbone or your code calls it.
2. **Compute from `t`** — the scene is a pure function `draw(t)`: positions come from formulas and seeded random numbers, nothing accumulates between frames.
3. **Bake** — anything that integrates over time (physics, particle simulations, smoothing) runs once, offline, at a fixed step, and writes a table `frame → state`; the page only reads `table[frame]`. This is what the lessons did for the poses of 3D characters [3D] (the `video-3d-animation` skill, `motion.md`).

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
  const wd = omega * Math.sqrt(1 - zeta * zeta);
  return 1 - Math.exp(-zeta * omega * t) *
    (Math.cos(wd * t) + (zeta * omega / wd) * Math.sin(wd * t));
}
```

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

## Paper.js

- Do not use `view.onFrame` (it runs on the browser's loop). `autoUpdate = false` alone does not stop that loop — `onFrame` handlers keep firing; also call `paper.view.pause()`. Set `paper.view.autoUpdate = false`, change items from `t` (`path.segments`, `path.smooth()`, `item.position`), then `paper.view.update()`.
- For a "drawn line" effect use `path.getPointAt(path.length * p)` or a dash offset from `p`, where `p` comes from the frame.

## tsParticles and particles in general

tsParticles runs its own animation loop and has no "go to frame N": a seeked render shows particles where the loop happened to leave them. Use it to sketch the look, then:

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
