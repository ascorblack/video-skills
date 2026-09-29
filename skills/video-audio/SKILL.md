---
name: video-audio
description: Rules of sound for videos — background music and sound design, matching sound to the picture, mixing voice and music (LUFS, true peak, ducking), extending music without seams, synthesis of narrator voiceover (verbatim reading, pace), an archive "ether" voice with interference, delivering the sound and working with API keys. Use when making, mixing, checking or editing the music, sound effects, voiceover or mix of a video.
---

# Audio processing and voiceover

Every rule is taken from the lessons of past videos; the source is in square brackets (legend at the bottom).
Where the sources disagree, both pieces of advice are given, with a note on which case each applies to.

## Short rules

1. Start the first version of the background calm and light, add on request; do not substitute the accepted style during revisions. [Audio]
2. Place sound events on the moment that is visible, and take the time from the animation itself, not from the storyboard. [Audio]
3. Music under the voice: 16–20 dB quieter than the speech [Audio], 18–20 dB [3D], about 19 dB [Popsci]. Measure the loudness of speech only on the sections with phrases. [Audio] [Popsci]
4. Normalize by loudness (LUFS), not by peak. [Audio] Bring the finished mix to −16 LUFS with a single static gain with a limiter, not by normalizing per track. [3D] [Popsci]
5. Measure the true peak on the already encoded file: lossy encoding raises peaks. [Audio]
6. Give the text for synthesis in an explicit frame "read verbatim, do not answer"; check verbatim reading twice. [Audio]
7. Background between events: silence, not a bed [Audio] — but the ether interference of the archive voice runs continuously for the whole video [Popsci]. See "Where the sources disagree" in `sound-design.md`.
8. Do not stretch or squeeze a phrase to fit the picture — move the picture [Video]; if the model speaks slowly, speed up the whole finished track by stretching without changing pitch [Audio]. See `voiceover.md`.
9. Place a phrase by the start of speech in the take, not by the start of the file. [Popsci]
10. Do not print the API key or write it anywhere; count the spending by the accounting. [Audio]
11. Do not delete or replace earlier versions: every new version is a new file. [Audio]

## Details

- `sound-design.md` — the character of the background, what to avoid in background layers, pauses and matching the picture, extending music.
- `mixing.md` — mixing voice and music, loudness, peaks, encoding.
- `voiceover.md` — voiceover synthesis: verbatim reading, pace, placing phrases.
- `archive-voice.md` — the "archive" voice and the layer of ether interference for stylization in the manner of popular science.
- `delivery.md` — how to deliver the sound, keys and spending.

## Sources

- [Audio] — archive lessons on sound and voiceover of promo videos and presentations.
- [Video] — archive lessons on video: interface recordings, pace, transitions.
- [Visual] — archive lessons on the visuals of promo videos made of schematic frames.
- [3D] — lessons of a three-dimensional first-person video in the browser (three.js → frame-by-frame render).
- [Popsci] — lessons of a video in the style of Soviet popular science and early-70s filmstrips.
