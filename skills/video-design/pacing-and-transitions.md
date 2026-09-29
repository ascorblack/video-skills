# Pace, transitions, camera

## How long to hold a slide

- [Визуал] Count the display time, do not assign it: **max(animation time + 2–3 s; 2 s + words ÷ reading speed)**. With a picture alongside, people read slowly, about 2.7 words per second. Service tags ("for example") do not count.
- [Визуал] If there are several languages, count by the slower one and keep one timing for all versions: the storyboard and sound are then shared.
- [Визуал] Do not set the length of the video before the text has been counted. A rigid "90 seconds" with full explanations gives two-second slides that nobody has time to read.
- [Визуал] The animation plays out in the first seconds of the slide, after that the frame stands calmly and lets it be read to the end.
- [Видео] The voice sets the time. A slide starts slightly before its phrase (0.5–0.7 s) and leaves 1–1.5 s after its end. Longer — the viewer waits; earlier — the phrase is cut off over someone else's picture.
- [Видео] If there is no voice, count the reading: a slide is no shorter than "words / 2.4 + 2" seconds.
- [Научпоп] After each phrase hold the frame another 2 seconds before changing, otherwise the viewer does not have time to finish reading what was just said.
- [Научпоп] Put the chapter title as a small plate in the bottom corner for 3–4 seconds: a large caption covers the very subject of the showing, and in educational film the main thing is the showing.

### Where the sources disagree

- **Hold after the end of the phrase.** [Видео]: 1–1.5 s, in a promo about a program — longer and the viewer waits. [Научпоп]: 2 s, in a popular-science video — otherwise the viewer does not have time to finish reading what was said.
- **Reading speed in the formula.** [Видео]: "words / 2.4 + 2" s — for a slide without voice. [Визуал]: "2 s + words ÷ 2.7" (and not less than animation + 2–3 s) — for schematic frames, where there is a picture alongside.

## Transitions

- [Видео] One transition for the whole video: the new slide appears over the old one in half a second. Different effects on each slide distract from the content.
- [Визуал] No scaling at the joins: only a dissolve (0.5–0.8 s). A hard cut is acceptable as a semantic device, but the viewer perceives it as a jerk; by default — a dissolve.
- [Научпоп] Connect chapters with a cross-dissolve of 0.5–1 s after the hold, not with an iris in every chapter: a repeating iris quickly becomes obtrusive.
- [Научпоп] Put cuts within a chapter into the pauses of the narrator's speech: a cut in the middle of a phrase cuts a word and is noticeable at once. How to find pauses — in the `video-audio` skill, file `voiceover.md`.

The duration of the dissolve differs between sources: half a second [Видео], 0.5–0.8 s [Визуал], 0.5–1 s between chapters [Научпоп].

## A transition without jerking [Визуал]

The viewer sees a jump when something that should have stayed in place changes between neighboring frames. Frequent causes:

1. **Different camera scale in neighboring shots.** A light "drift" or push-in at the start of each shot gives a noticeable scale jump at the join.
2. **Shared elements stand in different places.** The grid, panel, title, the "server" block in neighboring frames must have the same coordinates and size. If the composition of a chapter changes, change it inside the shot by motion, not at the join.
3. **Data is redrawn from scratch.** The next shot must start from the final state of the previous one: do not empty the grid only to fill it anew at once.
4. **Cause and effect in reverse order.** If a hit, a stamp or a command changes something, the change must happen after the hit, in the same shot. Otherwise at the dissolve the viewer sees that the effect happened before the cause.
5. **A hard cut where none was asked for.**
6. **Permanent blocks of different size.** A panel whose height depends on the length of the text "breathes" at every join. Fix the height.

### How to check joins [Визуал]

- For each join take three frames: the end of the shot, the middle of the dissolve, the start of the next. Look at the pairs side by side: everything that does not take part in the semantic change must match pixel for pixel.
- Look separately at frames in the middle of motion, not only the final ones: an object stuck halfway is visible only there.

## Camera

- [Видео] A camera push-in — onto a whole block of the interface, not onto the middle. Lay the edge of the frame on the boundary of a column or window. Text cut in half looks like a defect. A form into which something is entered must come into the frame entirely, together with the button.
- [3D] Show screen recordings whole and up to the result of the action: a zoom into buttons and a freeze frame right after a click the viewer notices and does not accept.
- [Научпоп] Do not shake the camera and do not sway the frame: shake hinders reading the screens, in educational film the camera stands on a tripod, and the shake from the first version had to be removed on request.
