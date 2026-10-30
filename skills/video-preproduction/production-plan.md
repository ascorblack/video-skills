# Stages 5–6 — the test shot, the plan, long runs and the retrospective [Practice]

## Stage 5 — the test shot

Render the opening 3–8 seconds (the first seconds of a launch film decide whether anyone watches the rest) or the hardest shot, at the final resolution and fps, with the real assets, the chosen style and the sound. Run the critic on it (`video-toolkit`, `qa.md`) before showing it. The person's "this is the film" is the gate to production; what they change goes into `style.md` and `beats.md`, not only into the code.

Plan this shot and the first seconds with the most careful reasoning the agent can afford; small edits later need less [Practice].

## Stage 6 — `plan.md`

```markdown
# Production plan
Backbone: <Remotion | HyperFrames | own renderAt harness> — named explicitly (video-toolkit, backbone.md)
Render: 1080x1920 @ 60 fps, <codec/bitrate>, <machine/GPU>
Per beat: library / technique (video-toolkit, effects-map.md), baked or seeked
Blockers: <missing assets, unconfirmed grid, unapproved voice> — production of those beats waits
Gates: test shot approved ✔ · all beats rendered → critic pass · full render → qa.sh · delivery
Review budget: one sheet per beat, strips for every hit and junction, native crops of all text (qa.md)
Delivery: MP4, editable project, beat sheet, asset list with licences, QA notes
```

## House rules for the project

Write the rules the next run must read into the project's agent file (`CLAUDE.md` / `AGENTS.md` at the project root): the backbone and render command, the format, the style bible path, "real assets only", "every frame is a pure function of t", where sheets go, what counts as done. Decisions that live only in the chat are lost; the next film should start from files [Practice].

## Long autonomous runs

The best agent-made films ran for hours between gates, on a long brief, while the person slept [Practice]. That works only with gates and blockers written down beforehand:

- **A missing asset is a blocker,** not a reason to draw a fake: skip that beat, finish the others, report.
- **An unclear reference gets one test frame or a question,** not 900 polished frames in the wrong direction.
- **Gates the run must not pass alone:** the style (stage 2), the story structure (stage 3), the test shot (stage 5). Inside production the run may iterate freely: render, critic, fix.
- Long renders are detached from the session and resumable (frames written to a temporary name and renamed) [3D] [Practice].
- The run ends with a report: what was done, sheets, findings fixed and left, blockers, slowest frame times.

## Parallel workers

For a long film the lead agent writes a guide and briefs one worker per chapter, all in one go [Practice]. The guide (`ANIMATION_GUIDE.md` or similar) holds:

- the direction in one line, in the person's words;
- how a chapter file works and the purity rule: "frames render in parallel and out of order; every shot is a pure function of `t`; no `Math.random()`";
- the canvas, safe areas and text bands; the API of shared helpers, characters and props;
- ownership: each worker edits only its own chapter file; a missing shared helper is written privately; a bug in a shared file is reported, not fixed; shared files change only through the lead, who then tells everyone;
- junctions: open from the previous chapter's exit state, end on the stated exit state;
- the performance budget per frame and the exact commands for sheets;
- the report format: one sentence per shot, sheet paths, slowest frame, junction states, problems with shared files.

The lead assembles only after all chapters are delivered and re-checks every junction (`video-toolkit`, `music-video.md`); an interrupted worker is resumed with its context, not re-briefed from zero.

## Generate-then-trace (reported, unverified)

One widely shared music video was made by generating base shots with a video model (characters, physics) and having the agent redraw the whole film in code on top of them, so the viewer sees only the code-drawn layer [Practice]. No source code of this step was published. If it is tried: extract frames of the generated shot, measure positions and timings into keyframe tables, write seekable code that follows them, and compare overlay sheets of generated and traced frames. Record the video model and its licence in the asset list.

## Retrospective — the tenth film is better than the first

After delivery, spend one round on lessons:

- what the person changed after seeing the film, and why;
- which findings of the critic recurred;
- what took the most time.

Write them into the project's house rules — and, where a lesson is general, propose it as an addition to these skills with its source in square brackets, the way the existing lessons are recorded. The brief, the renderer and the review checklist carry over; that is why the tenth film comes out better than the first [Practice].
