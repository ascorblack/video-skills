# video-skills

A set of Claude Code skills for producing videos: promos and presentations about programs, videos built from schematic frames, three-dimensional videos in the browser, and stylizations in the manner of Soviet popular-science film.

The skills are assembled from lessons recorded in the course of past videos. Every piece of advice traces back to a phrase from one of those lessons; nothing has been added beyond them. Each piece of advice has its source in square brackets. Where the sources disagree, both pieces of advice are given, with a note on which case each applies to.

## Skills

| Skill | Topic | When it triggers |
|---|---|---|
| `video-design` | Design and visuals | diagrams and lines, terms with examples, how long to hold a slide, transitions, camera, titles, stylization in the manner of popular science and filmstrips |
| `video-audio` | Audio processing and voiceover | background and sound events, mixing voice and music, LUFS and peaks, voiceover synthesis, an "archive" voice with interference |
| `video-3d-animation` | 3D animation | first-person hands and body, contact with objects, pose blending, pushing apart, light and materials, detectors of intersections and jerks |
| `video-ui-capture` | Interface recording | frame-by-frame browser capture, demo stand, cursor, marks, cropping and push-ins, second language version |
| `video-render` | Rendering and optimization | pitfalls of frame-by-frame rendering, determinism, NVENC and bitrate, launching a render, muxing in the audio, checking the finished file |

Each `skills/<name>/` folder holds a `SKILL.md` — the description by which the skill triggers, and short rules — and next to it files with details, which `SKILL.md` refers to.

## Sources

| Label | Where from |
|---|---|
| [Audio] | archive lessons on sound and voiceover of promo videos and presentations |
| [Video] | archive lessons on video: interface recordings, pace, transitions |
| [Visual] | archive lessons on the visuals of promo videos made of schematic frames (HTML frames → frame-by-frame render) |
| [3D] | lessons of a three-dimensional first-person video in the browser (three.js → frame-by-frame render) |
| [Popsci] | lessons of a video in the style of Soviet popular-science film and early-70s filmstrips |

## Where the sources disagree

- Continuous background: "between events — silence, not a bed" [Audio] versus a continuous layer of ether interference under the archive voice [Popsci] — `video-audio/sound-design.md`, `archive-voice.md`.
- Fitting the voice: cut the voice at silence and place the phrases into slides [Video] versus "re-seat the picture onto the ready grid of the voice with interference, do not cut the sound" [Popsci]; do not stretch a phrase to fit the picture [Video] versus speeding up the whole track via atempo [Audio] — `video-audio/voiceover.md`.
- Holding a slide after the phrase: 1–1.5 s [Video] versus 2 s [Popsci]; reading speed 2.4 [Video] versus 2.7 words per second [Visual] — `video-design/pacing-and-transitions.md`.
- Interface in the frame: only a real recording [Video] versus an interface redrawn in every frame of a stylized video [Popsci]; cursor from the recording's events [3D] versus cursor from key points [Popsci] — `video-ui-capture/framing.md`.

## How to install

The repository is private; clone it under your own account:

```bash
gh repo clone ascorblack/video-skills ~/video-skills
```

**Option 1 — personal skills, in all projects.** Copy or symlink the skill folders into `~/.claude/skills/`:

```bash
mkdir -p ~/.claude/skills
for d in ~/video-skills/skills/*/; do ln -s "$d" ~/.claude/skills/; done
```

**Option 2 — in a single project only.** The same, but into the `.claude/skills/` folder inside the project.

**Option 3 — as a plugin for one session.** The repository root holds `.claude-plugin/plugin.json`, so it can be loaded as a whole:

```bash
claude --plugin-dir ~/video-skills
```

Once installed, the skills trigger on their own when a task matches their description; a skill can be invoked explicitly by name: `/video-audio` in options 1–2, `/video-skills:video-audio` in option 3.

## Structure

```
.claude-plugin/plugin.json
skills/
  video-design/        SKILL.md, lines-and-layout.md, explanations.md,
                       pacing-and-transitions.md, retro-style.md, process.md
  video-audio/         SKILL.md, sound-design.md, mixing.md, voiceover.md,
                       archive-voice.md, delivery.md
  video-3d-animation/  SKILL.md, body-and-hands.md, motion.md,
                       materials-and-light.md, frame-checks.md
  video-ui-capture/    SKILL.md, recording.md, framing.md, languages-and-sync.md
  video-render/        SKILL.md, seek-render.md, performance.md, mux-and-delivery.md
```
