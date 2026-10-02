#!/usr/bin/env python3
"""Genera immagini e video con OpenRouter partendo da un file di richiesta JSON.

Comandi:
    python scripts/media/openrouter.py models --type video --limit 15
    python scripts/media/openrouter.py check media/requests/esempio.json      # valida e stima, senza spendere
    python scripts/media/openrouter.py run media/requests/esempio.json --out media/out

Il comando `run` ha bisogno della variabile OPENROUTER_API_KEY (nella GitHub Action
arriva dal segreto del repository). `models` e `check` non la usano.

Formato della richiesta (vedi media/requests/README.md):
{
  "max_usd": 3,
  "jobs": [
    {"name": "mela", "type": "image", "model": "openai/gpt-image-2.5-sunburst",
     "prompt": "...", "aspect_ratio": "1:1", "quality": "high", "background": "transparent"},
    {"name": "frutteto", "type": "video", "model": "google/veo-3.1-fast",
     "prompt": "...", "duration": 6, "resolution": "1080p", "aspect_ratio": "9:16",
     "generate_audio": false,
     "frame_images": [{"ref": "@mela", "frame_type": "first_frame"}]}
  ]
}
Ogni altra chiave del job (seed, n, provider, input_references, ...) passa così com'è
all'API. Un riferimento "@nome" usa l'output di un job precedente della stessa richiesta,
"@nome:last" (o ":first") il fotogramma reale di un video precedente, per concatenare le
clip; un percorso locale viene inviato come data URL; un URL http(s) passa invariato. Il tipo
(immagine, audio, video) si ricava dall'estensione o da "kind".

Tipi di job: "image", "video" e "speech" (sintesi vocale, anche con clonazione della voce
da un audio di riferimento: input_references [{"ref": "voce.wav", "transcript": "..."}]).
"""
import argparse
import base64
import datetime
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.request

API = "https://openrouter.ai/api/v1"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESERVED = {"name", "type", "note", "est_seconds"}
EXT = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp", "image/svg+xml": ".svg"}
MEDIA_KIND = {"image": "image", "audio": "audio", "video": "video"}


class MediaError(Exception):
    pass


# ---------------------------------------------------------------- HTTP

def http(method, url, body=None, auth=True, timeout=600, raw=False):
    if not url.startswith("http"):
        url = API + url
    headers = {"Content-Type": "application/json", "X-Title": "Food Hub video studio"}
    if auth:
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise MediaError("OPENROUTER_API_KEY non impostata")
        headers["Authorization"] = "Bearer " + key
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                payload = r.read()
                return payload if raw else json.loads(payload or b"{}")
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:800]
            if e.code in (429, 500, 502, 503, 504) and attempt < 3:
                time.sleep(2 ** (attempt + 2))
                continue
            raise MediaError(f"HTTP {e.code} su {method} {url}: {msg}")
        except urllib.error.URLError as e:
            if attempt < 3:
                time.sleep(2 ** (attempt + 2))
                continue
            raise MediaError(f"rete non raggiungibile ({url}): {e}")


_catalog = {}


def catalog(kind):
    if kind not in _catalog:
        path = "/models?output_modalities=speech" if kind == "speech" else f"/{kind}s/models"
        data = http("GET", path, auth=False)["data"]
        _catalog[kind] = {m["id"]: m for m in data}
    return _catalog[kind]


# ---------------------------------------------------------------- riferimenti a file

def as_url(value, outputs, base_dir):
    """'@job' -> output di un job; percorso locale -> data URL; http(s) -> invariato."""
    if value.startswith(("http://", "https://", "data:")):
        return value
    if value.startswith("@"):
        name, _, frame = value[1:].partition(":")
        if name not in outputs:
            raise MediaError(f"riferimento {value}: nessun job precedente con questo nome")
        path = outputs[name]
        if frame:
            path = extract_frame(path, frame)
    else:
        path = value if os.path.isabs(value) else os.path.join(ROOT, value)
        if not os.path.exists(path):
            alt = os.path.join(base_dir, value)
            path = alt if os.path.exists(alt) else path
    if not os.path.exists(path):
        raise MediaError(f"file non trovato: {value}")
    mime = mimetypes.guess_type(path)[0] or "image/png"
    mime = {"audio/x-wav": "audio/wav", "audio/mpeg": "audio/mpeg"}.get(mime, mime)
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def extract_frame(video, which):
    """'@clip:last' o '@clip:first': estrae il fotogramma reale per concatenare le clip."""
    import subprocess
    if which not in ("first", "last"):
        raise MediaError(f"fotogramma '{which}' non valido: usa :first o :last")
    out = os.path.splitext(video)[0] + f".{which}.png"
    seek = ["-sseof", "-0.1"] if which == "last" else []
    cmd = ["ffmpeg", "-v", "error", "-y", *seek, "-i", video, "-update", "1", "-frames:v", "1", out]
    if subprocess.run(cmd).returncode != 0 or not os.path.exists(out):
        raise MediaError(f"impossibile estrarre il fotogramma {which} da {video}")
    return out


