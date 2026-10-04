#!/usr/bin/env bash
# Installs the Food Hub video studio toolchain on macOS (Homebrew):
# Node 22+, FFmpeg, Poppler, whisper.cpp, Python packages (requirements.txt),
# Claude Code + HyperFrames, Chrome for rendering, RobustVideoMatting models.
# Usage: scripts/install-mac.sh [--yes]
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

# --- Homebrew ---
say "Homebrew"
if has brew; then
  ok "brew $(brew --version | head -n1 | awk '{print $2}')"
else
  warn "Homebrew not found."
  if confirm "Install Homebrew?"; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Put brew on PATH for this session (Apple Silicon / Intel)
    for b in /opt/homebrew/bin/brew /usr/local/bin/brew; do
      [ -x "$b" ] && eval "$("$b" shellenv)" && break
    done
  else
    echo "Homebrew is required. Aborting."; exit 1
  fi
fi

brew_install() { # brew_install <formula> <label>
  if confirm "Install $2 with 'brew install $1'?"; then
    brew install "$1"
  else
    warn "Skipped $2"
  fi
}

# --- Node.js 22+ ---
say "Node.js (>= 22)"
if has node && [ "$(node_major)" -ge 22 ]; then
  ok "node $(node --version)"
else
  if has node; then warn "node $(node --version) is older than 22"; fi
  brew_install node "Node.js"
  if has node && [ "$(node_major)" -lt 22 ]; then
    warn "node is still < 22. Try: brew upgrade node  (or brew link --overwrite node)"
  fi
fi

# --- FFmpeg ---
say "FFmpeg"
if has ffmpeg && has ffprobe; then
  ok "$(ffmpeg -version | head -n1)"
else
  brew_install ffmpeg "FFmpeg"
fi

# --- Python ---
say "Python 3"
if has python3; then
  ok "$(python3 --version)"
else
  brew_install python "Python 3"
fi

# --- whisper.cpp ---
say "whisper.cpp"
if has whisper-cli || has whisper-cpp; then
  ok "whisper.cpp present"
else
  brew_install whisper-cpp "whisper.cpp"
fi

# --- Poppler (PDF tools: pdftotext, pdfimages, pdftocairo) ---
say "Poppler (PDF tools)"
if has pdftotext && has pdfimages && has pdftocairo; then
  ok "$(pdftotext -v 2>&1 | head -n1)"
else
  brew_install poppler "Poppler"
fi

# --- Python packages (requirements.txt) ---
# On Apple Silicon the standard onnxruntime already uses the GPU/Neural Engine (CoreML).
say "Python packages (faster-whisper, numpy, scipy, pillow, onnxruntime)"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if has python3; then
  if python3 -c 'import faster_whisper, numpy, scipy, PIL, onnxruntime' >/dev/null 2>&1; then
    ok "all Python packages present"
  elif confirm "Install the Python packages from requirements.txt (user site)?"; then
    # Homebrew Python is "externally managed" (PEP 668); fall back if needed.
    python3 -m pip install --user --upgrade -r "$ROOT/requirements.txt" \
      || python3 -m pip install --user --upgrade --break-system-packages -r "$ROOT/requirements.txt" \
      || warn "pip install failed. Consider a venv: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
  else
    warn "Skipped Python packages"
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

# --- OpenRouter key (optional, for AI images and video from this Mac) ---
say "OpenRouter (optional)"
if [ -n "${OPENROUTER_API_KEY:-}" ]; then
  ok "OPENROUTER_API_KEY is set in this shell"
else
  echo "  AI generation already works through the GitHub Action (repository secret)."
  echo "  To generate directly from this Mac, add to ~/.zshrc (never to a file in the repo):"
  echo "      export OPENROUTER_API_KEY=\"sk-or-...\""
fi

# --- Summary ---
say "Installed versions"
v() { if has "$1"; then printf '  %-15s %s\n' "$1" "$(eval "$2" 2>/dev/null | head -n1)"; else printf '  %-15s %s\n' "$1" "MISSING"; fi; }
v node           "node --version"
v npm            "npm --version"
v ffmpeg         "ffmpeg -version | awk '{print \$3}'"
v ffprobe        "ffprobe -version | awk '{print \$3}'"
v python3        "python3 --version"
v whisper-cli    "echo present"
v claude         "claude --version"
v pdftotext      "pdftotext -v 2>&1"
for mod in faster_whisper numpy scipy PIL onnxruntime; do
  if has python3 && ver=$(python3 -c "import $mod; print(getattr($mod, '__version__', 'ok'))" 2>/dev/null); then
    printf '  %-15s %s\n' "$mod" "$ver"
  else
    printf '  %-15s %s\n' "$mod" MISSING
  fi
done
echo
echo "Done. Run scripts/check.sh anytime to re-verify."
