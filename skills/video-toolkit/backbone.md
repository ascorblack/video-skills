# The render backbone [Toolkit]

The backbone owns the timeline, the frame clock, the capture and the encoding. Everything else (motion libraries, canvases, 3D, physics, sound) plugs into it. Two backbones were named in the source; they are alternatives, not layers of one stack.

## Which one

| | Remotion | HyperFrames |
|---|---|---|
| What a scene is | React components; the time is `useCurrentFrame()` | HTML/CSS/JS compositions; the time is a paused GSAP timeline (and other registered animations) seeked by the runtime |
| Choose when | the project is React/TypeScript, many parameterized variants, data-driven videos, a team that already writes React | an agent writes the video; a catalog of ready blocks (titles, captions, charts, transitions, 3D) helps; plain HTML is easier to read and edit than a React tree |
| Seeks by itself | everything driven by `useCurrentFrame()`; integrations `@remotion/three`, `@remotion/gsap`, `@remotion/lottie`, `@remotion/gif`, `@remotion/rive`, `@remotion/skia`; CSS animations via `animation-play-state` + negative `animation-delay` | GSAP, CSS animations, Anime.js v4 (instances pushed to `window.__hfAnime`), Lottie, Three.js and TypeGPU (through the `hf-seek` event), Web Animations |
| Does not seek | `react-spring`, Framer Motion, anything on `requestAnimationFrame` | a library with its own ticker that is not registered; unregistered Anime.js instances are never seeked |
| Transitions | `@remotion/transitions` (`TransitionSeries`) | `@hyperframes/shader-transitions` (14 WebGL shaders on a GSAP timeline) and registry blocks |
| Reproducible render | the same frame function; pin Chrome and fonts yourself | `npx hyperframes render --docker` pins Chromium, fonts and FFmpeg |
| License | free for individuals, for-profit companies of up to 3 employees and non-profits; a company license above that | Apache 2.0 |

In both, "what does frame N look like" must depend only on N. That is the same rule the lessons arrived at the hard way [Visual] [3D] — see the `video-render` skill, `seek-render.md`.

## Setup

Check the current prerequisites before installing: the commands change between versions.

**Remotion.**

```bash
npx create-video@latest
npx remotion studio                          # preview
npx remotion compositions                    # list composition ids
npx remotion render <CompositionId> out/video.mp4
```

The pattern is `Composition` → `Sequence` → components that read `useCurrentFrame()` and compute styles through `interpolate()` and `spring()`. Read https://www.remotion.dev/docs/third-party before pulling any other animation library in.

**HyperFrames** (Node.js 22+ and FFmpeg).

```bash
npx hyperframes skills update                # agents: installs exactly the core skill set from main
npx hyperframes init my-video
cd my-video
npx hyperframes preview
npx hyperframes render                       # add --docker for a byte-reproducible render
```

The interactive `npx skills add heygen-com/hyperframes` picker opens with nothing selected and lags `main`; a non-interactive run without `--skill` installs all seven skills. For an agent, `npx hyperframes skills update` is the documented path. The core skills, to read before writing HyperFrames code:

- `/hyperframes` — the render contract and the work loop; read first.
- `/hyperframes-cli` — scaffold, lint, look at frames, preview, render, recover from failures.
- `/hyperframes-registry` — about 450 editable blocks: transitions, titles, kinetic type, captions, charts, maps, 3D, camera moves. Look here before building a named visual by hand.
- `/media-use` — music, sound effects, images, voiceover, transcripts, cutouts, colour looks.

Do not assume HyperFrames is a Remotion wrapper: it has its own composition format, runtime and CLI. `/remotion-to-hyperframes` exists for a port.

**Your own harness** [Practice] — one HTML page that exposes `window.renderAt(t)`, a Puppeteer/Playwright loop that calls it for every frame, and FFmpeg. Left without instructions, an agent tends to build exactly this and to ignore an installed Remotion or HyperFrames, so name the backbone in the brief. The own harness is the right choice when the whole film is one canvas (a p5.js/p5.brush cartoon, a single Three.js scene, a generative piece) and a framework would only add layers. Then it must give what a framework gives:

- `renderAt(t)` is a pure function of `t`, returns only when the frame is drawn (await async draws), and the page reports ready only after fonts and assets have loaded;
- page console errors and `pageerror` are forwarded to the render log; ms per frame is printed;
- frames are written to a temporary name and renamed, so an interrupted render resumes; encoding refuses a missing frame;
- the review modes of `music-video.md` (sheet, strip, clip with audio, loop) exist from the first day;
- the Chrome GPU flags and the WebGL renderer string are printed at start: a silent fall back to software rendering (SwiftShader) is many times slower (a heavy p5.brush frame took 14–16 s on SwiftShader) and not bit-identical to the GPU.

**OBS Studio** is not a backbone but a recorder. Its footage enters the backbone as a video file. When to use it and how — in `effects-map.md` and the `video-ui-capture` skill.

## Project layout

Adapt to the backbone; do not force Remotion paths onto HyperFrames.

```text
video-project/
  README.md            # what it is, render command, asset list with licenses
  package.json         # pinned versions
  src/ or compositions/
    scenes/            # one module per shot
    components/        # reusable titles, cards, diagrams, transitions
    theme/             # colors, fonts, motion tokens, output size and fps — in one place
    timeline/          # the shot table as data; baked simulations (JSON)
  assets/
    audio/ images/ video/
    fonts/             # only licensed fonts, as files, Cyrillic included [Popsci] [3D]
  scripts/
    bake-*.mjs         # simulations baked into per-frame tables
    render.sh
  out/
    v001.mp4 …         # every version a new file [Video] [Audio]
    qa/                # output of qa.sh
```

## Order of work

1. **Plan.** At the start of a new video offer the pre-production mode once (`video-preproduction` skill); whether it is taken or declined, the plan below ends up in files. Message, audience, length, platform, aspect ratio, fps, language, brand, available assets. Missing parameters — choose sensible defaults and state them. A shot table: `start`, `end`, picture, transition, narration, sound, library, assets. Frames are `round(seconds × fps)`. Mark what is real footage and what is generated. The length is not set before the text is counted [Visual].
2. **One representative shot.** 3–8 seconds at production resolution and fps, with the most demanding library of the video in it. Check typography, motion, the join, and that the library survives seeking (render twice, compare) before building the rest.
3. **All scenes.** The narration track first if the video is voice-led: its timings set the picture [Video]. Libraries only where they visibly beat the backbone.
4. **Render and inspect.** `scripts/qa.sh`, frames around every join and at every action at full size [Visual] [3D], then the whole video played through.
5. **Final gate.** Codec, size, fps, duration, an audio track of the right length, no black or transparent frames at the start and end, loudness and true peak on the encoded file [Audio]. Deliver the MP4 together with the editable project, the shot table, the asset list and the QA notes.