def media_kind(it, ref, outputs):
    """Tipo del riferimento: dichiarato con "kind", altrimenti dall'estensione del file."""
    if it.get("kind"):
        return it["kind"]
    path = outputs.get(ref[1:].partition(":")[0], "") if ref.startswith("@") else ref
    if ref.startswith("@") and ref.partition(":")[2]:
        return "image"  # @clip:last è un fotogramma
    mime = mimetypes.guess_type(path.split("?")[0])[0] or ""
    return mime.split("/")[0] if mime.split("/")[0] in MEDIA_KIND else "image"


def resolve_images(items, outputs, base_dir, keep_frame_type, speech=False):
    out = []
    for it in items:
        if isinstance(it, str):
            it = {"ref": it}
        ref = it.get("ref") or it.get("url") or (it.get("image_url") or {}).get("url")
        if not ref:
            raise MediaError(f"riferimento senza 'ref' o 'url': {it}")
        kind = media_kind(it, ref, outputs)
        url = as_url(ref, outputs, base_dir)
        if speech and kind == "audio":
            out.append({"type": "input_audio", "input_audio": {"data" if url.startswith("data:") else "url": url}})
            if it.get("transcript"):
                out.append({"type": "text", "text": it["transcript"]})
            continue
        entry = {"type": f"{kind}_url", f"{kind}_url": {"url": url}}
        if keep_frame_type:
            entry["frame_type"] = it.get("frame_type", "first_frame")
        out.append(entry)
    return out


def build_payload(job, outputs, base_dir, resolve=True):
    payload = {k: v for k, v in job.items() if k not in RESERVED}
    for key, keep in (("frame_images", True), ("input_references", False)):
        if key in payload:
            payload[key] = (resolve_images(payload[key], outputs, base_dir, keep, speech=job["type"] == "speech")
                            if resolve else payload[key])
    if job["type"] == "speech":
        payload["input"] = payload.pop("prompt")
        payload.setdefault("response_format", "mp3")
    return payload


# ---------------------------------------------------------------- validazione e stime

def validate(job):
    kind = job.get("type")
    if kind not in ("image", "video", "speech"):
        raise MediaError(f"job '{job.get('name')}': 'type' deve essere image, video o speech")
    for k in ("name", "model", "prompt"):
        if not job.get(k):
            raise MediaError(f"job '{job.get('name')}': manca '{k}'")
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", job["name"]):
        raise MediaError(f"job '{job['name']}': usa solo minuscole, numeri, punto, trattino")
    models = catalog(kind)
    m = models.get(job["model"])
    if not m:
        recent = sorted(models.values(), key=lambda x: -x.get("created", 0))[:8]
        raise MediaError(f"modello {kind} sconosciuto: {job['model']}. Recenti: " + ", ".join(x["id"] for x in recent))
    problems = []
    if kind == "speech":
        pass  # i parametri della voce dipendono dal provider: li controlla l'API
    elif kind == "video":
        for key, field in (("duration", "supported_durations"), ("resolution", "supported_resolutions"),
                           ("aspect_ratio", "supported_aspect_ratios")):
            allowed = m.get(field)
            if key in job and allowed and job[key] not in allowed:
                problems.append(f"{key}={job[key]!r} non supportato, valori ammessi: {allowed}")
        frames = m.get("supported_frame_images") or []
        for fr in job.get("frame_images", []):
            ft = fr.get("frame_type", "first_frame") if isinstance(fr, dict) else "first_frame"
            if ft not in frames:
                problems.append(f"frame_type {ft} non supportato (ammessi: {frames or 'nessuno'})")
    else:
        sp = m.get("supported_parameters", {})
        for key in ("aspect_ratio", "resolution", "quality", "background", "output_format"):
            if key in job:
                d = sp.get(key)
                if d is None:
                    problems.append(f"{key} non supportato da questo modello")
                elif d.get("type") == "enum" and job[key] not in d.get("values", []):
                    problems.append(f"{key}={job[key]!r} non ammesso, valori: {d.get('values')}")
        if "input_references" in job and "input_references" not in sp:
            problems.append("input_references non supportato da questo modello")
    if problems:
        raise MediaError(f"job '{job['name']}' ({job['model']}): " + "; ".join(problems))
    return m


