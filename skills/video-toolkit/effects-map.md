# Effect → library [Toolkit]

Start from the effect the shot needs, then take the first library that gives it. A library that does not visibly improve the shot over the backbone stays out: each one adds a way to break seeking, a dependency to pin and a license to record.

## The map

Details and seek recipes for every library named here: `seekable-libraries.md` (motion, 2D, particles, physics), `gpu-effects.md` (shaders, post-processing, Three.js looks, fluid, Hydra), `blender.md` (offline 3D).

### Type and motion

| The shot needs | First choice | Alternatives | Note |
|---|---|---|---|
| Titles, feature cards, logo reveal | the backbone itself (Remotion `interpolate`/`spring`, HyperFrames GSAP + registry) | Anime.js for SVG/DOM paths and staggers | Most "motion design" needs no extra library |
| Kinetic type: letter, word or line staggers, masked line reveals | HyperFrames: GSAP `SplitText` (`chars`/`words`/`lines`, `mask`) | Remotion: split the string in React, `spring()`/`interpolate()` per character | Split after `await document.fonts.ready`; random stagger orders are unseeded — `seekable-libraries.md`, GSAP |
| Decode / scramble text | your own pure function of (frame, seed) | | GSAP `ScrambleTextPlugin` uses `Math.random` and depends on seek history: not frame-exact |
| Elastic, springy motion with mass | closed-form springs per object class (`seekable-libraries.md`, Springs) | Remotion `spring()`; GSAP `elastic`/`back` eases | React Spring runs on the wall clock |
| Camera paths authored by a person on a timeline | Theatre.js (`@theatre/core`), state JSON seeked by `sequence.position` | your own keyframe/Bézier function — lighter for agent-only work | Unmaintained since 2024; studio is AGPL, keep it out of the render |

### Vector and 2D

| The shot needs | First choice | Alternatives | Note |
|---|---|---|---|
| SVG draw-on, path morphs between similar shapes | HyperFrames: GSAP `DrawSVGPlugin`, `MorphSVGPlugin` (free since GSAP 3.13) | Anime.js v4 | `@remotion/gsap` does not support GSAP plugins |
| Morph between unlike shapes, one shape into many, shape into circle or rectangle | flubber (`interpolate`, `separate`, `combine`, `interpolateAll`, `toCircle`) | MorphSVG | Pure function of `t`; output is a polygon — `maxSegmentLength` 2–4 for large shapes |
| Hand-drawn sketch look: diagrams, scribbled callouts, "boiling" lines | Rough.js with a fixed non-zero `seed` | p5.brush for painted strokes | `seed: 0` and `fillStyle: 'dots'` fall back to `Math.random` |
| Precise vector geometry: Bézier curves, boolean path ops | Paper.js | SVG + Anime.js | Paper.js is for geometry, not for timing |
| Thousands of sprites, dense 2D scenes, 2D filters | PixiJS | p5.js for experiments | WebGL/WebGPU canvas, no timeline of its own |
| Generative and algorithmic shapes, noise fields | p5.js | PixiJS, a fragment shader | Seed `random` and `noise` |
| Hand-painted cartoon look | p5.js + p5.brush, seed per element, linework boiling at 12 Hz | | Every element its own seed key — `seekable-libraries.md` |

### Particles and fluids

| The shot needs | First choice | Alternatives | Note |
|---|---|---|---|
| Dust, sparks, drifting dots | particles computed from `t` (analytic) | PixiJS `ParticleContainer` from formulas | Cheapest and seekable by construction |
| Confetti, emitter bursts, linked-dot networks | tsParticles v4 stepped by hand with a seeded random | baked simulation | Replay from frame 0; contiguous frame ranges per worker |
| Smoke, ink, liquid swirls following a path | WebGL-Fluid-Simulation (MIT) forked, baked sequentially to video | Blender fluid/smoke, rendered | Cannot seek; never simulate live in a parallel render |

### Shaders, looks and post-processing

