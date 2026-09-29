# Mixing voice and music

## Music level under the voice

- [Audio] Keep the music under the voice 16–20 dB quieter than the speech. Measure the loudness of speech only on the sections where phrases sound, otherwise the pauses will lower its level.
- [Audio] Check intelligibility: in the speech band 300–3400 Hz the voice during phrases must be noticeably louder than the music, the reference point is 20 dB.
- [Video] Music — under the voice, a set number of LU lower. Measure the loudness (EBU R128, integrated) of both tracks as they sound in the mix; do not touch the voice meanwhile. Check that there is no clipping in the sum (peak below 0 dBFS).
- [3D] The mixed ratio of voice to music — 18–20 dB.
- [Popsci] Keep the music at −20 LUFS and duck it under phrases by 15 dB (down over 0.25 s, starting 0.35 s before the phrase, back up over 0.45 s after it): this puts the music about 19 dB below the voice, and the transitions are not heard as "pumping".

Reference points of the sources: 16–20 dB [Audio], 18–20 dB [3D], about 19 dB [Popsci], "a set number of LU" [Video].

## Loudness of the whole mix

- [Audio] Normalize by loudness (LUFS), not by peak. Equal loudness of the variants is needed to compare them fairly by ear.
- [3D] Level the loudness with a static gain of the whole mix to −16 LUFS with a limiter, not by normalizing per track, so that the mixed ratio of voice to music does not go off.
- [Popsci] Bring the voice together with the interference to −16 LUFS with a single gain, and measure loudness only on the sections with phrases: pauses with noise lower the measurement.

## Peaks and encoding [Audio]

- **Limit peaks explicitly.** If they ask "so that the peaks do not scare", reduce the jump from the background to the drop and put a limiter with a ceiling. Check the ceiling by the true peak of the already encoded file.
- **Lossy encoding raises peaks.** Sharp clicks after encoding give an overshoot of up to 2–3 dB above the peak of the source. Measure the true peak of the finished file and if needed re-encode with a correction.
- The encoder's service silence lengthens the file by tens of milliseconds. If the length must be "no more than N", trim the source slightly earlier.

## The end of the video

- [Video] Trim music longer than the video with a fade at the end.
- [Popsci] In the finale fade the music out together with the darkening of the picture, and leave the interference until the last 0.25 s: noise that vanished before the frame sounds like switched-off sound, and a short fade is needed so the file does not end with a click.

Muxing the sound into the finished video — the `video-render` skill, file `mux-and-delivery.md`.