def estimate_video(job, m):
    """Stima in USD dai pricing_skus pubblici. None se il listino non è in secondi."""
    skus = m.get("pricing_skus") or {}
    dur = job.get("duration") or job.get("est_seconds") or min(m.get("supported_durations") or [5])
    res = str(job.get("resolution", "")).lower()
    audio = job.get("generate_audio", m.get("generate_audio"))
    cands = []
    for k, v in skus.items():
        try:
            price = float(v)
        except (TypeError, ValueError):
            continue
        kl = k.lower()
        if "token" in kl or "image_input" in kl or "reference" in kl or "minimum" in kl or "continuation" in kl:
            continue
        if "second" not in kl:
            continue
        if res and re.search(r"(\d+p|\dk)", kl) and res not in kl:
            continue
        if audio is False and "with_audio" in kl and any("without_audio" in x for x in skus):
            continue
        if audio and "without_audio" in kl and any("with_audio" in x for x in skus):
            continue
        if "frame_images" not in job and kl.startswith("image_to_video"):
            continue
        if "frame_images" in job and kl.startswith("text_to_video"):
            continue
        cands.append(price / 100 if kl.startswith("cents") else price)
    if cands:
        return round(max(cands) * dur, 3)
    # listino a token video (es. Seedance): token ≈ larghezza × altezza × 24 fps × secondi / 1024
    tok = skus.get("video_tokens") or skus.get("video_tokens_without_audio")
    if tok:
        h = {"480p": 480, "720p": 720, "1080p": 1080, "4k": 2160}.get(res or "720p", 720)
        w = h * 16 / 9
        return round(float(tok) * w * h * 24 * dur / 1024, 3)
    return None


def plan(request, base_dir):
    lines, total, unknown = [], 0.0, False
    names = set()
    for job in request["jobs"]:
        m = validate(job)
        if job["name"] in names:
            raise MediaError(f"nome job duplicato: {job['name']}")
        names.add(job["name"])
        for key in ("frame_images", "input_references"):
            for it in job.get(key, []):
                ref = it if isinstance(it, str) else (it.get("ref") or "")
                if ref.startswith("@") and ref[1:].partition(":")[0] not in names - {job["name"]}:
                    raise MediaError(f"job '{job['name']}': {ref} deve riferirsi a un job precedente")
                if ref and not ref.startswith(("@", "http", "data:")) and not os.path.exists(os.path.join(ROOT, ref)):
                    raise MediaError(f"job '{job['name']}': file non trovato {ref}")
        if job["type"] == "video":
            est = estimate_video(job, m)
        elif job["type"] == "speech":
            price = float((m.get("pricing") or {}).get("prompt") or 0)
            est = round(price * len(job["prompt"]) * 2, 4) if price else None  # margine x2 sul listino a carattere/token
        else:
            est = None
        if est is None:
            unknown = True
        else:
            total += est
        lines.append((job, est))
    return lines, round(total, 3), unknown


# ---------------------------------------------------------------- esecuzione

def save_b64(b64, media_type, path_noext):
    path = path_noext + EXT.get(media_type or "image/png", ".png")
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64))
    return path


def run_image(job, payload, out_dir):
    res = http("POST", "/images", payload)
    files = []
    for i, item in enumerate(res.get("data", [])):
        suffix = "" if i == 0 else f"-{i + 1}"
        files.append(save_b64(item["b64_json"], item.get("media_type"), os.path.join(out_dir, job["name"] + suffix)))
    if not files:
        raise MediaError(f"nessuna immagine restituita: {json.dumps(res)[:400]}")
    return files, (res.get("usage") or {}).get("cost")


