"""Genera i video del calendario (una cartella per pagina) dal modello unico.

    python src/build.py   (da project/)

Per ogni giornata in src/giornate.js e ogni pagina crea calendario-<giornata>-<pagina>/,
un progetto HyperFrames autonomo che condivide project/assets.
Render: cd calendario-10nov-1 && npm run render -- -o ../../renders/calendario-10nov-1.mp4
"""
import json
import os
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
DURATION = 15
PAGES = [("9nov", 1), ("9nov", 2), ("10nov", 1), ("10nov", 2), ("11nov", 1), ("11nov", 2)]

shapes = json.loads((SRC / "shapes.json").read_text())
strip_ns = lambda s: s.strip().replace(' xmlns="http://www.w3.org/2000/svg"', "")

fest = strip_ns((ROOT / "assets" / "festival-mark.svg").read_text())
vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', fest).group(1).split()]
fest = fest.replace(
    "<svg ",
    f'<svg id="festMark" style="left:{vb[0]}px;top:{vb[1]}px;width:{vb[2]}px;height:{vb[3]}px" ',
    1,
)

base = (SRC / "calendario.html.tpl").read_text()
common = {
    "{{DURATION}}": str(DURATION),
    "{{WAVE_DARK}}": shapes["waveDark"]["d"],
    "{{WAVE_LIGHT}}": shapes["waveLight"]["d"],
    "{{BLOB_DARK}}": shapes["blobDark"]["d"],
    "{{BLOB_LIGHT}}": shapes["blobLight"]["d"],
    "{{BANNER}}": shapes["banner"]["d"],
    "{{FEST_MARK}}": fest,
    "{{FH_LOGO}}": strip_ns((ROOT / "assets" / "foodhub-logo.svg").read_text()),
    "{{DATA}}": (SRC / "giornate.js").read_text(),
}

for day, page in PAGES:
    name = f"calendario-{day}-{page}"
    d = ROOT / name
    d.mkdir(exist_ok=True)
    for f in ("package.json", "hyperframes.json"):
        shutil.copy(ROOT / f, d / f)
    (d / "meta.json").write_text(json.dumps({"id": name, "name": f"Calendario {day} - pagina {page}"}, indent=2) + "\n")
    link = d / "assets"
    if not link.exists():
        os.symlink("../assets", link)
    html = base
    for k, v in {**common, "{{DAY}}": day, "{{PAGE}}": str(page)}.items():
        html = html.replace(k, v)
    assert not re.search(r"{{[A-Z_]+}}", html), name
    (d / "index.html").write_text(html)
    print("scritto", d / "index.html")
