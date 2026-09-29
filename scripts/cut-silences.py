#!/usr/bin/env python3
"""Rough cut: remove silences between words using a <stem>.words.json.

Usage:
    python scripts/cut-silences.py input/take.words.json [--threshold 0.3]
        [--padding 0.08] [--keep-before "Claude,però"] [--beat 0.35]
        [-o cuts.json] [--render out.mp4] [--input input/take.mp4]

Gaps between consecutive words longer than --threshold are removed, keeping
--padding seconds around each word. Cuts never fall inside a word. Words listed
in --keep-before get a longer lead-in (--beat) for a dramatic pause.

Writes cuts.json: {"source", "threshold", "padding", "old_duration",
"new_duration", "keep": [{"start", "end"}], "removed": [...]}.
With --render, ffmpeg (trim/atrim + concat) produces the rough cut.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Remove silences between words.",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("words_json", type=Path, help="<stem>.words.json from transcribe.py")
    p.add_argument("--threshold", type=float, default=0.3,
                   help="cut gaps between words longer than this (s)")
    p.add_argument("--padding", type=float, default=0.08,
                   help="silence kept before/after each kept run (s)")
    p.add_argument("--keep-before", default="",
                   help="comma-separated words that get a longer beat before them")
    p.add_argument("--beat", type=float, default=0.35,
                   help="lead-in kept before --keep-before words (s)")
    p.add_argument("-o", "--output", type=Path, default=None,
                   help="cuts JSON path (default: cuts.json next to words JSON)")
    p.add_argument("--render", type=Path, default=None, metavar="OUT.mp4",
                   help="render the rough cut with ffmpeg")
    p.add_argument("--input", type=Path, default=None,
                   help="media to cut (default: 'source' from words JSON)")
    return p.parse_args(argv)


def norm(word: str) -> str:
    return re.sub(r"[^\w]+", "", word.lower())


def compute_keep(words: list[dict], duration: float, threshold: float, padding: float,
                 keep_before: set[str], beat: float) -> list[tuple[float, float]]:
    """Return merged keep ranges that fully contain every word."""
    words = sorted((w for w in words if w["end"] > w["start"]), key=lambda w: w["start"])
    if not words:
        return []
    ranges: list[list[float]] = []
    prev_end = None
    for w in words:
        lead = beat if norm(w["word"]) in keep_before else padding
        start, end = w["start"], w["end"]
        if prev_end is not None and start - prev_end <= threshold:
            ranges[-1][1] = max(ranges[-1][1], end)       # short gap: keep it whole
        else:
            if ranges:
                ranges[-1][1] += padding                  # tail after previous run
            ranges.append([start - lead, end])
        prev_end = max(prev_end or 0.0, end)
    ranges[-1][1] += padding

    # Clamp and merge overlaps created by padding.
    merged: list[list[float]] = []
    for s, e in ranges:
        s, e = max(0.0, s), min(duration, e) if duration > 0 else e
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [(round(s, 3), round(e, 3)) for s, e in merged]


def removed_ranges(keep: list[tuple[float, float]], duration: float) -> list[tuple[float, float]]:
    out, t = [], 0.0
    for s, e in keep:
        if s > t:
            out.append((round(t, 3), s))
        t = e
    if duration > t:
        out.append((round(t, 3), round(duration, 3)))
    return out


def probe(path: Path) -> tuple[float, bool, bool]:
    """Return (duration, has_video, has_audio) via ffprobe."""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration:stream=codec_type", "-of", "json", str(path)],
                       capture_output=True, text=True, check=True)
    info = json.loads(r.stdout)
    kinds = {s.get("codec_type") for s in info.get("streams", [])}
    return float(info["format"].get("duration", 0) or 0), "video" in kinds, "audio" in kinds


def ffmpeg_major() -> int:
    r = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
    m = re.search(r"ffmpeg version n?(\d+)", r.stdout)
    return int(m.group(1)) if m else 0


def render(src: Path, keep: list[tuple[float, float]], out: Path) -> None:
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("ffmpeg/ffprobe not found (run scripts/check.sh)")
    _, has_v, has_a = probe(src)
    parts, labels = [], []
    for i, (s, e) in enumerate(keep):
        lab = ""
        if has_v:
            parts.append(f"[0:v]trim=start={s}:end={e},setpts=PTS-STARTPTS[v{i}]")
            lab += f"[v{i}]"
        if has_a:
            parts.append(f"[0:a]atrim=start={s}:end={e},asetpts=PTS-STARTPTS[a{i}]")
            lab += f"[a{i}]"
        labels.append(lab)
    outs = ("[outv]" if has_v else "") + ("[outa]" if has_a else "")
    parts.append(f"{''.join(labels)}concat=n={len(keep)}:v={int(has_v)}:a={int(has_a)}{outs}")
    graph = ";\n".join(parts)

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write(graph)
        script = f.name
    # ffmpeg 7+ prefers -/filter_complex <file>; older builds use -filter_complex_script.
    fc = ["-/filter_complex", script] if ffmpeg_major() >= 7 else ["-filter_complex_script", script]
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src), *fc]
    if has_v:
        cmd += ["-map", "[outv]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-pix_fmt", "yuv420p"]
    if has_a:
        cmd += ["-map", "[outa]", "-c:a", "aac", "-b:a", "192k"]
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd += ["-movflags", "+faststart", str(out)]
    try:
        subprocess.run(cmd, check=True)
    finally:
        Path(script).unlink(missing_ok=True)


def resolve_source(args: argparse.Namespace, data: dict) -> Path | None:
    if args.input:
        return args.input
    src = data.get("source")
    if not src:
        return None
    for cand in (Path(src), args.words_json.parent / Path(src).name):
        if cand.is_file():
            return cand
    return Path(src)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    data = json.loads(args.words_json.read_text(encoding="utf-8"))
    words = data.get("words", [])
    if not words:
        print("No words in JSON: nothing to keep.", file=sys.stderr)
        return 1

    src = resolve_source(args, data)
    duration = float(data.get("duration") or 0)
    if duration <= 0 and src and src.is_file() and shutil.which("ffprobe"):
        duration = probe(src)[0]
    if duration <= 0:
        duration = max(w["end"] for w in words)

    kb = {norm(w) for w in args.keep_before.split(",") if norm(w)}
    keep = compute_keep(words, duration, args.threshold, args.padding, kb, args.beat)
    new_dur = round(sum(e - s for s, e in keep), 3)

    out = args.output or args.words_json.with_name("cuts.json")
    result = {
        "source": str(src) if src else None,
        "threshold": args.threshold,
        "padding": args.padding,
        "keep_before": sorted(kb),
        "old_duration": round(duration, 3),
        "new_duration": new_dur,
        "keep": [{"start": s, "end": e} for s, e in keep],
        "removed": [{"start": s, "end": e} for s, e in removed_ranges(keep, duration)],
    }
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    saved = duration - new_dur
    pct = 100 * saved / duration if duration else 0
    print(f"Old length: {duration:.2f}s")
    print(f"New length: {new_dur:.2f}s  (-{saved:.2f}s, -{pct:.0f}%, {len(keep)} segment(s))")
    print(f"Wrote {out}")

    if args.render:
        if not src or not src.is_file():
            print(f"Source media not found: {src}. Pass --input.", file=sys.stderr)
            return 1
        render(src, keep, args.render)
        if shutil.which("ffprobe"):
            print(f"Rendered {args.render} ({probe(args.render)[0]:.2f}s)")
        else:
            print(f"Rendered {args.render}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
