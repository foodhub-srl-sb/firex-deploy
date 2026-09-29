#!/usr/bin/env python3
"""Pulisce una maschera (webm con alfa) dai pezzi di logo rimasti attaccati alla persona.

Dentro una zona ricostruisce la parete vuota con la mediana di tutti i fotogrammi
per sapere dove sta il logo, poi lì azzera l'alfa dei pixel molto saturi (il rosso
e l'arancio del logo). Pelle, maniche e muro neutro non vengono toccati.

Uso:
    python scripts/fix-matte.py SORGENTE.mp4 MASCHERA.webm OUT.webm --box 320,570,512,790
"""
import argparse
import subprocess

import numpy as np


def frames(cmd, shape):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n = int(np.prod(shape))
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape(shape)
    p.wait()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="video originale (per la parete)")
    ap.add_argument("matte", help="webm con alfa da pulire")
    ap.add_argument("output")
    ap.add_argument("--box", required=True, help="x0,y0,x1,y1 in pixel della zona da pulire")
    ap.add_argument("--sat-lo", type=float, default=0.62, help="saturazione sotto cui è persona")
    ap.add_argument("--sat-hi", type=float, default=0.72, help="saturazione sopra cui è logo")
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--fps", default="60")
    a = ap.parse_args()

    w, h = map(int, a.size.split("x"))
    x0, y0, x1, y1 = map(int, a.box.split(","))
    rgb_cmd = ["ffmpeg", "-v", "error", "-i", a.source, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    matte_cmd = ["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", a.matte,
                 "-f", "rawvideo", "-pix_fmt", "rgba", "-"]

    # 1) parete pulita della zona: mediana nel tempo
    crops = [f[y0:y1, x0:x1].astype(np.int16) for f in frames(rgb_cmd, (h, w, 3))]
    plate = np.median(np.stack(crops), axis=0).astype(np.float32)
    # agisci solo dove la parete è colorata (il logo): sul muro neutro una manica
    # bianca o la pelle coinciderebbero con lo sfondo e verrebbero bucate
    mx, mn = plate.max(axis=2), plate.min(axis=2)
    sat = (mx - mn) / np.maximum(mx, 1)
    logo = np.clip((sat - 0.25) / 0.15, 0, 1)
    print(f"Parete ricostruita da {len(crops)} fotogrammi, zona {x1-x0}x{y1-y0}")

    # sfumatura ai bordi della zona per non lasciare uno scalino
    fy = np.minimum(np.arange(y1 - y0), np.arange(y1 - y0)[::-1])[:, None]
    fx = np.minimum(np.arange(x1 - x0), np.arange(x1 - x0)[::-1])[None, :]
    edge = np.clip(np.minimum(fx, fy) / 12.0, 0, 1)

    # 2) nuova alfa: sul logo, via i pixel più saturi della pelle
    enc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", a.size,
         "-r", a.fps, "-i", "-", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0",
         "-crf", "18", "-row-mt", "1", "-auto-alt-ref", "0", "-metadata:s:v:0", "alpha_mode=1",
         a.output],
        stdin=subprocess.PIPE,
    )
    n = 0
    for rgb, rgba in zip(frames(rgb_cmd, (h, w, 3)), frames(matte_cmd, (h, w, 4))):
        out = rgba.copy()
        alpha = rgba[..., 3].astype(np.float32)
        c = rgb[y0:y1, x0:x1].astype(np.float32)
        # il logo è rosso/arancio molto saturo: la pelle è meno satura
        cmx, cmn = c.max(axis=2), c.min(axis=2)
        csat = (cmx - cmn) / np.maximum(cmx, 1)
        keep = 1 - np.clip((csat - a.sat_lo) / (a.sat_hi - a.sat_lo), 0, 1)
        keep = 1 - edge * logo * (1 - keep)
        alpha[y0:y1, x0:x1] *= keep
        out[..., 3] = alpha.astype(np.uint8)
        enc.stdin.write(out.tobytes())
        n += 1
    enc.stdin.close()
    enc.wait()
    print(f"Scritti {n} fotogrammi in {a.output}")


if __name__ == "__main__":
    main()
