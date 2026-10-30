#!/usr/bin/env bash
# Automatic QA pass over a finished video.
# Usage: qa.sh <video> [out-dir]
# Writes into out-dir (default: <video-name>.qa/):
#   probe.json        ffprobe of format and streams
#   summary.txt       the compact verdict printed at the end
#   detect.log        black segments (blackdetect) and frozen segments (freezedetect)
#   loudness.log      EBU R128 integrated loudness, LRA, true peak
#   sheet.jpg         contact sheet: 4x4 frames evenly over the video
#   first.png last.png  the first and the last frame at full size
set -euo pipefail

if [[ $# -lt 1 || ! -f "$1" ]]; then
  echo "usage: $0 <video> [out-dir]" >&2
  exit 2
fi
in="$1"
out="${2:-${in%.*}.qa}"
mkdir -p "$out"
# ffmpeg reads "name:" as a protocol; the file: prefix makes any path (with ":" in it) a plain file.
src="file:$in"; dst="file:$out"

ffprobe -v error -show_format -show_streams -of json "$src" > "$out/probe.json"

field() { ffprobe -v error -select_streams "$1" -show_entries "stream=$2" -of default=nw=1:nk=1 "$src" | head -n1; }
duration=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$src")
vcodec=$(field v:0 codec_name); width=$(field v:0 width); height=$(field v:0 height)
fps=$(field v:0 avg_frame_rate); pixfmt=$(field v:0 pix_fmt)
vdur=$(field v:0 duration || true)
acodec=$(field a:0 codec_name || true); adur=$(field a:0 duration || true)
arate=$(field a:0 sample_rate || true)

# Black and frozen segments in one decode pass.
# Both filters log to stderr (no file path inside the filter string, so any output path is safe).
if ! ffmpeg -hide_banner -nostats -i "$src" -an \
  -vf "blackdetect=d=0.1:pix_th=0.10,freezedetect=n=-60dB:d=0.5" \
  -f null - 2> "$out/detect.log"; then
  echo "error: detection pass failed, see $out/detect.log" >&2
  exit 1
fi
black=$(grep -c 'black_start' "$out/detect.log" || true)
freeze=$(grep -c 'freeze_start' "$out/detect.log" || true)

# Loudness: integrated LUFS, loudness range, true peak.
if [[ -n "$acodec" ]]; then
  ffmpeg -hide_banner -nostats -i "$src" -vn -af ebur128=peak=true -f null - 2> "$out/loudness.log" || true
  lufs=$(grep -A12 'Summary:' "$out/loudness.log" | awk '/I:/ {print $2; exit}')
  lra=$(grep -A12 'Summary:' "$out/loudness.log" | awk '/LRA:/ {print $2; exit}')
  tp=$(grep -A14 'Summary:' "$out/loudness.log" | awk '/Peak:/ {print $2; exit}')
fi

# Contact sheet: 16 frames evenly over the duration, and the first and last frame.
n=16
step=$(awk -v d="$duration" -v n="$n" 'BEGIN { printf "%.3f", d / n }')
ffmpeg -hide_banner -loglevel error -y -i "$src" \
  -vf "fps=1/${step},scale=360:-2,tile=4x4:padding=4:color=gray" -frames:v 1 "$dst/sheet.jpg"
ffmpeg -hide_banner -loglevel error -y -i "$src" -frames:v 1 "$dst/first.png"
ffmpeg -hide_banner -loglevel error -y -sseof -0.5 -i "$src" -update 1 "$dst/last.png"

{
  echo "file:      $in"
  echo "video:     $vcodec ${width}x${height} @ ${fps} fps, $pixfmt, ${vdur:-?} s"
  if [[ -n "$acodec" ]]; then
    echo "audio:     $acodec ${arate} Hz, ${adur:-?} s"
    echo "loudness:  ${lufs:-?} LUFS integrated, LRA ${lra:-?} LU, true peak ${tp:-?} dBFS"
  else
    echo "audio:     NONE"
  fi
  echo "duration:  $duration s"
  echo "black:     $black segment(s) >= 0.1 s   (see detect.log)"
  echo "frozen:    $freeze segment(s) >= 0.5 s  (see detect.log; holds on purpose are expected)"
  echo "sheet:     $out/sheet.jpg   first/last: $out/first.png $out/last.png"
} | tee "$out/summary.txt"
