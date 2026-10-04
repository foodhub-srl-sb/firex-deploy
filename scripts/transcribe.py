#!/usr/bin/env python3
"""Word-level transcription with faster-whisper.

Usage:
    python scripts/transcribe.py input/take.mp4 [--model small] [--language it]
        [--names "Food Hub,ChallengEat,Claude"] [-o take.words.json]

Writes <stem>.words.json (next to the input unless -o is given) and <stem>.srt:

    {"source", "language", "duration",
     "words":    [{"word", "start", "end", "probability"}],
     "segments": [{"start", "end", "text"}]}

--names is passed to Whisper as initial_prompt (hotwords) so proper nouns
are spelled correctly.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Word-level transcription with faster-whisper.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("input", type=Path, help="audio or video file")
    p.add_argument("--model", default="small",
                   help="Whisper model size or path (tiny, base, small, medium, large-v3, ...)")
    p.add_argument("--language", default=None,
                   help="language code, e.g. it or en (default: auto-detect)")
    p.add_argument("--names", default="",
                   help="comma-separated names/brands to spell correctly")
    p.add_argument("-o", "--output", type=Path, default=None,
                   help="output JSON path (default: <input dir>/<stem>.words.json)")
    p.add_argument("--device", default="auto", help="auto, cpu or cuda")
    p.add_argument("--show", type=int, default=40, help="words to print to stdout")
    return p.parse_args(argv)


def build_prompt(names: str) -> str | None:
    items = [n.strip() for n in names.split(",") if n.strip()]
    return ", ".join(items) + "." if items else None


def srt_time(t: float) -> str:
    ms = int(round(max(t, 0.0) * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(segments: list[dict], path: Path) -> None:
    lines = []
    for i, seg in enumerate(segments, 1):
        lines += [str(i), f"{srt_time(seg['start'])} --> {srt_time(seg['end'])}", seg["text"], ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def decode_audio(path: Path):
    """16 kHz mono float32 via ffmpeg (avoids PyAV API changes breaking faster-whisper)."""
    import numpy as np

    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-i", str(path), "-vn",
           "-ac", "1", "-ar", "16000", "-f", "s16le", "-"]
    pcm = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0


def load_model(name: str, device: str):
    from faster_whisper import WhisperModel

    if device == "auto":
        try:
            import ctranslate2
            device = "cuda" if ctranslate2.get_cuda_device_count() > 0 else "cpu"
        except Exception:
            device = "cpu"
    compute_type = "int8" if device == "cpu" else "auto"
    return WhisperModel(name, device=device, compute_type=compute_type), device, compute_type


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    src: Path = args.input
    if not src.is_file():
        print(f"Input not found: {src}", file=sys.stderr)
        return 1

    try:
        model, device, ctype = load_model(args.model, args.device)
    except ImportError:
        print("faster-whisper is not installed: python3 -m pip install faster-whisper",
              file=sys.stderr)
        return 1
    except Exception as exc:  # usually a failed model download
        print(f"Could not load model '{args.model}': {exc}\n"
              "The first run downloads it from Hugging Face; check your connection.",
              file=sys.stderr)
        return 1

    out_json = args.output or src.with_name(f"{src.stem}.words.json")
    out_srt = out_json.with_name(out_json.name.removesuffix(".words.json").removesuffix(".json") + ".srt")

    print(f"Transcribing {src} (model={args.model}, device={device}, compute={ctype})...",
          file=sys.stderr)
    try:
        audio = decode_audio(src)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"ffmpeg could not decode {src}: {exc}", file=sys.stderr)
        return 1
    seg_iter, info = model.transcribe(
        audio,
        language=args.language,
        initial_prompt=build_prompt(args.names),
        word_timestamps=True,
        vad_filter=True,
    )

    words: list[dict] = []
    segments: list[dict] = []
    for seg in seg_iter:
        segments.append({"start": round(seg.start, 3), "end": round(seg.end, 3),
                         "text": seg.text.strip()})
        for w in seg.words or []:
            words.append({"word": w.word.strip(), "start": round(w.start, 3),
                          "end": round(w.end, 3), "probability": round(w.probability, 3)})

    data = {
        "source": str(src),
        "language": info.language,
        "duration": round(info.duration, 3),
        "words": words,
        "segments": segments,
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    write_srt(segments, out_srt)

    for w in words[: args.show]:
        print(f"{w['start']:7.2f}s → {w['end']:6.2f}s  {w['word']}")
    if len(words) > args.show:
        print(f"... ({len(words) - args.show} more)")
    print(f"\n{len(words)} words, {len(segments)} segments, language={info.language}, "
          f"duration={info.duration:.2f}s")
    print(f"Wrote {out_json}\nWrote {out_srt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
