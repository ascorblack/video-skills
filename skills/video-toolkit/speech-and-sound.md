# Voice, procedural sound and word timing [Toolkit]

Three tools from the source cover three different jobs and are easy to confuse: **Chatterbox** makes speech from text, **faster-whisper** makes text with timings from speech, **Tone.js** makes music and sound effects from code. The mixing rules (levels under the voice, LUFS, true peak) do not change with the tool — they are in the `video-audio` skill, `mixing.md`.

## Chatterbox — local TTS

- Install: `uv pip install "chatterbox-tts @ git+https://github.com/resemble-ai/chatterbox"` (Python ≥ 3.10; developed on 3.11; a CUDA GPU is strongly preferred). MIT license. The PyPI release `chatterbox-tts` 0.1.7 predates Multilingual V3: its `from_pretrained` has no `t3_model` and loads V2, so the example below fails with a `TypeError` on it. Install from the repository (pin a commit) or drop `t3_model` and accept V2.
- Models: **Multilingual V3** (0.5B, 23 languages including Russian) is the one for non-English narration; **Turbo** (350M) and **Nano** (110M, CPU-capable) are English-only and support tags such as `[laugh]`, `[cough]`.

```python
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

model = ChatterboxMultilingualTTS.from_pretrained(device="cuda", t3_model="v3")
wav = model.generate("Текст одной фразы.", language_id="ru",
                     audio_prompt_path="voice_ref_10s.wav",   # optional voice reference
                     exaggeration=0.5, cfg_weight=0.5)
ta.save("phrase_01.wav", wav, model.sr)
```

- Generate **one phrase per file**, from the same list the on-screen text is built from [Video]: a phrase that failed is regenerated alone, and every phrase gets its own start in the timeline.
- Defaults `exaggeration=0.5, cfg_weight=0.5` suit most text. A fast reference speaker — lower `cfg_weight` to about 0.3. More expressive — `exaggeration` 0.7+ with `cfg_weight` about 0.3 (higher exaggeration speeds the speech up).
- The reference clip must be in the language of `language_id`; otherwise the speech inherits the reference's accent — then set `cfg_weight=0`.
- A cloned voice: only your own or one you have written consent for; never imitate a real person who has not agreed. Every output carries Resemble AI's inaudible Perth watermark, which survives MP3 encoding — record this in the asset list.
- Synthesis is not guaranteed verbatim: the same check as for any model applies — independent recognition of the finished audio, word-by-word comparison, regenerate on a mismatch [Audio] (`video-audio`, `voiceover.md`). faster-whisper below is that recognizer.
- Each file starts with a little silence; place a phrase by the start of speech in it, not by the start of the file [Popsci].
- Quality of Russian is not promised by the model being named in the source: listen to a test paragraph with names, numbers and terms before committing the whole voiceover to it.

## faster-whisper — word timestamps

- Install: `uv pip install faster-whisper` (CTranslate2; a CUDA GPU or CPU with `int8`). `scripts/words.py` wraps the call below and writes `words.json` and an `.srt`.

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="float16")  # CPU: device="cpu", compute_type="int8"
segments, info = model.transcribe("voice.wav", language="ru", word_timestamps=True,
                                  vad_filter=True, initial_prompt="HyperFrames, Remotion, ffmpeg")
for seg in segments:            # a generator: transcription runs while iterating
    for w in seg.words:
        print(w.start, w.end, w.word, w.probability)
```

Uses in a video:

- **Captions.** Group words into lines by pauses and length, not by a fixed count; a caption line appears at its first word and stays until it has been read [Video]. Then proofread by a person: terms, names, numbers and run-together words are where recognition fails [Audio]. Pass the project's terms in `initial_prompt` (or `hotwords`) to reduce, not remove, such errors.
- **Verbatim check of synthesis.** Recognize every generated phrase and compare word by word with the script; look at the differences with your eyes before rejecting [Audio].
- **Timing the picture to the voice.** Word starts give the moments for slides (0.5–0.7 s before the phrase) and for actions on screen; the start of the first word is the start of speech in the take [Video] [Popsci].
- **Cuts between words.** Word gaps say where a cut is safe; the lessons' own pause detector is in `video-audio`, `voiceover.md` [Popsci].
- Recognize the finished voice track, not the mix: music under the voice shifts word boundaries and adds hallucinated words in pauses (`vad_filter=True` helps against the latter).

## Tone.js — procedural sound

- Tone.js is Web Audio: it runs in a browser (or headless Chrome), not in plain Node. A live Tone.js transport inside a frame-by-frame render is not tied to the render's frames, so do not play it during the render.
- Render offline instead and mux the WAV in like any other track [Video] (the `video-render` skill, `mux-and-delivery.md`):

```js
import * as Tone from "tone";

const seconds = 12;
const buffer = await Tone.Offline(({ transport }) => {
  const synth = new Tone.PolySynth().toDestination();
  // times come from the shot table, in seconds — the same numbers the picture uses
  transport.schedule(t => synth.triggerAttackRelease(["C4", "G4"], "8n", t), 1.25);
  transport.start(0);
}, seconds, 2, 48000);

const audioBuffer = buffer.get();     // a standard AudioBuffer → encode to 16/24-bit WAV and save
```

- Schedule sound events from the same timings as the picture — the moment an object visibly lands, not the storyboard's estimate [Audio] (`video-audio`, `sound-design.md`).
- Any randomness (humanized timing, random notes) from a seeded generator, so that a re-render gives the same track and earlier versions reassemble byte for byte [Audio].
- Offline rendering runs faster than real time and has no dropouts; the result is then measured and mixed like a recorded file — Tone.js does not replace the loudness and true-peak checks.
