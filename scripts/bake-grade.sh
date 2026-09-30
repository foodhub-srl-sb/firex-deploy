#!/usr/bin/env bash
# Applica una correzione colore a un video con alfa (webm VP9) e la salva nel file,
# così il render non deve calcolarla fotogramma per fotogramma (molto più veloce).
#
# Uso: scripts/bake-grade.sh IN.webm OUT.webm [R_GAIN R_OFF G_GAIN G_OFF B_GAIN B_OFF]
#
# I valori predefiniti riproducono la correzione usata nel reel di prova
# (meno verde del LED, pelle più calda): misurati confrontando un fotogramma
# corretto da HyperFrames con l'originale (errore medio < 2/255).
set -euo pipefail

if [ $# -lt 2 ]; then
  sed -n '2,10p' "$0"; exit 2
fi
IN=$1; OUT=$2
RG=${3:-1.0659}; RO=${4:--2.02}
GG=${5:-1.0801}; GO=${6:--14.31}
BG=${7:-1.0797}; BO=${8:--12.05}

ffmpeg -v error -y -c:v libvpx-vp9 -i "$IN" \
  -vf "format=rgba,lutrgb=r='clip(val*${RG}+(${RO}),0,255)':g='clip(val*${GG}+(${GO}),0,255)':b='clip(val*${BG}+(${BO}),0,255)'" \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 18 -row-mt 1 -auto-alt-ref 0 \
  -metadata:s:v:0 alpha_mode=1 -an "$OUT"
echo "Scritto $OUT"
