---
name: video-toolkit
description: Choosing and wiring the tool stack of a code-driven video — the render backbone (Remotion or HyperFrames), screen capture in OBS, motion and 2D libraries (Anime.js, React Spring, PixiJS, p5.js, Paper.js, tsParticles), shader transitions (GL Transitions), 3D (Three.js) and physics (Matter.js, Rapier), local voiceover (Chatterbox), procedural sound (Tone.js) and word timestamps for captions (faster-whisper); how to make each of them seekable by frame, bake simulations, and check the finished file with ffmpeg. Use when planning a video made with code, choosing a library for an effect, adding a third-party animation, particle, physics, shader, TTS or captioning library to a frame-by-frame render, or running the final QA pass.
---

# Tool stack of a code-driven video

Unlike the other skills of this repository, the rules here are not lessons of past videos. They come from a breakdown of a short about a programmable video stack and were checked against the official documentation and package registries in October 2026; the label is [Toolkit]. Where they meet a lesson of a past video, the lesson is cited next to them with its own label, and where they disagree, both are given.

## Short rules

1. Pick **one** render backbone — Remotion or HyperFrames — before anything else, and do not chain two renderers. [Toolkit] See `backbone.md`.
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

## Details

- `backbone.md` — Remotion or HyperFrames or OBS; setup; what each backbone already seeks; project layout; the order of work.
- `effects-map.md` — effect → library, and what each library does not do.
- `seekable-libraries.md` — recipes that make Anime.js, springs, PixiJS, p5.js, Paper.js, particles, Three.js, GL Transitions, Matter.js and Rapier frame-exact.
- `speech-and-sound.md` — Chatterbox, Tone.js, faster-whisper: setup, the frame of a frame-by-frame video, checks.
- `qa.md` — the automatic checks of the finished file and what they do not see.

Scripts (`scripts/`):

- `qa.sh <video> [out-dir]` — ffprobe summary, black and frozen segments, EBU R128 loudness and true peak, a contact sheet, first and last frame.
- `compare-renders.sh <a> <b>` — compares two renders frame by frame by checksums of decoded frames and lists the frames that differ.
- `words.py <audio> [--lang ru]` — word timestamps with faster-whisper into `words.json` and `.srt` (runs through `uv run`).
- `bake-matter.mjs` — an example of baking a Matter.js scene into a per-frame JSON table.

Related skills: frame-by-frame render pitfalls — `video-render` (`seek-render.md`); mixing and voiceover — `video-audio`; shooting an interface — `video-ui-capture`; 3D characters — `video-3d-animation`; transitions and pace — `video-design`.

## Where the sources disagree

- **Transitions.** [Video] [Visual] [Popsci]: one transition for the whole video, a dissolve by default, no scaling at the joins. [Toolkit]: GPU shader transitions (wipes, warps, glitches) are available. In promos and explainers keep the dissolve; a shader transition is for a video whose whole style is built on it (a social short, a trailer), and then it is one shader for all joins, without zoom, and the next shot still starts from the final state of the previous one.
- **Screen recording.** [Video] [3D]: a real-time screen recording tears frames, shoot frame by frame in virtual time. [Toolkit]: OBS for real software. Both hold: a browser interface — frame by frame; OBS — only for what cannot be put on virtual time, at a constant frame rate, and its footage is then inserted into the frame-by-frame render as a video file.
- **Springs.** [Toolkit] lists React Spring for elastic motion; its runtime animation runs on the wall clock and does not survive seeking [Visual]. Use the spring of the backbone (`spring()` in Remotion) or a closed-form spring computed from `t` (`seekable-libraries.md`).

## Sources

- [Toolkit] — a breakdown of a 62-second short about a programmable video stack (watermark `@mmmorozov`), checked against the official documentation and npm/PyPI in October 2026. It is a map of possibilities: it does not prove that the short itself was made with all of these tools.
- [Audio] — archive lessons on sound and voiceover of promo videos and presentations.
- [Video] — archive lessons on video: interface recordings, pace, transitions.
- [Visual] — archive lessons on the visuals of promo videos made of schematic frames (HTML frames → frame-by-frame render).
- [3D] — lessons of a three-dimensional first-person video in the browser (three.js → frame-by-frame render).
- [Popsci] — lessons of a video in the style of Soviet popular science and early-70s filmstrips.
