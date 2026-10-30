---
name: video-toolkit
description: Choosing, wiring and checking the tool stack of a code-driven video — render backbone (Remotion, HyperFrames, own renderAt harness), OBS, kinetic type (GSAP SplitText), springs, morphs (flubber), hand-drawn looks (Rough.js, p5.brush), PixiJS, particles (tsParticles), shaders and post-processing (GL Transitions, LYGIA, mesh gradients, bloom, grain, glitch, ASCII), fluids, Hydra, Three.js explainer techniques, physics (Matter.js, Rapier), Blender, Theatre.js, beat grids and audio-reactive features, music videos, character acting, Chatterbox TTS, Tone.js, faster-whisper captions; making every library frame-exact, baking simulations, the critic's frame sheets, automatic QA. Use when planning a video made with code, choosing a library or look for an effect, adding one to a frame-by-frame render, syncing animation to music, animating characters, or reviewing a render.
---

# Tool stack of a code-driven video

Unlike the other skills of this repository, the rules here are not lessons of past videos. Library facts come from a breakdown of a short about a programmable video stack and from studies of the libraries' own source, checked against the official documentation and package registries in October 2026 — label [Toolkit]. Working practices come from published agent-made videos and their repositories — label [Practice]. Where they meet a lesson of a past video, the lesson is cited next to them with its own label, and where they disagree, both are given.

## Short rules

0. At the start of a new video, offer the pre-production mode once and let the person decline it — the `video-preproduction` skill. [Practice]
1. Pick **one** render backbone — Remotion, HyperFrames, or an own `renderAt` harness for a single-canvas film — and name it in the brief, before anything else, and do not chain two renderers. [Toolkit] See `backbone.md`.
2. Add a library only for an effect the backbone does not give well, and only one per job: an effect is chosen by the table in `effects-map.md`, not the other way round. [Toolkit]
3. A library is allowed into the render only when its state can be set for an arbitrary frame N: seek it, compute it from `t`, or bake it into a table in advance. Wall clock, `requestAnimationFrame`, a library's own ticker and unseeded randomness are banned. [Toolkit] [Visual] [3D] See `seekable-libraries.md`.
4. Simulations (particles, Matter.js, Rapier) are baked: a fixed step, a fixed seed, a pass over all frames without rendering, positions in JSON, the page reads `table[frame]`. [Toolkit] [3D]
5. Before writing an effect by hand, look in the backbone's own catalog: Remotion integrations (`@remotion/three`, `@remotion/gsap`, `@remotion/lottie`, `@remotion/transitions`), HyperFrames registry and `@hyperframes/shader-transitions`. [Toolkit]
6. Shader transitions are a style of the whole video, not a slide-by-slide decoration: one shader for all joins, or a dissolve. [Toolkit] [Video] [Visual] See "Where the sources disagree".
7. OBS only for what cannot be driven by virtual time — native desktop programs, games, devices, a webcam; a browser interface is shot frame by frame. [Toolkit] [Video] [3D]
8. Local TTS (Chatterbox) is checked like any synthesis: verbatim reading by independent recognition (faster-whisper), phrases placed by the start of speech. A cloned voice — only your own or with written consent. [Toolkit] [Audio] [Popsci]
9. Captions are aligned by word timestamps of the finished voice track, then proofread by a person: terms, names and numbers recognition gets wrong. [Toolkit] [Audio]
10. Procedural sound (Tone.js) is rendered offline into a WAV and muxed in like any track; it does not play live during the render. [Toolkit] [Video]
11. Record the license of every library, shader, voice, font and model in the asset list; several of them have their own terms (Remotion company license, per-shader licenses of GL Transitions, p5.js under LGPL, the watermark in Chatterbox audio). [Toolkit]
12. The final pass is automatic and by eye: `scripts/qa.sh` (probe, black and frozen frames, loudness and true peak, contact sheet, first and last frame), then full playback. Seek consistency — two clean renders compared frame by frame with `scripts/compare-renders.sh`. [Toolkit] [Video] [3D]
13. The critic looks at frames, not at playback: labelled sheets and strips (`scripts/sheet.sh`), a written list of findings with `t=`, fix and repeat until a full pass finds nothing. [Practice] See `qa.md`.
14. Measure the music before animating to it (`scripts/beats.py`), and have a person confirm the grid by ear. [Practice] See `music-video.md`.
15. Shaders get time only from a uniform set from the frame; feedback, fluids and temporal passes carry the previous frame and are baked sequentially. [Toolkit] See `gpu-effects.md`.

## Details

