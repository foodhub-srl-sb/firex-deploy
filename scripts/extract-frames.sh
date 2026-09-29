#!/usr/bin/env bash
# Extracts JPG frames from a video so Claude can look at them.
# Usage:
#   scripts/extract-frames.sh input/take.mp4 [fps=1] [outdir]
#   scripts/extract-frames.sh input/take.mp4 --at 7.2 [outdir]
# Default outdir: frames/<stem>/. Writes index.txt (frame -> seconds).
set -euo pipefail

usage() { sed -n '2,6p' "$0" | sed 's/^# \{0,1\}//'; }

[ $# -ge 1 ] || { usage; exit 2; }
case "$1" in -h|--help) usage; exit 0 ;; esac

IN=$1; shift
[ -f "$IN" ] || { echo "Input not found: $IN" >&2; exit 1; }
command -v ffmpeg >/dev/null || { echo "ffmpeg not found (run scripts/check.sh)" >&2; exit 1; }

stem=$(basename "${IN%.*}")
AT=""
FPS=1
OUT=""

if [ "${1:-}" = "--at" ]; then
  [ $# -ge 2 ] || { echo "--at needs a time in seconds" >&2; exit 2; }
  AT=$2; shift 2
  OUT=${1:-frames/$stem}
else
  FPS=${1:-1}
  OUT=${2:-frames/$stem}
fi
mkdir -p "$OUT"

# Single frame mode
if [ -n "$AT" ]; then
  file="$OUT/frame_at_${AT}s.jpg"
  ffmpeg -hide_banner -loglevel error -y -ss "$AT" -i "$IN" -frames:v 1 -q:v 2 "$file"
  printf '%s\t%s\n' "$(basename "$file")" "$AT" >> "$OUT/index.txt"
  echo "$file"
  exit 0
fi

# Sequence mode: clear old frames so the index matches the files.
rm -f "$OUT"/frame_[0-9]*.jpg "$OUT/index.txt"
ffmpeg -hide_banner -loglevel error -y -i "$IN" -vf "fps=$FPS" -q:v 2 "$OUT/frame_%04d.jpg"

# fps may be a fraction like 1/2. fps filter emits frame n (1-based) at t = (n-1)/fps.
n=0
: > "$OUT/index.txt"
for f in "$OUT"/frame_[0-9]*.jpg; do
  [ -e "$f" ] || continue
  n=$((n+1))
  t=$(awk -v n="$n" -v fps="$FPS" 'BEGIN{ k=split(fps,a,"/"); r=(k==2)?a[1]/a[2]:a[1]; printf "%.3f", (n-1)/r }')
  printf '%s\t%s\n' "$(basename "$f")" "$t" >> "$OUT/index.txt"
done
echo "Extracted $n frame(s) at ${FPS} fps into $OUT (index: $OUT/index.txt)"
