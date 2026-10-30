# /// script
# requires-python = ">=3.10"
# dependencies = ["faster-whisper>=1.1", "av<19"]  # PyAV 19 removed av.open(metadata_errors=...), which faster-whisper 1.2.1 passes
# ///
"""Word timestamps of a voice track with faster-whisper.

Usage:
  uv run words.py voice.wav [--lang ru] [--model large-v3] [--device auto|cuda|cpu]
                  [--prompt "Term1, Term2"] [--max-chars 42] [--max-gap 0.6] [--out-dir DIR]

Writes next to the audio (or into --out-dir):
  <name>.words.json  [{"start": s, "end": s, "word": "...", "p": probability}, ...]
  <name>.srt         caption lines grouped by pauses and length
Prints the configuration it used, a progress line per segment and a compact summary.
Recognize the clean voice track, not the mix: music under the voice shifts word boundaries.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def group_lines(words: list[dict], max_chars: int, max_gap: float) -> list[list[dict]]:
    """Break into caption lines at pauses, at sentence ends and at a length limit."""
    lines: list[list[dict]] = []
    cur: list[dict] = []
    for w in words:
        text = " ".join(x["word"] for x in cur + [w])
        gap = w["start"] - cur[-1]["end"] if cur else 0.0
        if cur and (gap > max_gap or len(text) > max_chars):
            lines.append(cur)
            cur = []
        cur.append(w)
        if w["word"].endswith((".", "!", "?", "…")):
            lines.append(cur)
            cur = []
    if cur:
        lines.append(cur)
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", type=Path)
    ap.add_argument("--lang", default=None, help="language code, e.g. ru, en; default: detect")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    ap.add_argument("--prompt", default=None, help="terms and names to bias recognition towards")
    ap.add_argument("--max-chars", type=int, default=42)
    ap.add_argument("--max-gap", type=float, default=0.6, help="pause in seconds that starts a new line")
    ap.add_argument("--out-dir", type=Path, default=None)
    a = ap.parse_args()

    if not a.audio.is_file():
        print(f"no such file: {a.audio}", file=sys.stderr)
        return 2

    from faster_whisper import WhisperModel

    device = a.device
    if device == "auto":
        try:
            import ctranslate2

            device = "cuda" if ctranslate2.get_cuda_device_count() > 0 else "cpu"
        except Exception:
            device = "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    print(f"config: model={a.model} device={device} compute_type={compute_type} lang={a.lang or 'auto'} "
          f"max_chars={a.max_chars} max_gap={a.max_gap}", flush=True)

    model = WhisperModel(a.model, device=device, compute_type=compute_type)
    segments, info = model.transcribe(
        str(a.audio), language=a.lang, word_timestamps=True, vad_filter=True,
        initial_prompt=a.prompt, beam_size=5,
    )
    words: list[dict] = []
    for seg in segments:
        for w in seg.words or []:
            words.append({"start": round(w.start, 3), "end": round(w.end, 3),
                          "word": w.word.strip(), "p": round(w.probability, 3)})
        print(f"[{seg.start:7.2f} → {seg.end:7.2f}] {seg.text.strip()}", flush=True)

    out_dir = a.out_dir or a.audio.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = a.audio.stem
    (out_dir / f"{stem}.words.json").write_text(json.dumps(words, ensure_ascii=False, indent=1), encoding="utf-8")

    lines = group_lines(words, a.max_chars, a.max_gap)
    srt = []
    for i, line in enumerate(lines, 1):
        srt.append(f"{i}\n{srt_time(line[0]['start'])} --> {srt_time(line[-1]['end'])}\n"
                   + " ".join(w["word"] for w in line) + "\n")
    (out_dir / f"{stem}.srt").write_text("\n".join(srt), encoding="utf-8")

    low = [w for w in words if w["p"] < 0.5]
    print("--- summary ---")
    print(f"language: {info.language} (p={info.language_probability:.2f}), audio {info.duration:.2f} s")
    print(f"words: {len(words)}, caption lines: {len(lines)}")
    print(f"first word at {words[0]['start'] if words else '-'} s, last ends at {words[-1]['end'] if words else '-'} s")
    print(f"low-confidence words (p<0.5), proofread these: {', '.join(w['word'] for w in low[:30]) or 'none'}")
    print(f"wrote: {out_dir / (stem + '.words.json')}, {out_dir / (stem + '.srt')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
