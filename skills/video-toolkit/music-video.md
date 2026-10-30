# Music videos and edits on the beat [Practice]

From the pipelines of the PDoomVideo music video (an animated clip written by an agent, briefing parallel workers per chapter) and of paint-mv-skills built on it. Their repositories carry no licence file: the ideas are reused here, not the code.

## The order

1. **Measure the song** before drawing anything: `uv run scripts/beats.py song.wav --fps 60` gives a constant beat grid (BPM, offset), a downbeat guess and per-frame audio features. Read the flags: `AMBIGUOUS_TEMPO` (half or double tempo fits as well), `GRID_DRIFT` (tempo is not constant — map sections separately, never force one grid onto it), `WEAK_PULSE`. The tool cannot hear: render a 10–15 s clip with a flash on every beat and a bigger one on downbeats and have a person confirm it before the storyboard is built on the grid.
2. **Time the lyrics.** Best: a real LRC/SRT from the artist. Otherwise faster-whisper word timestamps (`scripts/words.py song_vocals.wav`) aligned to the known lyric text — a draft with about 0.3 s error on sung lines, checked with a timing clip. A hotword prompt can make whisper invent lyrics in instrumental parts; run it on an isolated vocal stem when one exists.
3. **Chapters tile the whole song** (`intro 0–12.4`, `verse1 12.4–38.5`, …), cut on bar lines; inside a chapter, shots of 1.4–4 s. Every lyric line has a shot, every shot a concrete action. Write the storyboard as a table (see `video-preproduction`, `story-and-beats.md`).
4. **Junctions are contracts:** each chapter's last frame ("out") is stated in the storyboard and the next chapter opens from it. A chapter that changes its out must tell its neighbour.
5. **A cast sheet first:** every recurring character rendered on one model sheet, approved by the person before any chapter is drawn (`characters.md`).
6. **Chapters in parallel** (one worker each, briefed by the guide — `video-preproduction`, `production-plan.md`), then a unify pass over all junctions, then the full render.

## The frame contract

```js
// a shot paints the whole frame and is a pure function of time
// t = song time, lt = t - shotStart, dur = shot length
chapter("takeoff", 38.5, 59.0, [
  [38.5, (t, lt, dur) => { /* … */ }],
  [41.5, singularity],
]);
window.renderAt = async (t) => { T = t; await redraw(); return canvas.toDataURL("image/png"); };
```

- Beat helpers are pure: `beatOf(t) = (t - offset) / period`, `pulse(t)` = 1 on each beat decaying to 0, `onDownbeat(t)`. Important action within a shot lands on beat times; big moments on downbeats; hits and whooshes on onsets.
- Cuts, punch-ins, flashes and shakes are driven by the same grid (a "director" function of `t`), so the edit cannot drift from the music.
- Text bands (karaoke, captions) own a fixed zone: keep faces and key action out of it whenever a line is showing.
- Performance budget per frame: aim at ≤ 2.5 s, never more than ~4 s; the renderer prints ms per frame, and a slow chapter goes back to its author.

## The harness modes that pay off

Whatever renders the frames (HyperFrames, Remotion, or a page with `renderAt` and Puppeteer), have these modes, all from the same frame function:

| Mode | What it gives |
|---|---|
| sheet at chosen times | the critic's evidence: several moments on one labelled image, ms per frame printed |
| strip `a:b` | every frame around a hit or a junction |
| clip `a:b` with audio | a short piece to hear timing (the only way a person can judge sync) |
| frames `a:b` with N workers | the full render: each frame written to `.tmp` and renamed, so a crash resumes where it stopped; re-render until "0 frames to render" before encoding |
| encode | frames + audio → MP4, refusing to start if a frame number is missing |
| loop name | a standalone looping scene: model sheets, cast sheets, emotion sheets |

`scripts/sheet.sh` gives the sheet and strip modes on any rendered file.

## Checks specific to music videos

- At every chapter junction: frames at boundary −0.1 s, boundary, +0.05 s, +0.3 s side by side.
- Sample frames per chapter against the cast sheet: characters on model.
- Whole-film rhythm: something happens in every shot, the camera is never dead-still without a reason, text stays light, the picture tells the lyric.
- The ending rhymes with the opening frame.
