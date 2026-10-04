"""Per ogni pezzo del rough cut: c'e parlato appena fuori dai bordi del taglio?"""
import json
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(r"C:\Users\fabio\Desktop\claude-code\Claude_studio-video")
cache = {}


def audio(src):
    if src not in cache:
        pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(ROOT / src), "-ac", "1", "-ar", "16000",
                              "-f", "s16le", "-"], capture_output=True).stdout
        cache[src] = np.frombuffer(pcm, np.int16).astype(float) / 32768
    return cache[src]


def peak_db(x, a, b, w=0.025):
    seg = x[int(a * 16000):int(b * 16000)]
    n = int(w * 16000)
    if len(seg) < n:
        return -99.0
    rms = [np.sqrt((seg[i:i + n] ** 2).mean()) for i in range(0, len(seg) - n + 1, n)]
    return 20 * np.log10(max(rms) + 1e-9)


cuts = json.loads((ROOT / "renders" / "roughcut-v2.cuts.json").read_text(encoding="utf-8"))["cuts"]
for c in cuts:
    x = audio(c["source"])
    before = peak_db(x, max(c["src_start"] - 0.25, 0), c["src_start"])
    after = peak_db(x, c["src_end"], c["src_end"] + 0.25)
    flag = lambda v: "  <-- PARLATO" if v > -42 else ""
    print(f"seg{c['segment']} {c['src_start']:6.2f}-{c['src_end']:6.2f}  prima {before:6.1f} dB{flag(before)}"
          f" | dopo {after:6.1f} dB{flag(after)}")
