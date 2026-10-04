"""Monta il rough cut del video 'mela gluten-free' da hook + take 1 + take 2."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\fabio\Desktop\claude-code\Claude_studio-video")
spec = importlib.util.spec_from_file_location("cs", ROOT / "scripts" / "cut-silences.py")
cs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cs)

HOOK, T1, T2 = "video_20250702_100004", "video_20250702_100608", "video_20250702_100931"
# (sorgente, da, a, taglia_silenzi, nota)
SEGMENTS = [
    (HOOK, 7.10, 13.55, False, "hook: lancio della mela + 'E se il peccato originale...'"),
    (T1, 1.00, 22.40, True, "'Nel gluten-free...' -> '...reequilibrata'"),
    (T1, 23.30, 27.88, True, "'E qui che comincia... industria alimentare'"),
    (T2, 48.30, 67.30, True, "'Ad esempio, in uno studio...' -> '...2,10 N'"),
    (T1, 47.30, 60.15, True, "'Tradotto. Che cosa vuol dire?...' -> '...intera formulazione'"),
    (T2, 82.30, 87.50, True, "'Scopri questi nuovi approcci... agroalimentare'"),
    (T1, 71.00, 75.65, True, "'Il festival sara online e gratuito dal 9 al 12 novembre 2026'"),
]
THRESHOLD, LEAD, TAIL, BEAT = 0.30, 0.20, 0.10, 0.30
OUT_NAME = "roughcut-v3"
# Le riprese sono HDR (HLG, BT.2020, 10 bit): conversione a SDR Rec.709 prima di tutto
TONEMAP = ("zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:rin=tv:t=linear:npl=203,format=gbrpf32le,"
           "zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
KEEP_BEFORE = {"che", "più"}

sources = sorted({s[0] for s in SEGMENTS})
idx = {s: i for i, s in enumerate(sources)}
words = {s: json.loads((ROOT / "input" / f"{s}.words.json").read_text(encoding="utf-8"))["words"]
         for s in sources}

ranges = []  # (source, start, end, segment#)
for n, (src, a, b, cut, _) in enumerate(SEGMENTS, 1):
    if not cut:
        ranges.append((src, a, b, n))
        continue
    ws = [w for w in words[src] if w["start"] >= a and w["end"] <= b]
    # Ritmo serrato: si tagliano le pause sopra THRESHOLD. Whisper colloca l'inizio delle
    # parole in ritardo, quindi l'attacco (LEAD) e piu lungo della coda (TAIL).
    keep = []
    for i, w in enumerate(ws):
        lead = BEAT if cs.norm(w["word"]) in KEEP_BEFORE else LEAD
        if keep and w["start"] - ws[i - 1]["end"] <= THRESHOLD:
            keep[-1][1] = w["end"] + TAIL
        else:
            keep.append([w["start"] - lead, w["end"] + TAIL])
    merged = []
    for s_, e_ in keep:
        if merged and s_ <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e_)
        else:
            merged.append([s_, e_])
    keep = merged
    keep[0][0], keep[-1][1] = a, b  # i bordi del segmento li ho scelti a mano sull'audio
    for s, e in keep:
        ranges.append((src, max(s, a), min(e, b), n))

parts, labels = [], []
for i, (src, s, e, _) in enumerate(ranges):
    k = idx[src]
    d = e - s
    parts.append(f"[{k}:v]trim=start={s}:end={e},setpts=PTS-STARTPTS,{TONEMAP},"
                 f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[v{i}]")
    parts.append(f"[{k}:a]atrim=start={s}:end={e},asetpts=PTS-STARTPTS,aresample=48000,"
                 f"afade=t=in:d=0.01,afade=t=out:st={max(d - 0.01, 0):.3f}:d=0.01[a{i}]")
    labels.append(f"[v{i}][a{i}]")
parts.append(f"{''.join(labels)}concat=n={len(ranges)}:v=1:a=1[cv][ca]")
parts.append("[ca]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[outa]")
graph = ";\n".join(parts)

out = ROOT / "renders" / f"{OUT_NAME}.mp4"
out.parent.mkdir(exist_ok=True)
gfile = Path(__file__).with_name("roughcut_graph.txt")
gfile.write_text(graph, encoding="utf-8")
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
for s in sources:
    cmd += ["-i", str(ROOT / "input" / f"{s}.mp4")]
cmd += ["-/filter_complex", str(gfile), "-map", "[cv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)]
subprocess.run(cmd, check=True)

# Mappa: dove finisce ogni pezzo nel rough cut (serve per sincronizzare gli effetti)
t, edl = 0.0, []
for src, s, e, n in ranges:
    edl.append({"segment": n, "source": f"input/{src}.mp4", "src_start": s, "src_end": e,
                "out_start": round(t, 3), "out_end": round(t + e - s, 3)})
    t += e - s
meta = {"output": f"renders/{OUT_NAME}.mp4", "duration": round(t, 3),
        "segments": [{"n": n, "source": f"input/{s}.mp4", "from": a, "to": b, "note": note}
                     for n, (s, a, b, _, note) in enumerate(SEGMENTS, 1)],
        "cuts": edl}
(ROOT / "renders" / f"{OUT_NAME}.cuts.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                                                     encoding="utf-8")
print(f"{len(ranges)} pezzi, durata {t:.2f}s -> {out}")
for n in range(1, len(SEGMENTS) + 1):
    c = [x for x in edl if x["segment"] == n]
    print(f"  segmento {n}: {c[0]['out_start']:6.2f} - {c[-1]['out_end']:6.2f}s ({len(c)} pezzi)")
