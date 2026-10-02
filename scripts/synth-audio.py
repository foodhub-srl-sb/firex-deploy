#!/usr/bin/env python3
"""Genera musica ed effetti sonori originali (sintesi pura, nessun campione esterno).

Uso:
    python scripts/synth-audio.py                 # scrive sfx/*.wav e music/foodhub-beat.wav
    python scripts/synth-audio.py --bpm 120 --seconds 50 --music-out music/tracciabilita-beat.wav

Tutto è generato da oscillatori e rumore: nessun problema di diritti d'uso.
"""
import argparse
import os

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(7)


def t_axis(sec):
    return np.arange(int(sec * SR)) / SR


def env(n, a=0.005, d=0.2, curve=4.0):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-curve * np.maximum(0, t - a) / max(d, 1e-4))
    return e


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def norm(x, peak=0.9):
    m = np.max(np.abs(x)) or 1
    return x / m * peak


def save(path, x):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    wavfile.write(path, SR, (np.clip(x, -1, 1) * 32767).astype(np.int16))
    print("scritto", os.path.relpath(path, ROOT))


# ---------- effetti ----------

def whoosh(sec=0.7, lo=300, hi=5000, rise=True, seed=0):
    n = int(sec * SR)
    noise = np.random.default_rng(seed).standard_normal(n)
    t = np.linspace(0, 1, n)
    centers = lo * (hi / lo) ** (t if rise else 1 - t)
    out = np.zeros(n)
    blk = 512
    for i in range(0, n, blk):
        c = centers[i]
        out[i:i + blk] = bp(noise[i:i + blk + 0], c * 0.6, min(c * 1.6, SR / 2 - 100), 1)[: len(out[i:i + blk])]
    shape = np.sin(np.pi * t) ** 1.5
    return norm(out * shape, 0.8)


def pop(f0=900, f1=300, sec=0.12):
    t = t_axis(sec)
    f = f1 + (f0 - f1) * np.exp(-t * 40)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * env(len(t), 0.001, 0.05, 1)
    click = hp(rng.standard_normal(len(t)), 3000) * env(len(t), 0.0005, 0.004, 1) * 0.3
    return norm(x + click, 0.8)


def slap(sec=0.25):
    t = t_axis(sec)
    body = np.sin(2 * np.pi * 140 * t * np.exp(-t * 6)) * env(len(t), 0.001, 0.08, 1)
    snap = bp(rng.standard_normal(len(t)), 1200, 6000) * env(len(t), 0.0005, 0.03, 1)
    return norm(body * 0.7 + snap, 0.85)


def sparkle(sec=0.6):
    t = t_axis(sec)
    x = np.zeros_like(t)
    for k, f in enumerate([1568, 2093, 2637, 3136]):
        s = int(k * 0.06 * SR)
        tt = t[: len(t) - s]
        x[s:] += np.sin(2 * np.pi * f * tt) * env(len(tt), 0.002, 0.18, 1) * 0.5
    return norm(x, 0.6)


def riser(sec=1.5):
    n = int(sec * SR)
    t = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    out = np.zeros(n)
    blk = 512
    for i in range(0, n, blk):
        c = 400 * (8000 / 400) ** t[i]
        seg = bp(noise[i:i + blk], c * 0.7, min(c * 1.4, SR / 2 - 100), 1)
        out[i:i + len(seg)] = seg
    return norm(out * t ** 2, 0.7)


# ---------- musica ----------

def kick(sec=0.35):
    t = t_axis(sec)
    f = 45 + 110 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.001, 0.12, 1)


def clap(sec=0.25):
    t = t_axis(sec)
    n = bp(rng.standard_normal(len(t)), 900, 5000)
    e = env(len(t), 0.001, 0.06, 1)
    for d in (0.01, 0.02):
        e += np.roll(env(len(t), 0.001, 0.01, 1), int(d * SR)) * 0.6
    return n * e * 0.6


def hat(sec=0.06, open_=False):
    t = t_axis(0.25 if open_ else sec)
    return hp(rng.standard_normal(len(t)), 7000) * env(len(t), 0.001, 0.08 if open_ else 0.015, 1) * 0.35


