import subprocess
import sys

import numpy as np


def env(f, a, b, step=0.1):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", f,
                          "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(float) / 32768
    w = int(16000 * step)
    for i in range(0, len(x) - w + 1, w):
        db = 20 * np.log10(np.sqrt((x[i:i + w] ** 2).mean()) + 1e-9)
        print(f"{a + i / 16000:6.1f}s {db:6.1f} dB " + "#" * max(0, int((60 + db) / 2)))


f, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
step = float(sys.argv[4]) if len(sys.argv) > 4 else 0.1
env(f, a, b, step)
