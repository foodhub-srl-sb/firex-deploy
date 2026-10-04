"""Asset per mela-gluten-free: petali del logo del festival + audio macchina da scrivere."""
import json
import wave
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(r"C:\Users\fabio\Desktop\claude-code\Claude_studio-video")
P = ROOT / "projects" / "mela-gluten-free"

# ---------------- 1. Logo del festival diviso nei 5 petali ----------------
src = Image.open(ROOT / "assets" / "Festival logo.png").convert("RGBA")
a = np.asarray(src).astype(float)
rgb, alpha = a[..., :3], a[..., 3] / 255.0
petals = {  # nome: colore campionato dal logo
    "p1-chiaro": (209, 229, 196),
    "p2-verde": (168, 208, 141),
    "p3-salvia": (106, 141, 99),
    "p4-scuro": (81, 112, 85),
    "p5-rosa": (229, 25, 90),
}
cols = np.array(list(petals.values()), float)
# Lo sfondo e gli spazi tra i petali sono trasparenti: si tiene l'alfa originale e
# ogni pixel visibile va al petalo "pieno" (alfa 255) piu vicino.
from scipy.ndimage import distance_transform_edt
nearest = np.linalg.norm(rgb[..., None, :] - cols, axis=-1).argmin(-1)
core = alpha > 0.99
dist = np.stack([distance_transform_edt(~(core & (nearest == k))) for k in range(len(cols))], -1)
owner = dist.argmin(-1)
score = np.zeros(alpha.shape + (len(cols),))
for k in range(len(cols)):
    score[..., k] = np.where(owner == k, alpha, 0)
out_dir = P / "assets" / "img" / "festival"
out_dir.mkdir(parents=True, exist_ok=True)
ys, xs = np.nonzero(alpha > 0.02)
box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
for k, (name, c) in enumerate(petals.items()):
    al = score[..., k]
    layer = np.zeros(al.shape + (4,), np.uint8)
    layer[..., :3] = c
    layer[..., 3] = (al * 255).round().astype(np.uint8)
    Image.fromarray(layer).crop(box).save(out_dir / f"{name}.png", optimize=True)
print("logo: box", box, "->", out_dir)

# ---------------- 2. Macchina da scrivere ----------------
SR = 48000
CARDS = json.loads((Path(__file__).with_name("type_cards.json")).read_text(encoding="utf-8"))
rng = np.random.default_rng(7)


def key(strength=1.0):
    n = int(0.06 * SR)
    tt = np.arange(n) / SR
    click = rng.normal(0, 1, n) * np.exp(-tt * 900)          # colpo metallico secco
    click = np.diff(click, prepend=0)                          # piu brillante
    thock = np.sin(2 * np.pi * rng.uniform(95, 140) * tt) * np.exp(-tt * 70)
    s = 0.55 * click + 0.45 * thock
    return strength * s / np.abs(s).max()


info = {}
for c in CARDS:
    text, t0, t1 = c["text"], c["type_from"], c["type_to"]
    n = len(text)
    step = (t1 - t0) / max(n - 1, 1)
    dur = (t1 - t0) + 0.3
    buf = np.zeros(int(dur * SR) + SR // 10)
    times = []
    for i, ch in enumerate(text):
        ti = i * step
        times.append(round(t0 + ti, 3))
        if ch == " ":
            continue
        k = key(rng.uniform(0.7, 1.0))
        j = int(ti * SR)
        buf[j:j + len(k)] += k
    buf = 0.6 * buf / np.abs(buf).max()
    pcm = (buf * 32767).astype("<i2")
    path = P / "audio" / f"type-{c['id']}.wav"
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    info[c["id"]] = {"text": text, "start": t0, "step": round(step, 4), "times": times,
                     "audio_duration": round(len(buf) / SR, 3)}
    print(f"type-{c['id']}: {n} caratteri, {step*1000:.0f} ms/carattere")
(Path(__file__).with_name("type_schedule.json")).write_text(json.dumps(info, ensure_ascii=False, indent=1),
                                                            encoding="utf-8")
