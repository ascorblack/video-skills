---
name: video-preproduction
description: The optional pre-production mode for a new video — offering the person to work out the video before production (never forcing it), then guiding them through intent and brief, references and style frames, the story as a beat sheet of states, the sound plan, a test shot and the production plan, with every decision kept in files (production/<video>/brief.md, beats.md, sound.md, plan.md; production/brand/style.md, assets.md) so later sessions and parallel workers build the same film. Use at the start of any new video, film, promo, explainer, short, music video or series format; when the person asks to plan, work out, brainstorm or storyboard a video, its script, style or concept ("pre-production", "проработка", "storyboard", "brief"); and when resuming a production folder.
---

# Pre-production mode

A short request gets filled in with the safest defaults, and unrelated videos made that way start to look alike. The best agent-made videos were built from a real production document, references and a beat sheet, not from one line [Practice]. This mode helps the person write that document with the agent — **if they want to**. It is offered, never imposed.

## 1. Offer it once

**When:** at the start of a new video (or a new series format, or a new style for an existing channel) — a video that has no folder `production/<video>/` yet. An existing folder with `preproduction:` in its `brief.md` means resuming that video: read it and continue from its `stage`, do not offer again.

**Not when:** editing, fixing, re-rendering, remixing or re-voicing an existing video; a step inside a production that is already planned; the person has already said "just do it" / "без вопросов"; the person declined the mode earlier for this video, or the house rules say never to ask. In a run with nobody to answer (scheduled, overnight, a worker agent) do not ask: for a **new** video with no saved choice act as "No" below; when **resuming** a video saved as Full or Express, keep that mode, do all the work up to the first gate the person has not approved, and stop there with a report — never pass an unapproved gate alone.

**How:** one question, before any production code, in the person's language, with the host's question tool when there is one (otherwise a numbered list). Recommend one option and say why in a few words: a one-line request for a new film → Express or Full; a detailed brief already given → Express, asking only what is missing.

> Before I start — do you want to work the video out first?
> 1. **Full** — about 5 short rounds: brief → references and 2–3 style frames → beat sheet → sound → a 5-second test shot. Nothing is rendered in full until you approve the test shot.
> 2. **Express** — one round of 6 questions, then a one-page brief to confirm.
> 3. **No** — I choose sensible defaults, write them at the top of the brief and start; you can change any of it later.

Create `production/<video>/brief.md` and write the answer into its front matter at once (`preproduction: full | express | skipped`), so no other session asks again. Declining is a full answer, not a failure: never repeat the offer for the same video; when the person starts another video, one sentence is enough ("same as last time — skip pre-production?"), and a standing "never ask" goes into the house rules. The person can enter the mode at any time by asking ("let's work it out", "давай проработаем").

## 2. The three depths

| | Full | Express | No |
|---|---|---|---|
| Rounds of questions | 5–7, ≤ 4 questions each | 1 round of 6 | none |
| Produced before production | brief, references, style bible with 2–3 style frames, beat sheet with a storyboard sheet, sound plan with a measured grid, approved test shot, production plan | brief (one page) with assumptions, beat sheet draft | brief with an "Assumptions" block, beat sheet draft |
| Gates the person passes | after every stage | after the brief | none — the first render is the first review |
| Right for | a launch film, a series format, a music video, anything that will be reused | a single promo or short with a clear goal | a test of the rig, a sketch, a small piece |

Express asks the six decisions that are most expensive to change later (details in `brief.md`): goal and audience · format (platform, aspect, length range, language, voice) · look (a reference or a named style, and what to avoid) · real assets · sound · ending and must-haves.

## 3. The stages of Full

Each stage: the agent researches first, proposes, shows, then asks; the stage ends with a file and a gate where the person says "ok", changes something, or "skip".

