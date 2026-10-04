#!/usr/bin/env bash
# Crea un nuovo progetto video HyperFrames 9:16 nello stile Food Hub.
#
# Uso:
#   scripts/new-project.sh <nome> [secondi] ["Titolo"]
#   scripts/new-project.sh filiera-latte 40 "La filiera del latte"
#
# Crea projects/<nome>/ dal template, genera musica ed effetti originali in
# projects/<nome>/audio/ (restano fuori da git) e una cartella assets/ai/ per i
# media generati con OpenRouter.
set -euo pipefail
cd "$(dirname "$0")/.."

name="${1:?uso: scripts/new-project.sh <nome> [secondi] [titolo]}"
secs="${2:-30}"
title="${3:-$name}"
if ! [[ "$name" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "Nome non valido: usa minuscole, numeri e trattini (es. filiera-latte)." >&2
  exit 1
fi
dest="projects/$name"
if [ -e "$dest" ]; then
  echo "$dest esiste già." >&2
  exit 1
fi

# Su Windows Python si chiama "python" (python3 non esiste).
PY=python3; command -v python3 >/dev/null 2>&1 || PY=python

cp -R templates/hyperframes-9x16 "$dest"
mkdir -p "$dest/assets/ai"
end=$("$PY" -c "print(round($secs - 3.6, 2))")
"$PY" - "$dest/index.html" "$secs" "$end" "$title" <<'PY'
import sys
path, secs, end, title = sys.argv[1:]
s = open(path, encoding="utf-8").read()
s = s.replace("{{DURATION}}", secs).replace("{{END}}", end).replace("{{S1}}", end).replace("{{TITLE}}", title)
open(path, "w", encoding="utf-8", newline="").write(s)
PY
sed -i.bak "s/{{NAME}}/$name/" "$dest/package.json" && rm -f "$dest/package.json.bak"
printf '{\n  "id": "%s",\n  "name": "%s",\n  "createdAt": "%s"\n}\n' "$name" "$title" "$(date -u +%FT%TZ)" > "$dest/meta.json"

"$PY" scripts/synth-audio.py --seconds "$secs" --music-out "$dest/audio/music.wav" >/dev/null
cp sfx/*.wav "$dest/audio/"
echo "Creato $dest ($secs s). Prossimi passi:"
echo "  cd $dest && npx hyperframes snapshot --frames 6"
