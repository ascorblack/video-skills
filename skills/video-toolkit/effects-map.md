# Effect → library [Toolkit]

Start from the effect the shot needs, then take the first library that gives it. A library that does not visibly improve the shot over the backbone stays out: each one adds a way to break seeking, a dependency to pin and a license to record.

## The map

| The shot needs | First choice | Alternatives | Note |
|---|---|---|---|
| Titles, kinetic type, feature cards, logo reveal | the backbone itself (Remotion `interpolate`/`spring`, HyperFrames GSAP + registry) | Anime.js for SVG/DOM paths and staggers | Most "motion design" needs no extra library |
| Elastic, springy UI motion | the backbone's spring (Remotion `spring()`; GSAP `elastic`/`back` eases) | a closed-form spring from `t` | React Spring runs on the wall clock — see `seekable-libraries.md` |
| SVG line drawing, path morphs, staggered grids | Anime.js v4 | GSAP (in HyperFrames already there) | |
| Precise vector geometry: Bézier curves, boolean path ops, drawn diagrams | Paper.js | SVG + Anime.js | Paper.js is for geometry, not for timing |
| Thousands of sprites, dense 2D scenes, 2D filters | PixiJS | p5.js for experiments | WebGL/WebGPU canvas, no timeline of its own |
| Generative and algorithmic shapes, noise fields | p5.js | PixiJS, a fragment shader | Seed `random` and `noise` |
| Dust, sparks, confetti, linked dots | tsParticles for a quick look | particles computed from `t` in PixiJS or canvas | tsParticles has no seek — bake or replace |
| GPU transitions: wipes, warps, glitch, burn | HyperFrames `@hyperframes/shader-transitions`; Remotion `@remotion/transitions` | GL Transitions shaders in your own WebGL pass | One shader for the whole video — see `SKILL.md`, "Where the sources disagree" |
| Rotating product, 3D UI, camera flights, wireframes | Three.js (`@remotion/three` in Remotion; `hf-seek` in HyperFrames) | React Three Fiber inside `@remotion/three` | Three.js does not simulate physics |
| Falling, bouncing, colliding flat objects | Matter.js, baked | Rapier 2D, baked | A physics engine does not draw |
| 3D rigid bodies: collisions, inertia, stacks | Rapier 3D (deterministic build), baked, drawn by Three.js | hand keyframes when the motion is short | |
| Voiceover | a recorded narrator or an approved TTS provider; Chatterbox locally | | The rules of verbatim reading apply to any synthesis — `video-audio`, `voiceover.md` |
| Procedural stingers, risers, rhythmic beds | Tone.js, rendered offline to WAV | recorded SFX files mixed with FFmpeg | |
| Captions and word timing from a voice track | faster-whisper with word timestamps | the TTS provider's own word timestamps (HeyGen in HyperFrames `media-use`) | Recognition, not synthesis; proofread terms |
| A real desktop program, a game, a device, a webcam | OBS Studio | | A browser interface is shot frame by frame instead — `video-ui-capture` |
| Transcoding, muxing, probing, contact sheets, loudness | FFmpeg / ffprobe | | Not named in the source, needed in every project; HyperFrames requires it |

## What a library does not do

- **Three.js** draws; it does not simulate physics and has no timeline. Its `Clock` and `AnimationMixer.update(delta)` are wall-clock — use `mixer.setTime(t)`.
- **Matter.js and Rapier** compute positions; they do not render anything and do not know about frames. Fix the step, bake, then draw.
- **GL Transitions** is a collection of GLSL fragment shaders (`vec4 transition(vec2 uv)` with a `progress` uniform). It is not an editor and has no timeline: something must capture the two scenes as textures and feed `progress` from the frame.
- **tsParticles** animates on its own loop and cannot jump to frame N.
- **React Spring** integrates springs over real time; a render that takes frames in any order gets wrong values.
- **faster-whisper** turns speech into text with timings; it does not generate voice. **Chatterbox** generates voice; it does not give word timings.
- **Tone.js** plays through Web Audio in real time unless rendered with `Tone.Offline`; a live Tone.js transport inside a frame-by-frame render is out of sync by construction.
- **OBS** records in real time; it cannot be made frame-exact afterwards.
- **p5.js** redraws on its own loop at its own `frameRate` until told `noLoop()`.

## What may be offered on request

- Animated interfaces: real recordings with callouts; menus, toggles and walkthroughs drawn only where a stylization requires it [Popsci] — a promo shows the real program [Video].
- Technical visualization: architecture diagrams, request flows, queues, graph traversals, charts — with the line rules of `video-design` (`lines-and-layout.md`).
- Motion graphics: kinetic type, morphing vector paths, moving grids, procedural shapes, shader transitions.
- 2D and 3D: dense particles, 2D physics, 3D products and wireframes, camera orbits, rigid-body simulations.
- Sound: narration, procedural stingers, music under the voice, visualizers synchronized to the track, word-timed captions.

Warn in advance about what is expensive: photoreal people, an exact replica of a complex real application, physically accurate CGI and long cinematic stories need authored assets, pre-rendered footage and far more work. A library being named does not make any of these one click.