def note_hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def pluck(m, sec=0.35, bright=4000):
    t = t_axis(sec)
    f = note_hz(m)
    x = sum(np.sign(np.sin(2 * np.pi * f * t + p)) * w for p, w in [(0, 0.5), (0.3, 0.25)])
    x = x + np.sin(2 * np.pi * f * 2 * t) * 0.2
    return lp(x, bright) * env(len(t), 0.003, 0.12, 1) * 0.18


def bass(m, sec):
    t = t_axis(sec)
    f = note_hz(m)
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    e = np.minimum(1, t / 0.01) * np.minimum(1, (sec - t) / 0.03)
    return lp(x, 600) * e * 0.35


def pad(chord, sec):
    t = t_axis(sec)
    x = np.zeros_like(t)
    for m in chord:
        for det in (-0.08, 0.08):
            f = note_hz(m + det)
            x += 2 * (t * f % 1) - 1
    x = lp(x, 1800) / (len(chord) * 2)
    e = np.minimum(1, t / 0.3) * np.minimum(1, (sec - t) / 0.3)
    return x * e * 0.12


def place(buf, x, at):
    i = int(at * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(x))
    buf[i:j] += x[: j - i]


def music(bpm=120, seconds=44):
    beat = 60 / bpm
    total = int(seconds * SR)
    drums = np.zeros(total)
    keys = np.zeros(total)
    low = np.zeros(total)
    pads = np.zeros(total)
    # progressione in La maggiore luminosa: A - F#m - D - E (un accordo per battuta)
    prog = [(57, [69, 73, 76]), (54, [66, 69, 73]), (50, [62, 66, 69]), (52, [64, 68, 71])]
    arp = [0, 1, 2, 1, 2, 0, 1, 2]
    bars = int(seconds / (beat * 4)) + 1
    end_bar = int((seconds - 4) / (beat * 4))  # negli ultimi 4 secondi solo l'accordo finale
    for b in range(bars):
        t0 = b * beat * 4
        if t0 >= seconds:
            break
        root, chord = prog[b % 4]
        if b >= end_bar:
            place(pads, pad([57] + [69, 73, 76, 81], seconds - t0), t0)
            place(low, bass(45, min(3.5, seconds - t0)), t0)
            place(drums, kick() * 1.2, t0)
            place(drums, hat(open_=True), t0)
            break
        intro = b == 0
        place(pads, pad(chord, beat * 4), t0)
        for s in range(8):
            ts = t0 + s * beat / 2
            place(keys, pluck(chord[arp[s]] + (12 if s % 4 == 3 else 0), bright=2500 if intro else 5000), ts)
        if not intro:
            for k in range(4):
                tk = t0 + k * beat
                place(drums, kick(), tk)
                place(drums, hat(), tk + beat / 2)
                if k in (1, 3):
                    place(drums, clap(), tk)
            for k in range(4):
                place(low, bass(root - 12 if k % 2 == 0 else root, beat * 0.9), t0 + k * beat + (beat / 2 if k % 2 else 0))
    mix = drums * 0.9 + keys + low + pads
    mix = np.tanh(mix * 1.4) / np.tanh(1.4)
    fade = np.ones(total)
    fn = int(1.0 * SR)
    fade[-fn:] = np.linspace(1, 0, fn)
    return norm(mix * fade, 0.8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bpm", type=float, default=120)
    ap.add_argument("--seconds", type=float, default=44)
    ap.add_argument("--music-out", default=os.path.join("music", "foodhub-beat.wav"))
    a = ap.parse_args()
    sfx = os.path.join(ROOT, "sfx")
    save(os.path.join(sfx, "whoosh-up.wav"), whoosh(0.7, 300, 6000, True, 1))
    save(os.path.join(sfx, "whoosh-down.wav"), whoosh(0.6, 5000, 250, False, 2))
    save(os.path.join(sfx, "whoosh-long.wav"), whoosh(1.0, 200, 4000, True, 3))
    save(os.path.join(sfx, "pop-high.wav"), pop(1200, 500))
    save(os.path.join(sfx, "pop-mid.wav"), pop(800, 300))
    save(os.path.join(sfx, "pop-low.wav"), pop(520, 180, 0.14))
    save(os.path.join(sfx, "slap.wav"), slap())
    save(os.path.join(sfx, "sparkle.wav"), sparkle())
    save(os.path.join(sfx, "riser.wav"), riser())
    save(os.path.join(ROOT, a.music_out), music(a.bpm, a.seconds))


if __name__ == "__main__":
    main()
