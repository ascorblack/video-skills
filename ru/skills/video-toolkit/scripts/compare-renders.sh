#!/usr/bin/env bash
# Compare two renders frame by frame by checksums of the decoded frames.
# Identical source + deterministic scene => identical decoded frames, whatever the container says.
# Usage: compare-renders.sh <a.mp4> <b.mp4>
# Exit code: 0 identical, 1 frames differ, 2 usage error.
set -euo pipefail

if [[ $# -ne 2 || ! -f "$1" || ! -f "$2" ]]; then
  echo "usage: $0 <a> <b>" >&2
  exit 2
fi

sums() {
  # framemd5 lines: stream, dts, pts, duration, size, md5 — keep "pts md5" of the video stream
  ffmpeg -hide_banner -loglevel error -i "file:$1" -map 0:v:0 -f framemd5 - | awk -F', *' '!/^#/ {print $3, $6}'
}

# Timing first: identical pictures at a different frame rate or length are not the same render.
timing() { ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,avg_frame_rate,nb_frames,time_base:format=duration -of default=nw=1 "file:$1" | sort; }
ta=$(timing "$1"); tb=$(timing "$2")
if [[ "$ta" != "$tb" ]]; then
  echo "result:    TIMING DIFFERS"
  diff <(echo "$ta") <(echo "$tb") | sed 's/^/           /'
  exit 1
fi

a=$(sums "$1"); b=$(sums "$2")
# Per-frame presentation times (same time base, checked above): a variable-frame-rate render can
# match on aggregate fps and duration while its frames sit at different moments.
ptsdiff=$(paste -d' ' <(cut -d' ' -f1 <<< "$a") <(cut -d' ' -f1 <<< "$b") | awk '$1 != $2 {print NR - 1}')
if [[ -n "$ptsdiff" ]]; then
  echo "result:    FRAME TIMES DIFFER at frame(s): $(head -n 20 <<< "$ptsdiff" | tr '\n' ' ')"
  exit 1
fi
na=$(wc -l <<< "$a"); nb=$(wc -l <<< "$b")
diffs=$(paste -d' ' <(cut -d' ' -f2 <<< "$a") <(cut -d' ' -f2 <<< "$b") | awk '$1 != $2 {print NR - 1}')
ndiff=$(grep -c . <<< "$diffs" || true)

echo "frames:    $na vs $nb"
if [[ "$na" -eq "$nb" && "$ndiff" -eq 0 ]]; then
  echo "result:    IDENTICAL"
  exit 0
fi
echo "result:    $ndiff differing frame(s)"
if [[ "$ndiff" -gt 0 ]]; then
  echo "first:     $(head -n 20 <<< "$diffs" | tr '\n' ' ')"
fi
# How large the differences are: a hardware encoder may not be bit-exact between runs,
# then every frame differs by noise (PSNR above ~50 dB); a scene leak gives a few frames far below.
ffmpeg -hide_banner -nostats -i "file:$1" -i "file:$2" -lavfi "[0:v][1:v]psnr=stats_file=-" -f null - 2>/dev/null \
  | awk '{for (i = 1; i <= NF; i++) if ($i ~ /^psnr_avg:/) {split($i, kv, ":"); v = kv[2];
          if (v == "inf") continue; n++; if (min == "" || v + 0 < min) {min = v + 0; at = $1}}}
         END {if (n) printf "min PSNR:  %.2f dB at %s (%d of the compared frames not identical)\n", min, at, n;
              else print "min PSNR:  inf (pixels identical, only the encoded streams differ)"}'
echo "hint:      for a strict test render both runs with the same software encoder settings, or to PNG frames"
exit 1