- `backbone.md` — Remotion or HyperFrames or OBS; setup; what each backbone already seeks; project layout; the order of work.
- `effects-map.md` — effect → library, and what each library does not do.
- `seekable-libraries.md` — recipes that make Anime.js, springs, PixiJS, p5.js, Paper.js, particles, Three.js, GL Transitions, Matter.js and Rapier frame-exact.
- `speech-and-sound.md` — Chatterbox, Tone.js, faster-whisper: setup, the frame of a frame-by-frame video, checks.
- `gpu-effects.md` — shader time, renderer settings for 1080×1920, ShaderGradient-style gradients, LYGIA, post-processing (three.js passes, `postprocessing`), Three.js explainer techniques (exploded views, cutaways, ghosts, camera tours, ASCII), Hydra, WebGL fluid.
- `blender.md` — Blender headless as an offline asset generator: CLI render, seeds, baking, getting frames into the video.
- `music-video.md` — measuring the song, lyric timing, chapters and junctions, the frame contract, harness modes, music-video checks.
- `characters.md` — code-drawn characters: avoiding mechanical motion, emotions as data, acted transitions, model sheets, timing for the viewer.
- `qa.md` — the critic's frame sheets and what to hunt for, the automatic checks of the finished file, and what they do not see.

Scripts (`scripts/`):

- `qa.sh <video> [out-dir]` — ffprobe summary, black and frozen segments, EBU R128 loudness and true peak, a contact sheet, first and last frame.
- `compare-renders.sh <a> <b>` — compares two renders frame by frame by checksums of decoded frames and lists the frames that differ.
- `words.py <audio> [--lang ru]` — word timestamps with faster-whisper into `words.json` and `.srt` (runs through `uv run`).
- `bake-matter.mjs` — an example of baking a Matter.js scene into a per-frame JSON table.
- `sheet.sh <video> <times> [out]` — the critic's evidence: frames at chosen times, a strip `a:b` of every frame, or `a:b:step`, labelled with `t=` and the frame number; `CROP`, `WIDTH=0` for native-size detail.
- `beats.py <audio> [--fps 60]` — a constant beat grid (BPM, offset, downbeat guess) with ambiguity and drift flags, and per-frame rms, bands, onset and beat phase for audio-reactive visuals (numpy only, through `uv run`).

Related skills: frame-by-frame render pitfalls — `video-render` (`seek-render.md`); mixing and voiceover — `video-audio`; shooting an interface — `video-ui-capture`; 3D characters — `video-3d-animation`; transitions and pace — `video-design`.

## Where the sources disagree

- **Transitions.** [Video] [Visual] [Popsci]: one transition for the whole video, a dissolve by default, no scaling at the joins. [Toolkit]: GPU shader transitions (wipes, warps, glitches) are available. In promos and explainers keep the dissolve; a shader transition is for a video whose whole style is built on it (a social short, a trailer), and then it is one shader for all joins, without zoom, and the next shot still starts from the final state of the previous one.
- **Screen recording.** [Video] [3D]: a real-time screen recording tears frames, shoot frame by frame in virtual time. [Toolkit]: OBS for real software. Both hold: a browser interface — frame by frame; OBS — only for what cannot be put on virtual time, at a constant frame rate, and its footage is then inserted into the frame-by-frame render as a video file.
- **Springs.** [Toolkit] lists React Spring for elastic motion; its runtime animation runs on the wall clock and does not survive seeking [Visual]. Use the spring of the backbone (`spring()` in Remotion) or a closed-form spring computed from `t` (`seekable-libraries.md`).

## Sources

- [Toolkit] — a breakdown of a 62-second short about a programmable video stack (watermark `@mmmorozov`) and a list of libraries for video looks (GSAP, flubber, Rough.js, tsParticles, postprocessing, ShaderGradient, LYGIA, Hydra, Theatre.js, WebGL-Fluid-Simulation, Three.js, Blender); every library studied in its own source and checked against the official documentation and npm/PyPI in October 2026, with small experiments where noted. A map of possibilities: it does not prove that any particular video was made with these tools.
- [Practice] — working practices of published agent-made videos: the "frame function, rig, brief, reference, state lists, springs and sound, critic, skill" breakdown of a week of viral clips (post by @seeconvm, October 2026) and the repositories PDoomVideo, ClaudeAnimationBase, paint-mv-skills and teardown, read in October 2026.
- [Audio] — archive lessons on sound and voiceover of promo videos and presentations.
- [Video] — archive lessons on video: interface recordings, pace, transitions.
- [Visual] — archive lessons on the visuals of promo videos made of schematic frames (HTML frames → frame-by-frame render).
- [3D] — lessons of a three-dimensional first-person video in the browser (three.js → frame-by-frame render).
- [Popsci] — lessons of a video in the style of Soviet popular science and early-70s filmstrips.
