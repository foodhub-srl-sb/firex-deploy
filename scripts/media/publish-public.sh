#!/usr/bin/env bash
# Pubblica un file nel repository PUBBLICO foodhub-srl-sb/media-pubblici e stampa il link https (jsDelivr)
# da usare come riferimento audio/video nei modelli che non accettano allegati (es. FLUX Video
# Edit, Runway Aleph, HeyGen Avatar IV).
#
# Solo file di passaggio: niente codice, niente chiavi, niente materiale riservato.
# Cancellali quando il job è finito con --remove.
#
# Uso:
#   scripts/media/publish-public.sh input/clip-720p.mp4          # stampa il link raw
#   scripts/media/publish-public.sh --remove 2026-10-02/clip-720p.mp4
set -euo pipefail
REPO="foodhub-srl-sb/media-pubblici"
DIR="${MEDIA_PUBLIC_DIR:-$HOME/.cache/media-pubblici}"
cd "$(dirname "$0")/../.."

if [ ! -d "$DIR/.git" ]; then
  git clone -q "https://github.com/$REPO.git" "$DIR" || {
    echo "Non riesco a clonare $REPO: esiste ed è pubblico? In una sessione cloud va aggiunto con accesso push." >&2
    exit 1
  }
fi
git -C "$DIR" pull -q --rebase || true

if [ "${1:-}" = "--remove" ]; then
  git -C "$DIR" rm -q "${2:?percorso da rimuovere}"
  git -C "$DIR" commit -q -m "Rimuove $2"
  git -C "$DIR" push -q
  echo "Rimosso $2 (resta nella cronologia del repository)."
  exit 0
fi

src="${1:?file da pubblicare}"
size=$(stat -c %s "$src" 2>/dev/null || stat -f %z "$src")
if [ "$size" -gt $((20 * 1024 * 1024)) ]; then
  echo "File troppo grande ($((size / 1024 / 1024)) MB): jsDelivr serve al massimo 20 MB, comprimilo." >&2
  exit 1
fi
dest="$(date -u +%F)/$(basename "$src")"
mkdir -p "$DIR/$(dirname "$dest")"
cp "$src" "$DIR/$dest"
git -C "$DIR" add "$dest"
git -C "$DIR" commit -q -m "File di passaggio: $dest"
for i in 1 2 3 4; do git -C "$DIR" push -q && break; sleep $((2 ** i)); done
# jsDelivr serve i file con il Content-Type giusto (video/mp4, audio/mpeg...), che alcuni modelli
# pretendono (Runway); raw.githubusercontent.com risponde sempre application/octet-stream.
# Il link punta al commit esatto, così la cache della CDN non serve mai una versione vecchia.
sha=$(git -C "$DIR" rev-parse HEAD)
echo "https://cdn.jsdelivr.net/gh/$REPO@$sha/$dest"
