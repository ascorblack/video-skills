# Stages 3–4 — the story as states, and the sound on the same clock [Practice]

## A beat sheet, not an activity list

"Zoom in, morph, particles" is a list of activity. A storyboard says what the viewer knows at every second. The most-saved prompt of the week of viral agent-made clips was a spec of states: one container morphing its size, radius and colour from state to state, a cursor driving the changes with real clicks, and the last frame equal to the first so the video loops [Practice]. One shape that transforms reads better than ten effects.

Every beat has:

- an **entry state** and an **exit state** — what is on screen when it starts and when it ends;
- what the viewer **knows** after it that they did not know before;
- a **reason to exist** — if the agent cannot say why beat 4 is there, beat 4 is cut;
- its reads, counted (below), which set its length.

## `beats.md` template

```markdown
# Beat sheet: <title>
Logline: <one sentence — who/what, the change, the payoff>
Total: <sum of beats> s (counted, not assigned)

| # | t (s) | Entry state | Exit state | Viewer now knows | Why it exists | On screen text | Narration | Sound |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.0–2.4 | black, cursor at centre | card A at rest | this is about X | hook | — | — | low hit on the reveal |
| 2 | 2.4–6.0 | card A | card A grown into the dashboard | X does Y | the main feature | "Y in one click" | … | click, whoosh on the morph |
…
Ending: <exit state of the last beat> — equals the first frame (loop) / logo hold 2 s.
Storyboard sheet: out/storyboard.jpg
```

Junctions follow the lessons: the next beat starts from the exit state of the previous one; shared elements keep their coordinates and size; the effect never comes before its cause [Visual].

## Counting the length

- **Reads set the length.** For every moment: what must the viewer understand, and how long does it take someone who sees it once, at full speed, for the first time? One read at a time; fast actions, slow meanings (`video-toolkit`, `characters.md`).
- Text on screen: max(animation + 2–3 s; 2 s + words ÷ 2.7) for frames with a picture [Visual]; words ÷ 2.4 + 2 s without voice [Video]; with voice, the voice sets the time and the slide holds 1–1.5 s after the phrase [Video].
- Titles land hard and stay long enough to be read [Practice]; the last beat's final read needs time to land before the video ends.
- If the sum does not fit the length range, cut a beat — do not squeeze the reads.

## The storyboard sheet

Render the exit state of every beat as a still (rough is fine, but at the final aspect, from the real backbone) and tile them on one sheet. The person approves the structure on that sheet — rearranging stills is cheap, re-rendering a film is not.

## Stage 4 — the sound plan (`sound.md`)

Sound runs on the same clock as the picture [Practice]:

- **Own or licensed track:** measure first, then animate — `video-toolkit/scripts/beats.py` gives the grid, downbeats and per-frame features. State changes land on beats, big moments on downbeats, clicks and whooshes on hits. Render a 10–15 s clip with a flash on the beats and have the person confirm the grid by ear.
- **Synthesized score:** written to the beat sheet (Tone.js offline, or synthesized in Node/Python) — every sound event has a time in `beats.md` [Toolkit].
- **Voice:** choose it on a test paragraph with the project's names, numbers and terms; the script comes from the same source as the on-screen text [Video]; music under the voice 16–20 dB lower [Audio].
- **The blind test:** listen to the track with eyes closed. If the sound has no shape without the picture — no build, no hits, no release — the sound design is not finished [Practice]. The agent cannot hear: give the person a clip.

```markdown
# Sound plan
Music: <source, licence, BPM/offset measured, grid confirmed by ear on <date>>
Voice: <provider/voice, test take path, approved>
Events: see the Sound column of beats.md
Mix targets: voice vs music −16…−20 dB; final −16 LUFS, true peak measured on the encoded file (video-audio)
```
