# Shaders, post-processing and GPU looks [Toolkit]

The rule of `seekable-libraries.md` holds on the GPU too: frame N is a function of N. A shader whose only time input is a uniform is frame-exact by construction; the dangers are a library that advances that uniform itself, a pass that rolls `Math.random()`, and buffers that carry the previous frame (feedback, fluids, temporal anti-aliasing).

## The renderer for 1080×1920

- `renderer.setPixelRatio(1)` and `renderer.setSize(1080, 1920, false)`: never depend on the capturing machine's `devicePixelRatio`.
- `preserveDrawingBuffer: true` when the frame is read after the draw returned (screenshots); not needed if the pixels are read in the same task as the draw.
- `outputColorSpace = SRGBColorSpace`. With an effect composer, tone mapping and colour conversion happen only in the last pass (three.js `OutputPass`, `postprocessing`'s `ToneMappingEffect`) — put it last, or the frames come out washed out or crushed.
- Dark gradients band in 8-bit video: add fine grain or a dither as the last pass, the same for every frame of the video.
- Prefer `WebGLRenderer` in headless capture. `WebGPURenderer`: `await renderer.init()` once, then call `render()` synchronously (`renderAsync` is deprecated since r181; `render` before `init` throws); drive TSL uniforms yourself instead of the built-in `time` node.
- Before the first frame: load every texture and model (`await loader.loadAsync()`), wait for fonts, and compile the shaders once (`await renderer.compileAsync(scene, camera)`), so that frame 0 is not the frame that stalls or comes out half-loaded.
- Traps that cost a re-render [Toolkit, from the teardown skill]:
  - One NaN pixel turns the whole frame black through bloom: clamp the bases of `pow()` and divisions in your shaders.
  - `smoothstep(a, b, x)` with `a > b` is undefined on ANGLE/D3D: write `1.0 - smoothstep(b, a, x)`.
  - Decals and shadow catchers inside render targets need `polygonOffset`.
  - Ambient occlusion on a clipped model needs the same clipping planes on its normal material.

## Shader time

- Every animated shader gets `uniform float uTime;` and the page sets `uTime = frame / fps` before drawing. Nothing else advances it: no `THREE.Clock`, no `THREE.Timer` (both `performance.now()`), no library `animate` loop.
- Keep time small (seconds from the start of the shot, not epoch milliseconds) — precision of `sin()`-based hashes falls apart for large arguments and differs between GPUs.
- Randomness in a shader is a hash of position, element id and a seed; for jitter that "boils" use `floor(uTime * 12.0)` as part of the hash.
- Seamless loops: make noise periodic by sampling it on a circle, `noise(vec3(p, 0) + R * vec3(cos(2π t / T), sin(2π t / T), 0))`.

### Living mesh gradients (ShaderGradient)

`@shadergradient/react` (MIT) displaces a plane with `0.75 * cnoise(pos * 0.43 * uNoiseDensity + uTime * uSpeed)`. By default (`animate="on"`) a `THREE.Clock` inside the react-three-fiber loop advances `uTime` — wall clock.

- HyperFrames: do not install the React package. Copy its noise-displacement GLSL into a plain Three.js page, stop any loop, set `uTime` in the `hf-seek` handler and call `renderer.render()` yourself.
- Remotion: `<ShaderGradientCanvas lazyLoad={false} envBasePath="/env/"><ShaderGradient animate="off" uTime={frame / fps} /></ShaderGradientCanvas>` should work (not render-tested): `lazyLoad` and `envBasePath` belong to the canvas, `animate` and `uTime` to the gradient. Every new `uTime` prop rebuilds the material; set the uniform on the mesh named `shadergradient-mesh` instead if it is slow. Serve the environment map locally — otherwise it may be fetched over the network.

### LYGIA — a shader standard library

`npm i lygia` (v1.4): noise (`snoise`, `fbm`, `curl` in 2D–4D), `distort/grain`, `distort/chromaAB`, `color/dither`, SDF, colour spaces, lighting (`envMap`, `fresnel`, `iridescence`), in GLSL, WGSL, HLSL and MSL. All functions are pure: frame-exact given the uniforms.

- **Licence:** Prosperity 3.0.0 (free non-commercial, 30-day commercial trial) or the Patron licence for sponsors and contributors; some files carry their own MIT header. Check before a commercial video and record it in the asset list.
- Resolve `#include "lygia/…"` at build time — a small regex resolver or `vite-plugin-glsl` — never through `lygia.xyz/resolve.js` at render time (network mid-render). glslify is not supported.
- The default `random()` is a `sin()` hash: define `RANDOM_SINLESS` before including it, keep time small, render all frames of one video on the same GPU model.
- There is no ready "liquid chrome": compose an fbm-warped height field → normal from its derivatives → `envMap` + `fresnel` (+ `iridescence` for an oily tint).

## Post-processing a Three.js scene

### three.js passes (`three/addons/postprocessing/`)

- `EffectComposer.render()` without an argument reads its own timer: always `composer.render(0)`.
- `UnrealBloomPass`, `OutputPass` — no time, no randomness: deterministic.
- `FilmPass` has a `time` uniform the pass does not drive from the frame: set `filmPass.uniforms.time.value = t` before rendering.
- `GlitchPass` uses `Math.random()` and its own frame counter; `AfterimagePass` and TAA keep history — none of them seek. Write a `ShaderPass` with a seeded hash instead.

### The `postprocessing` library (pmndrs, Zlib, 6.39.5: peer `three >=0.168 <0.187` — pin three below r187)

```js
import { EffectComposer, RenderPass, EffectPass, BloomEffect, NoiseEffect, ChromaticAberrationEffect } from "postprocessing";

const composer = new EffectComposer(renderer, { frameBufferType: THREE.HalfFloatType });
composer.addPass(new RenderPass(scene, camera));
const fx = new EffectPass(camera, new BloomEffect({ intensity: 1.2 }), new NoiseEffect({ premultiply: true }));
composer.addPass(fx);

function renderAt(t) {                  // called from the seek handler
  fx.fullscreenMaterial.time = t;       // absolute time, not += delta
  composer.render(0);                   // never without an argument
}
```

- Each `EffectPass` adds `deltaTime` to its material's `time`: set `time` to the absolute frame time and pass 0.
- `NoiseEffect` depends only on uv and time — frame-exact once `time` is set.
- `GlitchEffect` calls `Math.random()` every frame (and in its constructor and perturbation texture); its default `SPORADIC` mode also accumulates time. Use `GlitchMode.CONSTANT_WILD` or `CONSTANT_MILD`, switch it on and off from the frame, replace `Math.random` with `rng(frame)` around `composer.render`, and seed before constructing it (or pass your own `perturbationMap`).
- `OutlineEffect` pulse and adaptive tone mapping keep history — avoid them.
- `@react-three/postprocessing` renders in `useFrame` with the real delta and its `<Glitch>` defaults to `SPORADIC`: in Remotion use it only for static effects (Bloom, Vignette, ToneMapping) and set time-varying ones through refs.

## Three.js techniques for explainers [Toolkit, from the teardown skill]

- **One input drives everything:** a single eased scalar per idea (`explode`, `cut`, `xray`) computed from `t`; parts, labels, camera and sound read the same scalar, so nothing drifts apart.
- **Exploded view / assembly:** each part has an offset vector; position = rest + offset × `explode`. Assembly is the same scalar reversed, staggered per part with an overshoot ease.
- **Cutaway section with solid caps:** one `THREE.Plane` shared as `material.clippingPlanes` (and `renderer.localClippingEnabled = true`); per solid part two stencil twins (`BackSide` increments, `FrontSide` decrements, `colorWrite: false`), then a cap plane on the cut drawn where the stencil is not zero.
- **Isolate / ghost:** clone the materials with `transparent: true, depthWrite: false`; swap them on the parts to hide and fade their opacity from the frame.
- **Camera tours:** named views `{ target, azimuth, elevation, distance }` as functions of local time; blend between them along the shortest azimuth, with a small "back-off" (`distance += k * sin(π p)`) on big moves so the camera swings around the model instead of cutting through it.
- **Punch-ins:** re-render a sub-rectangle with `camera.setViewOffset()` instead of scaling the finished frame with CSS — the detail stays sharp.
- **ASCII render:** `AsciiEffect` from `three/addons/effects/AsciiEffect.js` — `effect.setSize(W, H)`, `effect.render(scene, camera)`, and show `effect.domElement` (a DOM table of characters) instead of the canvas. Deterministic; keep `resolution` ≤ 0.15 and `color: false` for speed; install the same monospace font on every render machine.

## Hydra — live-coding visuals (`hydra-synth` 1.4, AGPL-3.0)

```js
const hydra = new Hydra({ canvas, autoLoop: false, detectAudio: false,
                          enableStreamCapture: false, makeGlobal: false });
const h = hydra.synth;
let A = { bands: [0], rms: 0, onset: 0 };
h.osc(8, 0.1, 1.2).kaleid(5).modulate(h.noise(3), () => A.bands[0] * 0.4).out();

function renderAt(t, frame) {
  const f = audio.frames;         // baked features (scripts/beats.py): one array per feature
  A = { bands: f.bands[frame], rms: f.rms[frame], onset: f.onset[frame] };
  h.time = t;
  hydra.tick(0);                 // synchronous draw at that time
}
```

- Set `synth.time`, then `tick(0)`; never set `synth.fps` (a frame is then silently skipped); `window.time` does nothing.
- Patches without feedback seek freely. **Feedback** (`src(o0)` reading its own output) accumulates: every `tick` advances it, even at the same time. Render feedback patches once, in order, in a single process, and use the result as a video layer.
- `a.fft` is the live microphone: replace it with features baked from the soundtrack (`scripts/beats.py` → per-frame bands, rms, onset), passed through function parameters `() => A.bands[0]`.
- 8-bit feedback buffers band in dark trails; pixel ratio is fixed at 1; read the canvas in the same task as `tick` (no `preserveDrawingBuffer`).
- AGPL: fine for rendering a video; do not ship the bundle inside a product.

## WebGL fluid and smoke (PavelDoGreat/WebGL-Fluid-Simulation, MIT)

A single-file demo: velocity, dye and pressure live in ping-pong framebuffers, so every frame is built from the previous ones — it cannot seek.

- Fork `script.js`: remove the `update()` `requestAnimationFrame` loop and the `Date.now()` delta; call `step(1 / 60)` once per 60 fps frame; replace the five `Math.random()` calls (random splats, `generateColor()`) with a seeded stream; replace pointer input with scripted `splat(x, y, dx, dy, color)` calls from the shot table; call `render(null)` to draw.
- Pin the quality settings: on a GPU without float textures the demo silently turns off bloom and sunrays and drops the dye resolution — throw instead.
- **Bake:** simulate once, sequentially, and write a PNG sequence or an alpha video; the composition then plays it as an ordinary video layer. Never simulate live inside a parallel render — each worker would start from empty buffers, and half-float results differ between GPUs.
