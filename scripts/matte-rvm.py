#!/usr/bin/env python3
"""Scontorna la persona da un video con RobustVideoMatting (ONNX, CPU).

Esce un WebM VP9 con canale alfa, pronto per HyperFrames. Usa il colore di primo
piano stimato dal modello (niente alone dello sfondo originale sui bordi).

Uso:
    python scripts/matte-rvm.py IN.mp4 OUT.webm [--downsample 0.375]
Il modello (15 MB) viene scaricato una volta in ~/.cache/rvm/.
"""
import argparse
import json
import subprocess
import urllib.request
from pathlib import Path

import numpy as np
import onnxruntime as ort

MODEL_URL = ("https://github.com/PeterL1n/RobustVideoMatting/releases/download/"
             "v1.0.0/rvm_mobilenetv3_fp32.onnx")


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,r_frame_rate", "-of", "json", path],
        capture_output=True, check=True, text=True).stdout
    s = json.loads(out)["streams"][0]
    return s["width"], s["height"], s["r_frame_rate"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--downsample", type=float, default=0.375,
                    help="risoluzione interna del modello (0.25-0.5 per video HD)")
    ap.add_argument("--warmup", type=int, default=45,
                    help="fotogrammi usati per scaldare la memoria del modello")
    ap.add_argument("--model", default=str(Path.home() / ".cache/rvm/rvm_mobilenetv3_fp32.onnx"))
    a = ap.parse_args()

    model = Path(a.model)
    if not model.exists():
        model.parent.mkdir(parents=True, exist_ok=True)
        print("Scarico il modello RVM...")
        urllib.request.urlretrieve(MODEL_URL, model)
    sess = ort.InferenceSession(str(model), providers=["CPUExecutionProvider"])

    w, h, fps = probe(a.input)
    size = w * h * 3
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.input, "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    frames = [np.frombuffer(raw[i:i + size], np.uint8).reshape(h, w, 3)
              for i in range(0, len(raw) - size + 1, size)]
    print(f"{len(frames)} fotogrammi {w}x{h} @ {fps}")

    ds = np.array([a.downsample], np.float32)
    rec = [np.zeros((1, 1, 1, 1), np.float32)] * 4

    def step(img, rec):
        src = (img.astype(np.float32) / 255.0).transpose(2, 0, 1)[None]
        fgr, pha, *rec = sess.run(None, {"src": src, "r1i": rec[0], "r2i": rec[1],
                                         "r3i": rec[2], "r4i": rec[3], "downsample_ratio": ds})
        return fgr, pha, rec

    # memoria temporale: scalda il modello sui primi fotogrammi, poi riparte da capo
    for img in frames[:a.warmup]:
        _, _, rec = step(img, rec)

    enc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{w}x{h}",
         "-r", fps, "-i", "-", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0",
         "-crf", "18", "-row-mt", "1", "-auto-alt-ref", "0", "-metadata:s:v:0", "alpha_mode=1",
         a.output], stdin=subprocess.PIPE)
    for n, img in enumerate(frames, 1):
        fgr, pha, rec = step(img, rec)
        out = np.empty((h, w, 4), np.uint8)
        out[..., :3] = np.clip(fgr[0].transpose(1, 2, 0) * 255 + 0.5, 0, 255)
        out[..., 3] = np.clip(pha[0, 0] * 255 + 0.5, 0, 255)
        enc.stdin.write(out.tobytes())
        if n % 50 == 0:
            print(f"  {n}/{len(frames)}")
    enc.stdin.close()
    enc.wait()
    print(f"Scritto {a.output}")


if __name__ == "__main__":
    main()