| The shot needs | First choice | Alternatives | Note |
|---|---|---|---|
| Living mesh gradient, liquid background | a vertex-noise shader with `uTime` from the frame (ShaderGradient's GLSL, MIT) | `@shadergradient/react` with `animate="off"` (Remotion) | The React component is clock-driven by default |
| Noise, fbm, curl, grain, dither, SDF, chrome-like metal as GLSL building blocks | LYGIA functions resolved at build time | your own GLSL | Licence: Prosperity / Patron — check before commercial use |
| Bloom, film grain, vignette, chromatic aberration on a Three.js scene | `postprocessing` `EffectComposer` driven from the frame | three.js `UnrealBloomPass`, `FilmPass` + `OutputPass` | `composer.render(0)` and set the shader time yourself |
| Glitch, VHS, RGB split | a seeded custom shader pass gated by the frame | `postprocessing` `GlitchEffect` in a `CONSTANT_*` mode with seeded random | three.js `GlitchPass` and the default `SPORADIC` mode cannot seek |
| ASCII or terminal render of a 3D scene | three.js `AsciiEffect` | a fragment shader that maps luminance to a glyph atlas | Deterministic but slow with `color: true`; pin the monospace font |
| Feedback trails, kaleidoscopes, beat-reactive abstract backgrounds | Hydra (`hydra-synth`) with `autoLoop: false`, time set per frame | a custom shader with baked audio features | Feedback patches accumulate: bake sequentially; AGPL |
| GPU transitions: wipes, warps, glitch, burn | HyperFrames `@hyperframes/shader-transitions`; Remotion `@remotion/transitions` | GL Transitions shaders in your own WebGL pass | One shader for the whole video — see `SKILL.md`, "Where the sources disagree" |

### 3D and physics

| The shot needs | First choice | Alternatives | Note |
|---|---|---|---|
| Rotating product, 3D UI, camera flights, wireframes | Three.js (`@remotion/three` in Remotion; `hf-seek` in HyperFrames) | React Three Fiber inside `@remotion/three` | Three.js does not simulate physics |
| Exploded view, assembly, cutaway section, ghosted parts | Three.js: per-part offsets from one eased scalar; clipping plane with stencil caps; transparent "ghost" twins | Blender for photoreal versions | One input drives everything — `gpu-effects.md`, Three.js techniques |
| Falling, bouncing, colliding flat objects | Matter.js, baked | Rapier 2D, baked | A physics engine does not draw |
| 3D rigid bodies: collisions, inertia, stacks | Rapier 3D (deterministic build), baked, drawn by Three.js | hand keyframes when the motion is short | |
| Photoreal 3D: real light, glass, shatter, smoke, volumetrics | Blender CLI → PNG/EXR sequence → a video layer in the backbone | Blender bake → per-frame matrices JSON → Three.js `InstancedMesh` | An offline asset generator, not a second backbone — `blender.md` |

### Sound, speech, capture

| The shot needs | First choice | Alternatives | Note |
|---|---|---|---|
| Animation on the beat, beat-reactive visuals | `scripts/beats.py`: constant beat grid + per-frame rms/bands/onset JSON | a hand-set BPM and offset checked by ear | Measure first, then animate; confirm the grid by ear |
| Voiceover | a recorded narrator or an approved TTS provider; Chatterbox locally | | The rules of verbatim reading apply to any synthesis — `video-audio`, `voiceover.md` |
| Procedural stingers, risers, rhythmic beds | Tone.js, rendered offline to WAV | recorded SFX files mixed with FFmpeg | |
| Captions, word timing, lyric alignment | faster-whisper with word timestamps (`scripts/words.py`) | the TTS provider's own word timestamps (HeyGen in HyperFrames `media-use`) | Recognition, not synthesis; ~0.3 s error on sung lyrics — a draft, proofread |
| A real desktop program, a game, a device, a webcam | OBS Studio | | A browser interface is shot frame by frame instead — `video-ui-capture` |
| Transcoding, muxing, probing, contact sheets, loudness | FFmpeg / ffprobe; `scripts/qa.sh`, `scripts/sheet.sh` | | Needed in every project; HyperFrames requires it |

## What a library does not do

- **Three.js** draws; it does not simulate physics and has no timeline. `Clock`, `Timer` and `AnimationMixer.update(delta)` are wall-clock — use `mixer.setTime(t)`. `EffectComposer.render()` without an argument reads a timer.
- **Matter.js and Rapier** compute positions; they do not render anything and do not know about frames. Fix the step, bake, then draw.
- **GL Transitions** is a collection of GLSL fragment shaders (`vec4 transition(vec2 uv)` with a `progress` uniform). It is not an editor and has no timeline: something must capture the two scenes as textures and feed `progress` from the frame.
- **tsParticles** has no seek: it can be stepped by hand from frame 0, never jumped to frame N.
- **React Spring** integrates springs over real time; a render that takes frames in any order gets wrong values.
- **faster-whisper** turns speech into text with timings; it does not generate voice. **Chatterbox** generates voice; it does not give word timings.
- **Tone.js** plays through Web Audio in real time unless rendered with `Tone.Offline`; a live Tone.js transport inside a frame-by-frame render is out of sync by construction.
- **OBS** records in real time; it cannot be made frame-exact afterwards.
- **p5.js** redraws on its own loop at its own `frameRate` until told `noLoop()`; in 2.x `redraw()` is asynchronous.
- **postprocessing** reads `performance.now()` when `render()` gets no delta; its `GlitchEffect` calls `Math.random()` every frame.
- **Hydra** reads the live microphone for `a.fft` and its feedback buffers carry the previous frame.
- **WebGL-Fluid-Simulation** is a demo page, not a library: it starts its own loop at load and takes `dt` from `Date.now()`.
- **Theatre.js** `onValuesChange` and `sequence.play()` run on its own ticker; only `sequence.position` + `obj.value` is synchronous.
- **Blender** renders frames; its physics caches must be baked and saved before a frame range is rendered in parallel.

## What may be offered on request

- Animated interfaces: real recordings with callouts; menus, toggles and walkthroughs drawn only where a stylization requires it [Popsci] — a promo shows the real program [Video].
- Technical visualization: architecture diagrams, request flows, queues, graph traversals, charts — with the line rules of `video-design` (`lines-and-layout.md`).
- Motion graphics: kinetic type, morphing vector paths, moving grids, procedural shapes, shader transitions.
- 2D and 3D: dense particles, 2D physics, 3D products and wireframes, camera orbits, rigid-body simulations.
- Sound: narration, procedural stingers, music under the voice, visualizers synchronized to the track, word-timed captions.

Warn in advance about what is expensive: photoreal people, an exact replica of a complex real application, physically accurate CGI and long cinematic stories need authored assets, pre-rendered footage and far more work. A library being named does not make any of these one click.
