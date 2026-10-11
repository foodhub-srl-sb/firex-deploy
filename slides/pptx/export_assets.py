"""Esporta contenuti e illustrazioni del mazzo di benvenuto per la versione PowerPoint.

Uso:  python3 slides/pptx/export_assets.py [cartella_output]
Scrive deck.json e le illustrazioni SVG che build_benvenuto.js converte in PNG.
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import illustrations as ill  # noqa: E402
import content_benvenuto  # noqa: E402

out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "build"
(out / "svg").mkdir(parents=True, exist_ok=True)

(out / "deck.json").write_text(json.dumps(content_benvenuto.DECK, ensure_ascii=False, indent=1), encoding="utf-8")

labels = {}
for name in ("team", "puzzle", "devices", "routing"):
    svg = ill.get(name)
    (out / "svg" / f"{name}.svg").write_text(svg, encoding="utf-8")
    labels[name] = re.search(r'aria-label="([^"]*)"', svg).group(1)
(out / "svg" / "deco.svg").write_text(ill.SECTION_DECO, encoding="utf-8")
(out / "labels.json").write_text(json.dumps(labels, ensure_ascii=False, indent=1), encoding="utf-8")
print("esportato in", out)