def run_speech(job, payload, out_dir):
    data = http("POST", "/audio/speech", payload, raw=True, timeout=600)
    if not data or data[:1] == b"{":
        raise MediaError(f"nessun audio restituito: {data[:300]!r}")
    ext = ".mp3" if payload.get("response_format", "mp3") == "mp3" else ".pcm"
    path = os.path.join(out_dir, job["name"] + ext)
    with open(path, "wb") as f:
        f.write(data)
    return [path], None


def run_video(job, payload, out_dir, poll=15, max_wait=45 * 60):
    sub = http("POST", "/videos", payload)
    url, t0 = sub["polling_url"], time.time()
    print(f"    job video {sub['id']} in coda", flush=True)
    while True:
        time.sleep(poll)
        st = http("GET", url)
        status = st.get("status")
        if status == "completed":
            break
        if status in ("failed", "cancelled", "expired"):
            raise MediaError(f"video {status}: {st.get('error')}")
        if time.time() - t0 > max_wait:
            raise MediaError(f"video ancora '{status}' dopo {max_wait // 60} minuti")
        print(f"    ... {status} ({int(time.time() - t0)} s)", flush=True)
    files = []
    for i, u in enumerate(st.get("unsigned_urls") or []):
        data = http("GET", u, raw=True, timeout=900)
        path = os.path.join(out_dir, job["name"] + ("" if i == 0 else f"-{i + 1}") + ".mp4")
        with open(path, "wb") as f:
            f.write(data)
        files.append(path)
    return files, (st.get("usage") or {}).get("cost")


