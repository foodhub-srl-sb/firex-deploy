#!/usr/bin/env bash
# Installs the Food Hub video studio toolchain on Debian/Ubuntu (apt):
# Node 22+, FFmpeg, Poppler, Python packages (requirements.txt), Claude Code + HyperFrames,
# Chrome for rendering, RobustVideoMatting models.
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

# --- Poppler (PDF tools: pdftotext, pdfimages, pdftocairo) ---
say "Poppler (PDF tools)"
if has pdftotext && has pdfimages && has pdftocairo; then
  ok "$(pdftotext -v 2>&1 | head -n1)"
elif confirm "Install poppler-utils with apt?"; then
  apt_install poppler-utils
else
  warn "Skipped Poppler (needed to read PDFs for motion-graphics videos)"
fi

# --- Python packages (requirements.txt) ---
say "Python packages (faster-whisper, numpy, scipy, pillow, onnxruntime)"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
pip_user() {
  # Newer distros mark system Python as externally managed (PEP 668).
  python3 -m pip install --user --upgrade "$@" \
    || python3 -m pip install --user --upgrade --break-system-packages "$@"
}
if has python3; then
  if python3 -c 'import faster_whisper, numpy, scipy, PIL, onnxruntime' >/dev/null 2>&1; then
    ok "all Python packages present"
  elif confirm "Install the Python packages from requirements.txt (user site)?"; then
    pip_user -r "$ROOT/requirements.txt" \
      || warn "pip install failed. Consider a venv: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
  else
    warn "Skipped Python packages"
  fi
  if has nvidia-smi && ! python3 -c 'import onnxruntime as o; assert "CUDAExecutionProvider" in o.get_available_providers()' >/dev/null 2>&1; then
    if confirm "NVIDIA GPU found: switch to onnxruntime-gpu for much faster person cutouts (RVM)?"; then
      python3 -m pip uninstall -y onnxruntime >/dev/null 2>&1 || true
      pip_user onnxruntime-gpu || warn "onnxruntime-gpu install failed, keeping the CPU version"
    fi
  fi
else
  warn "python3 missing, cannot install Python packages"
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

# --- HyperFrames: Chrome for rendering + doctor ---
say "HyperFrames (Chrome for rendering + doctor)"
if has npx; then
  npx --yes hyperframes browser ensure || warn "could not prepare Chrome for rendering"
  npx --yes hyperframes doctor || warn "hyperframes doctor reported problems"
else
  warn "npx missing, skipping HyperFrames setup"
fi

# --- RobustVideoMatting models (person cutouts) ---
say "RobustVideoMatting models (~120 MB, once)"
if has python3 && python3 -c 'import onnxruntime' >/dev/null 2>&1; then
  if confirm "Download the RVM models now?"; then
    python3 "$ROOT/scripts/rvm-matte.py" --prepare || warn "model download failed (it will retry on first use)"
  fi
else
  warn "onnxruntime missing, skipping RVM models"
fi

# --- OpenRouter key (optional, for AI images and video from this PC) ---
say "OpenRouter (optional)"
if [ -n "${OPENROUTER_API_KEY:-}" ]; then
  ok "OPENROUTER_API_KEY is set in this shell"
else
  echo "  AI generation already works through the GitHub Action (repository secret)."
  echo "  To generate directly from this PC, add to ~/.bashrc (never to a file in the repo):"
  echo "      export OPENROUTER_API_KEY=\"sk-or-...\""
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
v pdftotext "pdftotext -v 2>&1"
for mod in faster_whisper numpy scipy PIL onnxruntime; do
  if has python3 && ver=$(python3 -c "import $mod; print(getattr($mod, '__version__', 'ok'))" 2>/dev/null); then
    printf '  %-15s %s\n' "$mod" "$ver"
  else
    printf '  %-15s %s\n' "$mod" MISSING
  fi
done
echo
echo "Done. Run scripts/check.sh anytime to re-verify."
