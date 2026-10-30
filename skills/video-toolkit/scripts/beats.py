# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy>=1.26"]
# ///
"""Measure a soundtrack before animating to it: a constant beat grid and per-frame audio features.

Usage:
  uv run beats.py track.wav [--fps 60] [--bands 4] [--min-bpm 60] [--max-bpm 200] [--out track.beats.json]

Needs ffmpeg on PATH (any input format it can decode).
Writes JSON:
  bpm, offset            constant grid: beat k is at offset + k * 60 / bpm (seconds)
  beats, downbeats       beat times; downbeats are a GUESS (bars assumed to be 4 beats)
  flags                  AMBIGUOUS_TEMPO, GRID_DRIFT, WEAK_PULSE — read them before trusting the grid
  frames                 per video frame: rms, bands (low..high), onset, beat_phase (0..1), all 0..1 normalised
                         and smoothed offline (fast attack, slow release) so visuals can read frames[n] directly
Prints the configuration, the result and the flags. The grid is a measurement, not a fact:
render a short clip with a metronome flash on the beats and let a person listen before building on it.
"""

from __future__ import annotations

import argparse
import math
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

SR = 22050
HOP = 256          # ~86 onset frames per second
NFFT = 2048
# Spectral flux of centred 2048-sample frames peaks before the hit; measured on synthetic kicks: 36 ms.
ONSET_LAG = 0.036


