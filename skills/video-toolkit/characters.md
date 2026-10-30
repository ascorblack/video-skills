# Characters and acting in code-drawn animation [Practice]

From the guide of ClaudeAnimationBase (MIT, a starter kit for hand-painted cartoons drawn by an agent with p5.js + p5.brush) and the PDoomVideo music video. For 3D first-person bodies and hands see the `video-3d-animation` skill.

## Why code-drawn motion looks mechanical

"Code moves every part at once, on the same curve, by the same amount." The fixes are the classic principles, written as code rules:

- **Avoid twinning.** Code copies values: both arms at the same angle, both eyes blinking together, a crowd bouncing in unison. Offset phases and amplitudes per part and per character (from a seeded per-element constant).
- **Strong key poses first.** Block the key poses of a shot and check them as stills; add the motion between them only once they read. If the key poses do not read, the motion will not fix it.
- **Anticipation, overshoot, settle.** A move starts with a small counter-move, ends past its target and settles (springs by class — `seekable-libraries.md`).
- **Contact, not proximity.** Props touch the hand; feet touch the ground (the same rule as `video-3d-animation`).
- **On twos.** For a hand-made look hold each drawing for two frames (12 or 24 drawings per second) and boil linework at 12 Hz — 60 fps adds cost and nothing to that style.

## Acting as data

Keep every emotion as one data entry, not as code scattered over shots:

```js
const EMO = {
  sad:     { eyes: "sad",   mouth: "frown", tint: "blue", tintK: .35, emote: "cloud", take: .3,
             body: t => ({ sq: .08, armL: -.75, armR: -.75, lookY: .5 }) },
  furious: { eyes: "angry", mouth: "teeth", tint: "red",  tintK: .5,  emote: "steam", take: 1.2,
             body: t => ({ dx: .22 * Math.sin(20 * Math.PI * t) }) },
};
```

- Each entry has a face, a colour shift, a symbol, a **reaction size** (`take`) and an idle body motion locked to the beat. Body language, not just a face: bored sighs every four beats, nervous glances alternate each beat, proud stretches.
- `feel(name, t)` returns the full pose for time `t` — a pure function.
- An **acted transition** between emotions, from a key list `[[0, "bored"], [1.2, "surprised"]]`: a squint starts 0.1 s before the key and holds 0.14 s after it, the face swaps under the squint, then a take sized by the new emotion, then an eased cross-fade of the pose with a 0.4 s overshoot. Faces act; they never snap.
- Compose poses by spreading objects: `{ ...feel("happy", t), ...turn(t), hat: "party" }` — later spreads win; where two sources move the same field, add them.

## Model sheets

- Render every character in all its views and all its emotions on one sheet (a loop mode of the harness, the one place where text labels are allowed) and have it approved before any shot is drawn.
- Workers and later sessions look at the sheet first; review samples of every chapter against it.

## Timing for the viewer

- "You know what happens because you wrote the code. The viewer doesn't: they see it once, at full speed, for the first time." For every moment, ask what the viewer must understand and how long that takes.
- **One read at a time.** Do not start a new read while the last one is still being taken in; two things at once — the viewer sees one.
- **Fast actions, slow meanings.** A motion may be very quick if it was anticipated; what it means needs held time.
- **Let the reads set the length** — including the last shot. If the reads do not fit, lengthen the shot or cut a read; do not squeeze them. (The kit's first demo packed its ending into about 1.3 s, and nobody could tell what had happened.)
- **Every shot needs an event:** something changes between its first and last frame. "A character stands in a meadow being cute" is not a shot.
- **Show, do not label.** A sign that repeats the story ("I'm lost") is the classic failure; show the character being lost.
