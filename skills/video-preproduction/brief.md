# Stage 1 — intent and the brief [Practice]

The prompt is about a tenth of the result; the rest is the brief, the references, the rig and the review. A short "make an insane product video" gets every gap filled with the safest default; and when hundreds of people send the same one-liner, their videos start to rhyme ("brief contagion"). The brief is where the person's video stops being the average video.

## What the agent gathers before asking

- The request itself, word for word, into `brief.md` → "Original request".
- The product or subject: its site (copy, screenshots, colours, logo, fonts in use), docs, store page. Real screenshots and logos go into `assets.md` with their source.
- The channel or brand: past videos (format, length, fps, typical hooks, captions style), an existing `production/brand/` folder or house rules.
- Constraints already fixed by the project (for example, a channel that is always 1080×1920 at 60 fps).

Present it as "here is what I found — correct me" rather than as questions.

## `brief.md` template

```markdown
---
preproduction: full        # full | express | skipped
stage: intent              # intent | style | story | sound | test-shot | plan | done
updated: 2026-10-30
---
# <working title>

## Original request
<verbatim>

## Goal
After watching, the viewer <does / feels / knows> …  Success looks like …

## Audience
Who, what they already know, where they will see it (feed, landing page, conference screen).

## Format
Platform · aspect and resolution · fps · length range (final length is counted from the beats, not fixed in advance) · language(s) · captions · voice yes/no · safe areas of the platform UI.

## Must have / must not
Real product screens only; logo at the end; no faces; no competitor names; …

## Ending
Call to action / loop back to the first frame / punchline / logo hold.

## Assumptions
What the agent decided without asking, each on one line — the person may overrule any of them.

## Open questions
What is still unknown and what it blocks.
```

## Express: the six questions

Ask them in one round, each with options and a recommended default derived from what was found:

1. **Goal and audience** — what should the viewer do, feel or know afterwards, and who is it?
2. **Format** — platform, aspect, length range, language, voice or no voice.
3. **Look** — a reference (a frame, a clip, a link, own past work) or a named style; and one thing to avoid.
4. **Real assets** — what exists (product URL, screenshots, logo, footage, brand book); the agent fetches the rest itself.
5. **Sound** — own track, licensed, generated or synthesized music, or none; voiceover or not.
6. **Ending and must-haves** — CTA, loop or punchline; anything that must or must not appear.

Then write the one-page brief with the assumptions block and a draft beat sheet, and ask for one confirmation.

## The question bank by format

Defaults a recommendation can start from; replace them with what the project already fixes.

| Format | Questions that matter most | Sensible defaults |
|---|---|---|
| Launch film / product promo | the one feature that sells; real screens available; offer at the end | 30–45 s; 16:9 for the site plus a 9:16 cut from the same timeline; real UI recordings; music with hits on state changes; logo + URL hold ≥ 2 s |
| UI demo / walkthrough | which flow, start and end state, demo data | frame-by-frame capture of a demo stand [Video]; voice optional; callouts on marks [Video] |
| Explainer / popular science | the one idea; the example with a participant, an action and a number [Visual] | length counted from the text [Visual]; one transition (dissolve) [Video]; narrator |
| Social short (vertical) | the hook of the first 1–2 s; the loop or punchline | 1080×1920; 15–45 s; big type, few elements; captions burned in; ending rhymes with the opening |
| Horror / atmospheric short | what the fear is about; how explicit; the payoff | dark palette with grain and dither against banding; slow reveals; sound carries half the fear; no jump-scare every few seconds |
| Music video | the song (with stems if any), lyrics source, the visual idea per section | measured grid confirmed by ear; chapters on bar lines; karaoke band or not; cast sheet first (`video-toolkit`, `music-video.md`) |
| Data story | the source of the numbers and who verified them [Visual] | one chart idea per beat; numbers worded as what was actually measured [Visual] |

## Rules of this stage

- **Real assets only.** The agent may invent a camera move, never the person's dashboard. A missing screen, logo or figure is a **blocker** in `assets.md` — it stops that beat until the person supplies it; it is not drawn as a fake [Video] [Practice].
- **Keys by name.** API keys for voices, music or video models live in `.env`; the brief names the variable, never the value [Audio].
- **Length is a range until the beats are counted** [Visual].
- **One brand, one shared folder.** A second video of the same brand gets its own `production/<video>/` but reuses `production/brand/` — style, assets, references — and the house rules, instead of starting from zero [Practice].