def run(request_path, out_root):
    with open(request_path) as f:
        request = json.load(f)
    base_dir = os.path.dirname(os.path.abspath(request_path))
    req_id = request.get("id") or os.path.splitext(os.path.basename(request_path))[0]
    out_dir = os.path.join(out_root, req_id)
    os.makedirs(out_dir, exist_ok=True)
    if not os.environ.get("OPENROUTER_API_KEY"):
        raise MediaError("OPENROUTER_API_KEY non impostata: niente generazione")
    max_usd = float(request.get("max_usd", 5))
    lines, estimate, unknown = plan(request, base_dir)
    failed = set()
    if estimate > max_usd:
        raise MediaError(f"stima video {estimate} $ oltre il tetto max_usd={max_usd} $: alza il tetto o riduci i job")
    spent, outputs, results, ok = 0.0, {}, [], True
    for job, est in lines:
        if spent >= max_usd:
            results.append({"name": job["name"], "status": "skipped", "reason": "tetto di spesa raggiunto"})
            failed.add(job["name"])
            ok = False
            continue
        if est is not None and spent + est > max_usd:
            results.append({"name": job["name"], "status": "skipped", "reason": f"stima {est} $ oltre il tetto residuo"})
            failed.add(job["name"])
            ok = False
            continue
        deps = {(it if isinstance(it, str) else it.get("ref") or "")[1:].partition(":")[0]
                for key in ("frame_images", "input_references") for it in job.get(key, [])
                if (it if isinstance(it, str) else it.get("ref") or "").startswith("@")}
        if deps & failed:
            failed.add(job["name"])
            ok = False
            results.append({"name": job["name"], "status": "skipped", "reason": "dipende da un job non riuscito: " + ", ".join(sorted(deps & failed))})
            continue
        print(f"→ {job['name']} · {job['type']} · {job['model']}", flush=True)
        t0 = time.time()
        try:
            payload = build_payload(job, outputs, base_dir)
            runner = {"image": run_image, "video": run_video, "speech": run_speech}[job["type"]]
            files, cost = runner(job, payload, out_dir)
            outputs[job["name"]] = files[0]
            spent += float(cost or est or 0)
            results.append({"name": job["name"], "type": job["type"], "model": job["model"], "status": "ok",
                            "files": [os.path.relpath(p, out_root) for p in files],
                            "cost_usd": cost, "seconds": round(time.time() - t0, 1)})
            print(f"  ok in {time.time() - t0:.0f} s · costo {cost} $ · {', '.join(os.path.basename(p) for p in files)}", flush=True)
        except MediaError as e:
            ok = False
            failed.add(job["name"])
            results.append({"name": job["name"], "type": job["type"], "model": job["model"], "status": "error", "error": str(e)})
            print(f"  ERRORE: {e}", flush=True)
    manifest = {
        "request": os.path.relpath(os.path.abspath(request_path), ROOT),
        "id": req_id,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "max_usd": max_usd,
        "spent_usd": round(spent, 4),
        "jobs": results,
        "prompts": {j["name"]: j["prompt"] for j in request["jobs"]},
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    return manifest, ok


# ---------------------------------------------------------------- CLI

def cmd_models(a):
    kinds = ["image", "video"] if a.type == "all" else [a.type]
    for kind in kinds:
        ms = sorted(catalog(kind).values(), key=lambda m: -m.get("created", 0))[: a.limit]
        print(f"\n== modelli {kind} (più recenti per primi) ==")
        for m in ms:
            day = datetime.date.fromtimestamp(m.get("created", 0)).isoformat()
            if kind == "video":
                extra = (f"durate {m.get('supported_durations')} · {m.get('supported_resolutions')} · "
                         f"frame {m.get('supported_frame_images')} · audio {m.get('generate_audio')} · $ {m.get('pricing_skus')}")
            else:
                sp = m.get("supported_parameters", {})
                extra = " · ".join(f"{k} {v.get('values')}" for k, v in sp.items()
                                   if isinstance(v, dict) and v.get("type") == "enum" and k in ("resolution", "background", "quality"))
            print(f"{day}  {m['id']}\n            {extra}")


def cmd_check(a):
    ok = True
    for path in a.requests:
        with open(path) as f:
            request = json.load(f)
        try:
            lines, total, unknown = plan(request, os.path.dirname(os.path.abspath(path)))
        except MediaError as e:
            print(f"✗ {path}: {e}")
            ok = False
            continue
        print(f"✓ {path} · tetto {request.get('max_usd', 5)} $")
        for job, est in lines:
            cost = f"~{est} $" if est is not None else "costo a consumo (immagine)"
            print(f"   - {job['name']:<22} {job['type']:<5} {job['model']:<40} {cost}")
        print(f"   stima video: {total} $" + (" + immagini a consumo" if unknown else ""))
        if total > float(request.get("max_usd", 5)):
            print("   ✗ la stima supera max_usd")
            ok = False
    sys.exit(0 if ok else 1)


def cmd_run(a):
    all_ok = True
    summary = []
    for path in a.requests:
        try:
            manifest, ok = run(path, a.out)
        except MediaError as e:
            print(f"✗ {path}: {e}")
            all_ok = False
            summary.append(f"| `{path}` | errore: {e} | | |")
            continue
        all_ok &= ok
        for j in manifest["jobs"]:
            summary.append(f"| `{manifest['id']}/{j['name']}` | {j['status']} | {j.get('model', '')} | {j.get('cost_usd', '')} |")
        print(f"= {manifest['id']}: spesi {manifest['spent_usd']} $ su {manifest['max_usd']} $")
    step = os.environ.get("GITHUB_STEP_SUMMARY")
    if step:
        with open(step, "a") as f:
            f.write("### Media generati con OpenRouter\n\n| job | stato | modello | costo $ |\n|---|---|---|---|\n")
            f.write("\n".join(summary) + "\n")
    sys.exit(0 if all_ok else 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("models", help="elenca i modelli immagine/video, i più recenti per primi")
    p.add_argument("--type", choices=["image", "video", "all"], default="all")
    p.add_argument("--limit", type=int, default=15)
    p.set_defaults(fn=cmd_models)
    p = sub.add_parser("check", help="valida le richieste e stima i costi, senza spendere")
    p.add_argument("requests", nargs="+")
    p.set_defaults(fn=cmd_check)
    p = sub.add_parser("run", help="genera (serve OPENROUTER_API_KEY)")
    p.add_argument("requests", nargs="+")
    p.add_argument("--out", default=os.path.join(ROOT, "media", "out"))
    p.set_defaults(fn=cmd_run)
    a = ap.parse_args()
    try:
        a.fn(a)
    except MediaError as e:
        sys.exit(f"errore: {e}")


if __name__ == "__main__":
    main()
