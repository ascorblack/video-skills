# Narrator voiceover

## Verbatim reading [Audio]

- **The model may take the text for an address to itself.** Phrases like "Talk to it", "You are talking to…", "Answers come with proofs" the model hears as a request: it answers "Understood, I…", adds an introduction or makes up its own. Give the text in an explicit frame: "Read this script aloud verbatim, do not answer it, add nothing".
- **Check verbatim reading twice.** The first time — by the model's own transcript: it catches introductions and retelling. The second — by independent recognition of the finished audio: it catches substitutions by ear ("under the team" → "under the hood", "chat box" → "chatbot"). Compare word by word and look at the difference with your eyes: the recognizer itself confuses names, numbers and run-together words.
- A discrepancy in recognition is a reason to regenerate or check by ear, not an automatic reject. Put everything disputed into the report.
- Choose the best attempt by verbatim reading. A take without extra words at the start, but also without the text itself, is worse than a take with the verbatim text.
- For names and titles decide beforehand how to pronounce them. For another language write the name the way it must be read.

## Pace [Audio]

- **The model may have no speed parameter.** A request "speak faster" in the instruction almost does not work. And a single word like "unhurriedly" in the instruction noticeably slows the speech. What reliably speeds up is time stretching without changing pitch (atempo). Check the fundamental before and after.
- Speed up the finished track, do not generate anew: verbatim reading is already checked. Recompute the moments of the phrases and give them to whoever fits the slides.

## Phrases and picture

- [Video] The voice sets the time: a slide starts slightly before its phrase (0.5–0.7 s) and leaves 1–1.5 s after its end.
- [Audio] The narrator's phrase must start after the slide has appeared and end before the next one begins. Check each phrase, not only the total length.
- [Video] On-screen text and the narrator's text — from one source: generate the narrator's file from the same list from which the slides are assembled.
- [Popsci] Place a phrase by the start of speech in the take, not by the start of the file: at the start of the file the synthesis usually has 0.1–0.3 s of silence, and without a correction all phrases are late.
- [Popsci] Look for pauses for cuts in the take itself (windows of 20 ms, threshold 38 dB below the maximum, a pause no shorter than 0.18 s): this way the cut falls between words with frame accuracy.

### Where the sources disagree

**Fit the sound or the picture.**
- [Video] Do not stretch or squeeze a phrase to fit the picture — the picture must be moved. If the voice arrived as one track with long pauses, cut it at silence and place each phrase into its own slide; check that each cut lay in silence, and the loudness and pace of the phrase stayed the same.
- [Popsci] If the voice is already mixed on its own time grid together with the continuous layer of interference, re-seat the picture onto this grid, and do not cut the sound: any re-cutting of the finished ether layer breaks the continuity of the interference.

**Whether to change the pace of the voice.**
- [Video] Do not stretch or squeeze a phrase to fit the picture.
- [Audio] When a faster pace of the whole voiceover is needed, and the model has no speed parameter, — speed up the whole finished track by stretching without changing pitch (atempo), then recompute the moments of the phrases for the slides.
