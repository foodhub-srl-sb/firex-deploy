#!/usr/bin/env bash
# Installs the video-editing workspace toolchain on Debian/Ubuntu (apt).
# Usage: scripts/install-linux.sh [--yes]
set -euo pipefail

YES=0
for arg in "$@"; do
  case "$arg" in
    -y|--yes) YES=1 ;;
    -h|--help) echo "Usage: $0 [--yes]"; exit 0 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

say()  { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
ok()   { printf '  ok  %s\n' "$*"; }
warn() { printf '  !!  %s\n' "$*" >&2; }
has()  { command -v "$1" >/dev/null 2>&1; }

confirm() {
  [ "$YES" -eq 1 ] && return 0
  local reply
  read -r -p "  $1 [y/N] " reply || true
  [[ "$reply" =~ ^[Yy]$ ]]
}

node_major() { node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0; }

if ! has apt-get; then
  echo "apt-get not found: this script supports Debian/Ubuntu only." >&2
  exit 1
fi

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  if has sudo; then SUDO="sudo"; else echo "Run as root or install sudo." >&2; exit 1; fi
fi

APT_UPDATED=0
apt_install() {
  if [ "$APT_UPDATED" -eq 0 ]; then $SUDO apt-get update -y; APT_UPDATED=1; fi
  $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y "$@"
}

# --- Node.js 22+ (NodeSource) ---
say "Node.js (>= 22)"
if has node && [ "$(node_major)" -ge 22 ]; then
  ok "node $(node --version)"
else
  if has node; then warn "node $(node --version) is older than 22"; fi
  if confirm "Install Node.js 22 from NodeSource?"; then
    apt_install ca-certificates curl gnupg
    curl -fsSL https://deb.nodesource.com/setup_22.x | $SUDO -E bash -
    $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs
  else
    warn "Skipped Node.js"
  fi
fi

# --- FFmpeg ---
say "FFmpeg"
if has ffmpeg && has ffprobe; then
  ok "$(ffmpeg -version | head -n1)"
elif confirm "Install ffmpeg with apt?"; then
  apt_install ffmpeg
else
  warn "Skipped FFmpeg"
fi

# --- Python + pip ---
say "Python 3 + pip"
if has python3 && python3 -m pip --version >/dev/null 2>&1; then
  ok "$(python3 --version), $(python3 -m pip --version | awk '{print "pip "$2}')"
elif confirm "Install python3 and python3-pip with apt?"; then
  apt_install python3 python3-pip python3-venv
else
  warn "Skipped Python"
fi

# --- faster-whisper ---
say "faster-whisper (Python)"
if has python3 && python3 -c 'import faster_whisper' >/dev/null 2>&1; then
  ok "faster-whisper $(python3 -c 'import faster_whisper; print(faster_whisper.__version__)' 2>/dev/null || echo '?')"
elif has python3; then
  if confirm "Install faster-whisper with pip (user site)?"; then
    # Newer distros mark system Python as externally managed (PEP 668).
    python3 -m pip install --user --upgrade faster-whisper \
      || python3 -m pip install --user --upgrade --break-system-packages faster-whisper \
      || warn "pip install failed. Consider a venv: python3 -m venv .venv && .venv/bin/pip install faster-whisper"
  else
    warn "Skipped faster-whisper"
  fi
else
  warn "python3 missing, cannot install faster-whisper"
fi

# --- Claude Code + HyperFrames plugin ---
say "Claude Code + HyperFrames plugin"
if has claude; then
  ok "claude $(claude --version 2>/dev/null | head -n1)"
  if confirm "Add HyperFrames marketplace and install the plugin?"; then
    claude plugin marketplace add heygen-com/hyperframes || warn "marketplace add failed (maybe already added)"
    claude plugin install hyperframes@hyperframes || warn "plugin install failed (maybe already installed)"
  fi
else
  warn "Claude Code not found. Install it with:"
  echo "      curl -fsSL https://claude.ai/install.sh | bash"
  echo "    then re-run this script to add the HyperFrames plugin."
fi

# --- HyperFrames doctor ---
say "HyperFrames doctor"
if has npx; then
  npx --yes hyperframes doctor || warn "hyperframes doctor reported problems"
else
  warn "npx missing, skipping doctor"
fi

# --- Summary ---
say "Installed versions"
v() { if has "$1"; then printf '  %-15s %s\n' "$1" "$(eval "$2" 2>/dev/null | head -n1)"; else printf '  %-15s %s\n' "$1" "MISSING"; fi; }
v node     "node --version"
v npm      "npm --version"
v ffmpeg   "ffmpeg -version | awk '{print \$3}'"
v ffprobe  "ffprobe -version | awk '{print \$3}'"
v python3  "python3 --version"
v claude   "claude --version"
if has python3 && python3 -c 'import faster_whisper' >/dev/null 2>&1; then
  printf '  %-15s %s\n' faster-whisper "$(python3 -c 'import faster_whisper; print(faster_whisper.__version__)')"
else
  printf '  %-15s %s\n' faster-whisper MISSING
fi
echo
echo "Done. Run scripts/check.sh anytime to re-verify."
