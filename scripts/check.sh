#!/usr/bin/env bash
# Checks the workspace toolchain without installing anything.
# Usage: scripts/check.sh [--doctor]
# Exit code: number of required items missing (0 = all good).
set -uo pipefail

DOCTOR=0
for arg in "$@"; do
  case "$arg" in
    --doctor) DOCTOR=1 ;;
    -h|--help) echo "Usage: $0 [--doctor]"; exit 0 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

has() { command -v "$1" >/dev/null 2>&1; }
MISSING=0
PY=python3; has python3 || PY=python

row() { printf '  %-4s %-15s %s\n' "$1" "$2" "$3"; }

# check <name> <required:1|0> <version command>
check() {
  local name=$1 req=$2 cmd=$3 out
  if has "$name" && out=$(eval "$cmd" 2>/dev/null | head -n1) && [ -n "$out" ]; then
    row ok "$name" "$out"
  elif [ "$req" -eq 1 ]; then
    row FAIL "$name" "missing (required)"; MISSING=$((MISSING+1))
  else
    row -- "$name" "missing (optional)"
  fi
}

echo "Toolchain check"
check node    1 "node --version"
if has node; then
  major=$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0)
  if [ "$major" -lt 22 ]; then
    row FAIL "node>=22" "found major $major, need 22+"; MISSING=$((MISSING+1))
  fi
fi
check npm     1 "npm --version"
check ffmpeg  1 "ffmpeg -version | awk '{print \$3}'"
check ffprobe 1 "ffprobe -version | awk '{print \$3}'"
check "$PY"   1 "$PY --version 2>&1"
check claude  1 "claude --version"

# Speech-to-text: need at least one of faster-whisper / whisper.cpp.
STT=0
if has "$PY" && fw=$("$PY" -c 'import faster_whisper; print(faster_whisper.__version__)' 2>/dev/null); then
  row ok faster-whisper "$fw"; STT=1
else
  row -- faster-whisper "missing (pip install faster-whisper)"
fi
wbin=""
for b in whisper-cli whisper-cpp; do has "$b" && { wbin=$b; break; }; done
if [ -n "$wbin" ]; then
  row ok whisper-cpp "$(command -v "$wbin")"; STT=1
else
  row -- whisper-cpp "missing (optional)"
fi
if [ "$STT" -eq 0 ]; then
  row FAIL whisper "no speech-to-text engine found"; MISSING=$((MISSING+1))
fi

if [ "$DOCTOR" -eq 1 ]; then
  echo; echo "HyperFrames doctor"
  if has npx; then
    npx --yes hyperframes doctor || MISSING=$((MISSING+1))
  else
    row FAIL npx "missing, cannot run doctor"; MISSING=$((MISSING+1))
  fi
fi

echo
if [ "$MISSING" -eq 0 ]; then
  echo "All required tools present."
else
  echo "$MISSING required item(s) missing. Run the installer for your OS in scripts/."
fi
exit "$MISSING"