| Stage | The agent does | The person decides | File |
|---|---|---|---|
| 1. Intent | reads everything already known: the request, the product site, the channel's past videos, the project folder | goal, audience, format, length range, must-haves and must-nots | `brief.md`, `assets.md` |
| 2. References and style | collects references, writes "what the default version would look like", renders 2–3 contrasting style frames at the final aspect | the direction (or a mix), the anti-default list | `references/`, `style.md` |
| 3. Story | logline, a beat sheet of states with the reason for every beat, counted reads, a storyboard sheet of key states | the structure, the ending, cuts | `beats.md` |
| 4. Sound | measures the track (`video-toolkit/scripts/beats.py`), proposes voice and sound events on the same clock, renders a 10–15 s sketch | music, voice, the shape of the sound | `sound.md` |
| 5. Test shot | renders the opening 3–8 s (or the hardest shot) at final resolution and passes it through the critic | "this is the film" — or what to change | `out/test/`, findings in `plan.md` |
| 6. Plan | backbone, libraries per beat, gates and blockers, review budget, delivery list; house rules for the project | approval to start production | `plan.md`, house rules |

Details: `brief.md` (stage 1 and the question bank by format), `style-and-references.md` (stage 2), `story-and-beats.md` (stages 3–4), `production-plan.md` (stages 5–6, long autonomous runs, parallel workers, the retrospective).

## 4. How to ask

1. **Research before asking.** Never ask what can be found: brand colours, logo, screenshots and copy from the product site, the channel's format from its past videos, an existing `production/` folder. Present what was found for confirmation instead.
2. **Small rounds.** At most four questions per round (Express's single round of six is the one exception, because it replaces all the others); each with 2–4 concrete options, the recommended one marked, and room for a free answer. Accept short answers ("1b, 2a, the rest is yours").
3. **Show, do not describe.** A style is chosen from rendered style frames, pacing from a timing clip, sound from a sketch — adjectives ("dynamic", "premium") are translated into frames before anyone agrees to them.
4. **Ask only what is expensive to change.** Format, length, look, story structure, music and real assets — yes. A colour tweak or a caption wording — decide, write it down, move on.
5. **One line of consequence per option.** The person may not know video craft: "9:16 at 60 s → about 12 beats, text no smaller than 48 px".
6. **The person decides what; the skills decide how.** When a wish conflicts with a lesson (a rigid length before the text is counted [Visual], a drawn fake of the real product [Video]), say so once with the reason and an alternative — then do what the person chose and note it in `decisions.md`.
7. **Every answer goes into the files at once.** `decisions.md` keeps a dated line per decision. Nothing lives only in the chat.
8. **"Skip" is always available.** At any point the person may say "skip" / "дальше" / "the rest is yours": the remaining stages are filled with defaults, listed as assumptions in the brief, and production starts.
9. **Say what remains.** After each gate: what was decided, what comes next, how many rounds are left.
10. **Pause and resume.** The front matter of `production/<video>/brief.md` holds the stage; any later session continues from the files, not from memory.

## 5. The production folder

```text
production/
  brand/            shared by every video of this brand or channel
    style.md        the style bible (stage 2), reused and extended
    assets.md       logos, fonts, screenshots, music — with source and licence
    references/     frames, clips, past works, one line each: what to take from it
  <video>/          one folder per video, e.g. 2026-10-launch-film
    brief.md        front matter: preproduction, stage, updated; the brief; Assumptions; Open questions
    assets.md       assets specific to this video; what is missing = blockers
    style.md        only the deviations from brand/style.md (or the whole bible for a one-off)
    beats.md        the beat sheet and the storyboard sheet path
    sound.md        music, measured grid, voice, sound events
    plan.md         backbone, libraries, gates, review budget, delivery
    decisions.md    dated log of decisions and who made them
```

The folders outlive the session: a second video of the same brand starts from `brand/`, and the house rules grow with every film (`production-plan.md`, Retrospective).

## Sources

- [Practice] — working practices of published agent-made videos: the breakdown of a week of viral Opus 5.5 clips (post by @seeconvm, October 2026: frame function, rig, brief, reference, state lists, springs and sound, critic, skill) and the repositories PDoomVideo, ClaudeAnimationBase, paint-mv-skills and teardown, read in October 2026.
- [Visual], [Video], [Audio], [3D], [Popsci] — the lessons of past videos used in the other skills of this repository; cited where pre-production meets them.