def decode(path: Path) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-i", f"file:{path}", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def spectrogram(y: np.ndarray) -> np.ndarray:
    pad = np.concatenate([np.zeros(NFFT // 2), y, np.zeros(NFFT // 2)])
    n = 1 + (len(pad) - NFFT) // HOP
    idx = np.arange(NFFT)[None, :] + HOP * np.arange(n)[:, None]
    frames = pad[idx] * np.hanning(NFFT)[None, :]
    return np.abs(np.fft.rfft(frames, axis=1))            # (frames, bins)


def log_bands(mag: np.ndarray, n: int, fmin=40.0, fmax=10000.0) -> np.ndarray:
    freqs = np.fft.rfftfreq(NFFT, 1 / SR)
    edges = np.geomspace(fmin, fmax, n + 1)
    out = np.zeros((mag.shape[0], n))
    for i in range(n):
        sel = (freqs >= edges[i]) & (freqs < edges[i + 1])
        out[:, i] = mag[:, sel].mean(axis=1) if sel.any() else 0.0
    return out


def onset_envelope(mag: np.ndarray) -> np.ndarray:
    b = np.log1p(1000 * log_bands(mag, 40))
    flux = np.maximum(0.0, np.diff(b, axis=0, prepend=b[:1])).sum(axis=1)
    flux -= np.convolve(flux, np.ones(16) / 16, mode="same")   # remove slow loudness changes
    flux = np.maximum(flux, 0.0)
    return flux / (flux.max() or 1.0)


def grid_score(env: np.ndarray, bpm: float, offset: float) -> float:
    rate = SR / HOP
    period = 60.0 / bpm
    t = np.arange(offset, len(env) / rate, period)
    if len(t) < 4:
        return 0.0
    return float(np.interp(t * rate, np.arange(len(env)), env).mean())


def best_phase(env: np.ndarray, bpm: float, t0: float = 0.0, t1: float | None = None) -> tuple[float, float]:
    rate = SR / HOP
    period = 60.0 / bpm
    seg = env[int(t0 * rate): int(t1 * rate) if t1 else None]
    phases = np.arange(0.0, period, 0.002)
    scores = [grid_score(seg, bpm, p) for p in phases]
    k = int(np.argmax(scores))
    return t0 + float(phases[k]), float(scores[k])


def tempo_candidates(env: np.ndarray, min_bpm: float, max_bpm: float) -> list[tuple[float, float]]:
    rate = SR / HOP
    x = env - env.mean()
    ac = np.correlate(x, x, mode="full")[len(x) - 1:]
    ac /= ac[0] or 1.0
    res = []
    for bpm in np.arange(min_bpm, max_bpm + 0.01, 0.5):
        lag = 60.0 / bpm * rate
        v = np.interp(lag, np.arange(len(ac)), ac)
        prior = np.exp(-0.5 * (np.log2(bpm / 120.0) / 0.9) ** 2)   # mild preference for ~120 BPM
        res.append((float(bpm), float(v * prior)))
    return sorted(res, key=lambda r: -r[1])


def smooth(x: np.ndarray, attack: float, release: float) -> np.ndarray:
    out = np.zeros_like(x)
    v = 0.0
    for i, s in enumerate(x):
        k = attack if s > v else release
        v = v + k * (s - v)
        out[i] = v
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", type=Path)
    ap.add_argument("--fps", type=float, default=60.0)
    ap.add_argument("--bands", type=int, default=4)
    ap.add_argument("--min-bpm", type=float, default=60.0)
    ap.add_argument("--max-bpm", type=float, default=200.0)
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()
    if not a.audio.is_file():
        print(f"no such file: {a.audio}", file=sys.stderr)
        return 2
    if not (all(math.isfinite(v) for v in (a.fps, a.min_bpm, a.max_bpm))
            and 0 < a.fps <= 1000 and 0 < a.bands <= 64 and 0 < a.min_bpm < a.max_bpm <= 1000):
        print("invalid --fps/--bands/--min-bpm/--max-bpm", file=sys.stderr)
        return 2
    out = a.out or a.audio.with_suffix(".beats.json")
    print(f"config: file={a.audio} sr={SR} hop={HOP} fps={a.fps} bands={a.bands} "
          f"bpm_range={a.min_bpm}-{a.max_bpm}", flush=True)

    y = decode(a.audio)
    dur = len(y) / SR
    if dur < 4.0:
        print(f"error: {dur:.2f} s of audio; a beat grid needs at least 4 s", file=sys.stderr)
        return 3
    if float(np.max(np.abs(y))) < 1e-4:
        print("error: the audio is silent (peak below -80 dBFS); nothing to measure", file=sys.stderr)
        return 3
    mag = spectrogram(y)
    env = onset_envelope(mag)
    flags: list[str] = []

    # Tempo: autocorrelation candidates, then a fine search of a constant grid around the best.
    cands = tempo_candidates(env, a.min_bpm, a.max_bpm)
    coarse = cands[0][0]
    best = (0.0, coarse, 0.0)
    for bpm in np.arange(coarse * 0.96, coarse * 1.04, 0.01):
        off, sc = best_phase(env, float(bpm))
        if sc > best[0]:
            best = (sc, float(bpm), off)
    score, bpm, offset = best
    if score <= 0.0:
        print("error: no onsets found; the track has no measurable pulse", file=sys.stderr)
        return 3
    offset = (offset + ONSET_LAG) % (60.0 / bpm)

    # Rival tempi: half, double, 2/3, 3/2 of the chosen one.
    rivals = []
    for f in (0.5, 2.0, 2 / 3, 1.5):
        rb = bpm * f
        if a.min_bpm * 0.98 <= rb <= a.max_bpm * 1.02:   # a rival just outside the range still counts
            _, rs = best_phase(env, rb)
            rivals.append((round(rb, 2), rs))
            # half and 2/3 tempo always fit a steady track about as well (they skip beats), so they count
            # only when clearly better; double and 3/2 count when nearly as good (strong off-beats)
            if rs > (1.15 if f < 1 else 0.9) * score:
                flags.append(f"AMBIGUOUS_TEMPO: {rb:.2f} BPM scores {rs / score:.0%} of {bpm:.2f}")
    if score < 2.0 * float(env.mean()):
        flags.append(f"WEAK_PULSE: grid score {score:.3f} vs mean onset {env.mean():.3f}")

    # Drift: the tempo measured in each 16-beat window must agree with the global constant grid.
    period = 60.0 / bpm
    win = 16 * period
    worst = 0.0
    local = []
    t = 0.0
    while t + win <= dur + 1e-9:
        lb, ls = bpm, -1.0
        for b in np.arange(bpm * 0.94, bpm * 1.06, 0.1):
            _, sc = best_phase(env, float(b), t, t + win)
            if sc > ls:
                lb, ls = float(b), sc
        local.append(round(lb, 1))
        # how far a local tempo would carry the grid off over one window, in seconds
        worst = max(worst, abs(16 * 60.0 / lb - win))
        t += win
    if worst > 0.045:
        flags.append(f"GRID_DRIFT: window tempi {min(local)}-{max(local)} BPM vs {bpm:.2f}; a constant grid is "
                     f"up to {worst * 1000:.0f} ms off within 16 beats — tempo is not constant, map sections separately")

    beats = [round(offset + k * period, 4) for k in range(int((dur - offset) / period) + 1)]

    # Downbeat guess: which beat index mod 4 carries the most low-band energy (kick).
    rate = SR / HOP
    low = log_bands(mag, 1, 40.0, 150.0)[:, 0]
    energy = [float(np.mean([np.interp((b - ONSET_LAG) * rate, np.arange(len(low)), low) for b in beats[k::4]] or [0]))
              for k in range(4)]
    k0 = int(np.argmax(energy))
    downbeats = beats[k0::4]

    # Per-frame features for visuals, normalised and smoothed offline.
    n = int(math.ceil(dur * a.fps - 1e-9))   # include the last, partial frame
    tf = np.arange(n) / a.fps
    pos = tf * rate
    grid = np.arange(mag.shape[0])
    rms_full = np.sqrt(np.mean(np.square(mag), axis=1))
    rms = np.interp(pos, grid, rms_full)
    bands = log_bands(mag, a.bands)
    bands_f = np.stack([np.interp(pos, grid, np.log1p(1000 * bands[:, i])) for i in range(a.bands)], axis=1)
    onset_f = np.interp((tf - ONSET_LAG) * rate, grid, env)

    def norm(x):
        hi = np.percentile(x, 99) or 1.0
        return np.clip(x / hi, 0, 1)

    att, rel = 1 - np.exp(-1 / (0.010 * a.fps)), 1 - np.exp(-1 / (0.200 * a.fps))
    rms_s = smooth(norm(rms), att, rel)
    bands_s = np.stack([smooth(norm(bands_f[:, i]), att, rel) for i in range(a.bands)], axis=1)
    onset_s = smooth(norm(onset_f), 1.0, 1 - np.exp(-1 / (0.120 * a.fps)))
    phase = ((tf - offset) / period) % 1.0

    result = {
        "config": {"file": str(a.audio), "fps": a.fps, "bands": a.bands, "sr": SR, "hop": HOP},
        "duration": round(dur, 4), "bpm": round(bpm, 2), "offset": round(offset, 4),
        "flags": flags, "rivals": rivals,
        "beats": beats, "downbeats": downbeats, "downbeat_is_guess": True,
        "frames": {
            "rms": np.round(rms_s, 4).tolist(),
            "bands": np.round(bands_s, 4).tolist(),
            "onset": np.round(onset_s, 4).tolist(),
            "beat_phase": np.round(phase, 4).tolist(),
        },
    }
    out.write_text(json.dumps(result, separators=(",", ":")), encoding="utf-8")

    print("--- summary ---")
    print(f"duration {dur:.2f} s, tempo {bpm:.2f} BPM, offset {offset:.3f} s, grid score {score:.3f}")
    print(f"beats {len(beats)}, downbeats (guess, beat index ≡ {k0} mod 4) {len(downbeats)}, frames {n} @ {a.fps} fps")
    print("half/double tempo always fits a steady track: confirm the tempo and the downbeat by ear")
    print(f"rivals: {', '.join(f'{b} BPM {s / score:.0%}' for b, s in rivals) or 'none'}")
    print(f"window tempi: {min(local) if local else bpm}-{max(local) if local else bpm} BPM, max drift per 16 beats: {worst * 1000:.0f} ms")
    print("flags: " + ("; ".join(flags) if flags else "none"))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
