"""Genera i due video del calendario dal modello unico.

    python src/build.py   (da project/)

Pagina 1 -> calendario-1/index.html   (render: cd calendario-1 && npm run render)
Pagina 2 -> calendario-2/index.html   (render: cd calendario-2 && npm run render)
Ogni cartella e' un progetto HyperFrames autonomo che condivide project/assets.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
DURATION = 15

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
}
import os, shutil
for page in (1, 2):
    d = ROOT / f"calendario-{page}"
    d.mkdir(exist_ok=True)
    for f in ("package.json", "hyperframes.json"):
        shutil.copy(ROOT / f, d / f)
    (d / "meta.json").write_text(json.dumps({"id": f"calendario-{page}", "name": f"Calendario 9 novembre - pagina {page}"}, indent=2))
    link = d / "assets"
    if not link.exists():
        os.symlink("../assets", link)
    out = d / "index.html"
    html = base
    for k, v in {**common, "{{PAGE}}": str(page)}.items():
        html = html.replace(k, v)
    assert "{{" not in html, out
    out.write_text(html)
    print("scritto", out)
