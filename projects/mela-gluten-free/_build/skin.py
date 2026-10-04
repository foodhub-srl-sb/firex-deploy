"""Colore medio della pelle in un riquadro: RGB, tonalita (gradi) e saturazione."""
import colorsys
import sys

import numpy as np
from PIL import Image

for arg in sys.argv[1:]:
    path, box = arg.split("@")
    x0, y0, x1, y1 = map(int, box.split(","))
    a = np.asarray(Image.open(path).convert("RGB"))[y0:y1, x0:x1].reshape(-1, 3).astype(float)
    r, g, b = a.mean(0)
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    print(f"{path.split(chr(92))[-1]:28s} RGB=({r:5.1f},{g:5.1f},{b:5.1f})  tonalita={h*360:5.1f}  sat={s:.2f}  val={v:.2f}  R/G={r/g:.2f}")
