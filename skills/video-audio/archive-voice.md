# The "archive" voice and ether interference [Научпоп]

Everything in this file is from a video in the style of Soviet popular-science film of the early 70s, where the voice sounds "from the archive".

## Voice processing chain

- Build the chain in this order: wow and flutter (drift 0.55 Hz at ±1.2 ms, jitter 6.5 Hz at ±0.06 ms) → band-pass filter → equalizer → heavy compression → light saturation → a tiny room → the interference layer. Taken separately, each link is almost imperceptible, and the "ether" is heard only from all of them together.
- Choose the frequency cuts by the spectrum of a reference recording in third-octave bands, not by ear. What worked: from below 170 Hz with a 6th-order slope, from above 5.6 kHz of the 8th order, a shelf of −4 dB above 3.2 kHz, presence +6 dB at 2.2 kHz. The initial "by ear" 300 Hz / 6 kHz matched the reference noticeably worse.
- Make the compression hard (threshold −40 dB, ratio 12:1): even loudness without live swings is the main sign of the broadcasting of that time.
- The saturation is soft (hyperbolic tangent with gain 2.2), the room is very small (response 120 ms, level −24 dB). With larger values the voice sounds "in a hall", not "on the air".

## The interference layer

- Build the interference from three layers: film hiss −54 dBFS in the band 1.5–8 kHz; radio noise −56 dBFS in the band 250–3500 Hz with a slow fluctuation of ±35 % at 0.23 Hz; a rare crackle of about 0.35 clicks per second at −30…−22 dB. White noise alone sounds like a malfunction, not like ether.
- Run the interference continuously for the whole length of the video — under phrases, in pauses, under the music and before the first word. The variant with noise only inside phrases was rejected: in the pauses the ether "switched off", and the sound was heard as glued together from pieces.
- Generate the interference layer once for the whole video and add it with one constant gain: when each phrase is processed and normalized separately, the noise level jumps from phrase to phrase.
- Check continuity by measurement: the interference in pauses and under phrases must match to within 1 dB (the working result — −49.6 and −49.6 dBFS). A check by ear is easily fooled by the music.
- Under the voice duck only the music and do not touch the interference, otherwise the noise sags exactly under the phrases, and the join is audible again.

This disagrees with the general advice [Звук] "between events — silence, not a bed"; that advice is about the background layers of the music and sound design of a promo, this one is about the ether layer of the archive voice.

## Loudness and the finale

- Bring the voice together with the interference to −16 LUFS with a single gain, and measure loudness only on the sections with phrases: pauses with noise lower the measurement.
- Keep the music at −20 LUFS and duck it under phrases by 15 dB (down over 0.25 s, starting 0.35 s before the phrase, back up over 0.45 s after it).
- In the finale fade the music out together with the darkening of the picture, and leave the interference until the last 0.25 s.
- If the voice is already mixed on its own time grid, re-seat the picture onto this grid, and do not cut the sound: any re-cutting of the finished ether layer breaks the continuity of the interference.
