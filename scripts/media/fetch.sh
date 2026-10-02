#!/usr/bin/env bash
# Scarica in locale i media generati dalla GitHub Action (branch media-store).
#
# Uso:
#   scripts/media/fetch.sh                 # elenca le richieste disponibili
#   scripts/media/fetch.sh tracciabilita   # copia media-store/tracciabilita/ in media/out/tracciabilita/
#   scripts/media/fetch.sh tracciabilita projects/mio/assets/ai   # in una cartella a scelta
set -euo pipefail
cd "$(dirname "$0")/../.."

for i in 1 2 3 4; do
  git fetch -q origin media-store && break
  [ "$i" = 4 ] && { echo "media-store non trovato: la GitHub Action non ha ancora pubblicato nulla." >&2; exit 1; }
  sleep $((2 ** i))
done

if [ $# -eq 0 ]; then
  echo "Richieste in media-store:"
  git ls-tree -d --name-only origin/media-store | sed 's/^/  /'
  exit 0
fi

id="$1"
dest="${2:-media/out/$id}"
if ! git cat-file -e "origin/media-store:$id" 2>/dev/null; then
  echo "Nessuna cartella '$id' in media-store." >&2
  exit 1
fi
mkdir -p "$dest"
git archive origin/media-store "$id" | tar -x -C "$dest" --strip-components=1
echo "Scaricato in $dest:"
ls -la "$dest"
if [ -f "$dest/result.json" ]; then
  python3 -c "
import json,sys
m=json.load(open('$dest/result.json'))
print(f\"spesi {m['spent_usd']} \$ su {m['max_usd']} \$\")
for j in m['jobs']: print(f\"  {j['name']:<24} {j['status']:<8} {j.get('cost_usd') or ''} {j.get('error') or j.get('reason') or ''}\")
"
fi
