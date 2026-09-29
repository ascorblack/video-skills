# Music and sound design

## First agree on the character [Звук]

- The first version almost always turns out "too much": too harsh, fast or dense. For a background under a video it is more reliable to start with calm and light, and add on request.
- If they ask for "not enough sound", it does not mean "add music". Often they want more of the same sounds: hits, clicks, drops in the chosen style. Clarify what exactly to add: do not change the genre, add within it.
- Once a style is accepted, it must not be substituted during revisions. Extending, shortening, speeding up — all is done with the same instruments and at the same tempo.

## Background layers: what to avoid [Звук]

- **A continuous background irritates.** Rustles, ticks on every sixteenth, "data in the background" are perceived as "something is sneaking". Between events there must be silence, not a bed.
- **An even pulse promises a resolution.** If a heartbeat or a kick sounds unchanged, the listener waits for a drop; if there is no drop, the expectation is cheated. Make the pulse between climaxes sparser and quieter, and build up toward the climax.
- **Do not change the tempo before a drop.** A sharp speed-up (beats → eighths) is heard as a glitch. The lead-in is built on the same grid: fill in the skipped beats, smoothly raise the volume, give a short breath and only then the hit.
- **Periodic repetition of one piece of noise gives a tone.** A piece of 30 ms, repeated exactly, sounds like a hum at ~33 Hz. For "stutter" and glitch take a new piece of different length each time.
- **An error signal is not a drop.** A buzzer is good on an error in the frame, but it does not replace the climax. A drop is a noticeable hit with a short lead-in.
- **No melody means no melody.** If they asked for "only technical sounds", check the spectrum for tonal peaks: there must be no bass, pad, notes or chords.

### Where the sources disagree: continuous background

- [Звук] — background layers of the music and sound design of a promo: a continuous background irritates, between events — silence, not a bed.
- [Научпоп] — the layer of ether interference under the "archive" voice: the interference runs continuously for the whole length of the video, under phrases, in pauses, under the music and before the first word; the variant with noise only inside phrases was rejected, because in the pauses the ether "switched off" and the sound was heard as glued together from pieces. In detail — `archive-voice.md`.

## Pauses and matching the picture [Звук]

- Place sound events on the moment that is visible, not on the start of the animation. A stamp that flies for 0.2 s "hits" at the end of the flight, together with the camera shake.
- Take the time from the animation itself, down to the offset within the scene, not from the storyboard.
- If the scenes were lengthened, the events are moved by the rule "the same scene, the same offset from its start". The pauses stretch along with the scenes, and tens of seconds of silence sound like a loss of sound. Fill long pauses with a rare quiet pulse (once per bar, noticeably quieter than the main one). Leave full silence only where it is needed dramaturgically, and for 2–3 seconds.
- At a constant tempo a bar seldom divides the intervals between sections evenly. Do not change the tempo: lengthen the quiet bar before an accent by a beat (a breath before the hit) or choose a grid shift at which the error is minimal. An accent slightly later than the frame appears is better than earlier.
- The narrator's phrase must start after the slide has appeared and end before the next one begins. Check each phrase, not only the total length.

[Визуал] Before muxing in the sound, compare the timecodes of the frame's events with the drops of the track and write the sound engineer the actual times if the discrepancy is more than a second.

## Splicing and extending music [Звук]

- Do not cut finished sound. Reassemble the composition by a map "old bar → new place": each note is moved whole, tails and reverb are computed in the new time, and no joins are heard.
- It is convenient to cut and repeat in blocks of 4 bars with a full cycle of chords, so that the harmony goes naturally at the join.
- A bar where there was a rise to the climax must not be placed before an ordinary verse: the rise will go nowhere. Replace it with a bar with the same chord without a rise.
- If a former accent bar landed on a join, put the rise back before it. Otherwise the accent enters abruptly, without preparation.
- Check joins by measurement: compare the jump of the spectrum at the join with an ordinary bar change. Only the intended places should stand out.
- If the generation depends on random numbers, preserve their sequence: generate the notes in the same order, even when some of them are thrown away. Then the extended version matches the original down to the sample, and this is easy to prove.
- After any edits of the generator, check that the earlier versions reassemble byte for byte the same.

[Видео] Trim music longer than the video with a fade at the end. Better — ask for a track to the exact length and accents on chapter changes.
