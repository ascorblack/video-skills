#!/usr/bin/env bash
# Evidence for the critic: frames at chosen moments, labelled with time and frame number, tiled on one image.
# Usage:
#   sheet.sh <video> <times> [out.jpg]
#     times: "0.5,2,3.75"  — those moments (seconds)
#            "3.2:3.6"     — every frame between 3.2 s and 3.6 s (a strip around a hit or a join)
#            "0:12:0.5"    — from 0 to 12 s every 0.5 s
# Environment:
#   COLS=4        columns of the tile
#   WIDTH=480     width of one cell in pixels (0 = native size, for checking small text)
#   CROP=w:h:x:y  crop every frame first (a face, a caption, a corner), in source pixels
# Prints the configuration, then the path of the sheet. Exit code 2 on a usage error.
set -euo pipefail

if [[ $# -lt 2 || ! -f "$1" ]]; then
  sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//' >&2
  exit 2
fi
in="$1"; spec="$2"; out="${3:-${in%.*}.sheet.jpg}"
cols="${COLS:-4}"; width="${WIDTH:-480}"; crop="${CROP:-}"
if ! [[ "$cols" =~ ^[1-9][0-9]*$ && "$width" =~ ^[0-9]+$ ]]; then
  echo "error: COLS must be a positive integer and WIDTH a non-negative integer (got COLS=$cols WIDTH=$width)" >&2
  exit 2
fi
if [[ -n "$crop" && ! "$crop" =~ ^[0-9]+:[0-9]+:[0-9]+:[0-9]+$ ]]; then
  echo "error: CROP must be w:h:x:y in pixels (got '$crop')" >&2
  exit 2
fi
src="file:$in"

fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=avg_frame_rate -of default=nw=1:nk=1 "$src")
rfps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=nw=1:nk=1 "$src")
if [[ "$fps" != "$rfps" ]]; then
  # frame numbers are computed as t * fps, which is only true at a constant frame rate
  echo "error: variable frame rate (avg $fps, r $rfps); make a CFR copy first: ffmpeg -i in -fps_mode cfr -r <fps> cfr.mp4" >&2
  exit 2
fi
fpsf=$(awk -v r="$fps" 'BEGIN { split(r, a, "/"); printf "%.6f", (a[2] ? a[1] / a[2] : a[1]) }')
dur=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$src")

# Expand the time spec into a list of times.
times=()
if [[ "$spec" == *:* ]]; then
  IFS=: read -r a b step <<< "$spec"
  step="${step:-$(awk -v f="$fpsf" 'BEGIN { printf "%.6f", 1 / f }')}"
  num='^[0-9]+([.][0-9]+)?$'
  if ! [[ "$a" =~ $num && "$b" =~ $num && "$step" =~ $num ]] || \
     ! awk -v a="$a" -v b="$b" -v s="$step" 'BEGIN { exit !(b > a && s > 0 && (b - a) / s < 120) }'; then
    echo "error: range must be a:b or a:b:step with numbers, b > a, step > 0, at most 120 frames (got '$spec')" >&2
    exit 2
  fi
  while read -r t; do times+=("$t"); done < <(awk -v a="$a" -v b="$b" -v s="$step" \
    'BEGIN { n = int((b - a) / s + 1e-6); for (i = 0; i <= n; i++) printf "%.4f\n", a + i * s }')
else
  IFS=, read -r -a times <<< "$spec"
fi
num='^[0-9]+([.][0-9]+)?$'
if [[ "$spec" == *:* ]]; then
  if ! [[ "$a" =~ $num && "$b" =~ $num && "$step" =~ $num ]] || ! awk -v a="$a" -v b="$b" -v s="$step" 'BEGIN { exit !(b > a && s > 0) }'; then
    echo "error: range must be a:b or a:b:step with numbers, b > a, step > 0 (got '$spec')" >&2
    exit 2
  fi
fi
last=$(awk -v d="$dur" -v f="$fpsf" 'BEGIN { printf "%.6f", d - 1 / f }')   # time of the last frame
for t in "${times[@]}"; do
  if ! [[ "$t" =~ $num ]] || ! awk -v t="$t" -v l="$last" -v f="$fpsf" 'BEGIN { exit !(t <= l + 0.5 / f) }'; then
    echo "error: time '$t' is not a number within 0..${last} s (the last frame)" >&2
    exit 2
  fi
done
n=${#times[@]}
if (( n == 0 || n > 120 )); then
  echo "error: $n frames requested; give 1..120" >&2
  exit 2
fi
echo "config: video=$in fps=$fps duration=${dur}s frames=$n cols=$cols width=${width:-native} crop=${crop:-none}"

tmp=$(mktemp -d)   # system temp: its path never contains ":"
trap 'rm -rf "$tmp"' EXIT

vf=""
[[ -n "$crop" ]] && vf="crop=${crop},"
[[ "$width" != "0" ]] && vf="${vf}scale=${width}:-2,"
i=0
for t in "${times[@]}"; do
  t=$(awk -v t="$t" -v l="$last" 'BEGIN { printf "%.4f", (t > l ? l : t) }')   # clamp rounding past the last frame
  frame=$(awk -v t="$t" -v f="$fpsf" 'BEGIN { printf "%d", t * f + 0.5 }')
  label="t=${t}s  f=${frame}"
  # drawtext needs ":" escaped inside the text
  # accurate seek returns the first frame at or after the seek point: aim a quarter frame before frame n
  seek=$(awk -v n="$frame" -v f="$fpsf" 'BEGIN { s = (n - 0.25) / f; printf "%.6f", (s < 0 ? 0 : s) }')
  ffmpeg -hide_banner -loglevel error -y -ss "$seek" -i "$src" -frames:v 1 \
    -vf "${vf}drawtext=text='${label//:/\\:}':fontcolor=white:fontsize=18:box=1:boxcolor=black@0.65:boxborderw=4:x=6:y=6" \
    "$tmp/$(printf '%04d' "$i").png"
  if [[ ! -s "$tmp/$(printf '%04d' "$i").png" ]]; then
    echo "error: no frame decoded at t=$t" >&2
    exit 1
  fi
  i=$((i + 1))
done

rows=$(( (n + cols - 1) / cols ))
ffmpeg -hide_banner -loglevel error -y -framerate 1 -i "$tmp/%04d.png" \
  -vf "tile=${cols}x${rows}:padding=4:color=gray" -frames:v 1 -q:v 3 "file:$out"
echo "sheet: $out (${n} frames, ${cols}x${rows})"
