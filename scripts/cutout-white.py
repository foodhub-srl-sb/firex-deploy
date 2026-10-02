#!/usr/bin/env python3
"""Scontorna un'immagine su fondo bianco (o quasi bianco) e salva un PNG trasparente.

Il fondo viene trovato partendo dai bordi (flood fill), quindi le zone chiare
interne al soggetto, come uno schermo grigio, restano intatte.

Uso:
    python scripts/cutout-white.py input/canva/mela.jpg assets/mela.png
    python scripts/cutout-white.py in.jpg out.png --tol 28 --feather 1.5
    python scripts/cutout-white.py ramo.jpg ramo.png --holes 40   # anche il bianco tra le foglie
"""
import argparse
from collections import deque

import numpy as np
from PIL import Image, ImageFilter


def cutout(src, dst, tol=30, feather=1.2, pad=8, holes=0):
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    dist = 255 - a.min(axis=2)  # 0 = bianco puro
    bg = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        q.append((0, x))
        q.append((h - 1, x))
    for y in range(h):
        q.append((y, 0))
        q.append((y, w - 1))
    while q:
        y, x = q.popleft()
        if bg[y, x] or dist[y, x] > tol:
            continue
        bg[y, x] = True
        if y > 0:
            q.append((y - 1, x))
        if y < h - 1:
            q.append((y + 1, x))
        if x > 0:
            q.append((y, x - 1))
        if x < w - 1:
            q.append((y, x + 1))
    if holes:
        # buchi interni (es. bianco tra le foglie): zone quasi bianche chiuse, più grandi di `holes` pixel
        seen = bg.copy()
        for sy in range(h):
            for sx in range(w):
                if seen[sy, sx] or dist[sy, sx] > tol:
                    continue
                comp = []
                q.append((sy, sx))
                seen[sy, sx] = True
                while q:
                    y, x = q.popleft()
                    comp.append((y, x))
                    for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                        if 0 <= ny < h and 0 <= nx < w and not seen[ny, nx] and dist[ny, nx] <= tol:
                            seen[ny, nx] = True
                            q.append((ny, nx))
                if len(comp) >= holes:
                    for y, x in comp:
                        bg[y, x] = True
    alpha = Image.fromarray(np.where(bg, 0, 255).astype(np.uint8))
    # bordo morbido: si erode di un pixel e si sfuma, così non resta l'alone bianco
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(feather))
    out = im.convert("RGBA")
    out.putalpha(alpha)
    bbox = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox:
        l, t, r, b = bbox
        out = out.crop((max(0, l - pad), max(0, t - pad), min(w, r + pad), min(h, b + pad)))
    out.save(dst)
    print(f"{dst}: {out.size[0]}x{out.size[1]}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--tol", type=int, default=30)
    ap.add_argument("--feather", type=float, default=1.2)
    ap.add_argument("--holes", type=int, default=0, help="rimuove anche i buchi bianchi interni più grandi di N pixel")
    a = ap.parse_args()
    cutout(a.src, a.dst, a.tol, a.feather, holes=a.holes)
