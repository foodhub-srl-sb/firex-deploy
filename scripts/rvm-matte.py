#!/usr/bin/env python3
"""Scontorna le persone in un video con RobustVideoMatting (RVM) e salva un webm VP9 con alfa.

RVM (https://github.com/PeterL1n/RobustVideoMatting, GPL-3.0) è un modello di video matting:
usa la memoria tra i fotogrammi, quindi bordi e capelli restano stabili, e separa bene la
persona dagli oggetti alle spalle. Qui si usa il modello ONNX, scaricato alla prima esecuzione
in ~/.cache/rvm (niente codice di RVM nel repository).

Uso:
    python scripts/rvm-matte.py input/ripresa.mp4 projects/x/assets/ai/me.webm
    python scripts/rvm-matte.py input/ripresa.mp4 out.webm --model resnet50 --despill
    python scripts/rvm-matte.py input/ripresa.mp4 out.webm --preview frames/rvm-check.jpg

Il video viene raddrizzato in automatico (rotazione dei telefoni). Usa da sola la scheda video se
c'è (NVIDIA con onnxruntime-gpu, Apple Silicon, DirectML su Windows), altrimenti la CPU.
Requisiti: ffmpeg, numpy, onnxruntime (vedi requirements.txt).

Per scaricare i modelli in anticipo (ad esempio durante l'installazione):
    python scripts/rvm-matte.py --prepare
"""
import argparse
import json
import os
import subprocess
import time
import urllib.request

import numpy as np

MODELS = {
    "mobilenetv3": "https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx",
    "resnet50": "https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_resnet50_fp32.onnx",
}


def model_path(name):
    d = os.path.expanduser("~/.cache/rvm")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, os.path.basename(MODELS[name]))
    if not os.path.exists(path):
        print(f"scarico il modello RVM {name}...", flush=True)
        urllib.request.urlretrieve(MODELS[name], path)
    return path


def probe(path):
    """Dimensioni già ruotate come le mostra il telefono, fps e numero di fotogrammi."""
    out = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height,r_frame_rate,nb_frames:stream_side_data=rotation", "-of", "json", path]))
    s = out["streams"][0]
    w, h = s["width"], s["height"]
    rot = 0
    for sd in s.get("side_data_list", []):
        rot = int(sd.get("rotation", 0) or 0)
    if abs(rot) % 180 == 90:
        w, h = h, w
    num, den = map(int, s["r_frame_rate"].split("/"))
    return w, h, num / den, int(s.get("nb_frames") or 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", nargs="?")
    ap.add_argument("out", nargs="?", help="webm VP9 con canale alfa")
    ap.add_argument("--prepare", action="store_true", help="scarica i modelli RVM ed esce")
    ap.add_argument("--model", choices=list(MODELS), default="mobilenetv3",
                    help="mobilenetv3 (veloce) o resnet50 (più preciso, più lento)")
    ap.add_argument("--downsample", type=float, default=None,
                    help="scala interna di RVM: 0.25 per Full HD, 0.125 per 4K (default automatico)")
    ap.add_argument("--despill", action="store_true", help="toglie la dominante verde di luci o green screen")
    ap.add_argument("--crf", type=int, default=28)
    ap.add_argument("--preview", help="salva un'anteprima JPG di 3 fotogrammi su sfondo verde")
    a = ap.parse_args()
    if a.prepare:
        for name in MODELS:
            print(f"{name}: {model_path(name)}")
        return
    if not a.input or not a.out:
        ap.error("servono il video di ingresso e il file di uscita")

    import onnxruntime as ort

    w, h, fps, n = probe(a.input)
    ds = a.downsample or (0.125 if max(w, h) >= 3000 else 0.25 if max(w, h) >= 1500 else 0.4)
    preferred = ["CUDAExecutionProvider", "CoreMLExecutionProvider", "DmlExecutionProvider"]
    providers = [p for p in preferred if p in ort.get_available_providers()] + ["CPUExecutionProvider"]
    sess = ort.InferenceSession(model_path(a.model), providers=providers)
    print(f"RVM {a.model} su {sess.get_providers()[0].replace('ExecutionProvider', '')}", flush=True)
    rec = [np.zeros([1, 1, 1, 1], np.float32)] * 4
    dsr = np.array([ds], np.float32)

    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.input, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{w}x{h}",
                            "-r", f"{fps}", "-i", "-", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0",
                            "-crf", str(a.crf), "-row-mt", "1", "-deadline", "good", "-cpu-used", "4",
                            "-auto-alt-ref", "0", a.out], stdin=subprocess.PIPE)
    size, i, t0 = w * h * 3, 0, time.time()
    picks = {int(n * f) for f in (0.2, 0.5, 0.8)} if n else {0}
    previews = []
    while True:
        buf = dec.stdout.read(size)
        if len(buf) < size:
            break
        rgb = np.frombuffer(buf, np.uint8).reshape(h, w, 3)
        src = (rgb.astype(np.float32) / 255).transpose(2, 0, 1)[None]
        fgr, pha, *rec = sess.run(None, {"src": src, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3],
                                         "downsample_ratio": dsr})
        alpha = pha[0, 0]
        # sui bordi semitrasparenti usa il colore "ripulito" stimato da RVM, all'interno quello originale
        fg = fgr[0].transpose(1, 2, 0)
        col = rgb.astype(np.float32) / 255
        edge = (alpha < 0.98)[..., None]
        col = np.where(edge, fg, col)
        if a.despill:
            r, g, b = col[..., 0], col[..., 1], col[..., 2]
            col[..., 1] = np.minimum(g, np.maximum(r, b))
        out = np.dstack([np.clip(col, 0, 1), alpha[..., None]])
        frame = (out * 255 + 0.5).astype(np.uint8)
        enc.stdin.write(frame.tobytes())
        if i in picks and a.preview:
            previews.append(frame)
        i += 1
        if i % 60 == 0:
            print(f"  {i}/{n or '?'} fotogrammi · {(time.time() - t0) / i:.2f} s/fotogramma", flush=True)
    enc.stdin.close()
    enc.wait()
    dec.wait()
    print(f"{a.out}: {i} fotogrammi {w}x{h} in {time.time() - t0:.0f} s (RVM {a.model}, downsample {ds})")

    if a.preview and previews:
        from PIL import Image
        tiles = []
        for f in previews:
            bg = Image.new("RGBA", (w, h), (30, 140, 90, 255))
            bg.alpha_composite(Image.fromarray(f, "RGBA"))
            tiles.append(bg.convert("RGB").resize((w // 3, h // 3)))
        sheet = Image.new("RGB", (sum(t.width for t in tiles) + 10 * (len(tiles) - 1), tiles[0].height))
        x = 0
        for t in tiles:
            sheet.paste(t, (x, 0))
            x += t.width + 10
        sheet.save(a.preview)
        print(f"anteprima: {a.preview}")


if __name__ == "__main__":
    main()
