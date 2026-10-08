"""Genera i pacchetti di slide ChallengEat 8 come file HTML autonomi.

Uso:  python3 slides/build.py
Output: slides/naturitalia.html, slides/rago.html

Il template (CSS, navigazione, illustrazioni) è condiviso; i contenuti
stanno in content_naturitalia.py e content_rago.py.
"""
import base64
import html
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import illustrations as ill  # noqa: E402
import content_naturitalia  # noqa: E402
import content_rago  # noqa: E402

LOGO = "data:image/png;base64," + base64.b64encode((HERE / "foodhub-logo.png").read_bytes()).decode()

CSS = (HERE / "template.css").read_text(encoding="utf-8")
JS = (HERE / "template.js").read_text(encoding="utf-8")


def ul(items, cls=""):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def footer(deck, n, total):
    return (
        f'<div class="footer"><span class="logo" role="img" aria-label="Food Hub"></span><span>ChallengEat 8 · {deck["short"]}</span></div>'
        f'<div class="pageno">{n} / {total}</div>'
    )


def title(t):
    return f'<h2 class="title">{t}</h2>'


def render(s, deck):
    k = s["type"]
    if k == "cover":
        mentors = " · ".join(s["mentors"])
        return f"""
<div class="cover-grid">
  <div class="cover-text">
    <span class="logo cover-logo" role="img" aria-label="Food Hub"></span>
    <p class="eyebrow">ChallengEat 8 · Edizione 2026</p>
    <h1>{s["title"]}</h1>
    <p class="subtitle">{s["subtitle"]}</p>
    <div class="pills"><span class="pill">{s["date"]}</span><span class="pill pill-soft">{s["duration"]}</span></div>
  </div>
  <div class="illus">{ill.get(s["illus"])}</div>
</div>
<p class="cover-mentors">{s["mentor_label"]}: {mentors}</p>"""
    if k == "section":
        return f"""
<div class="sec-deco">{ill.SECTION_DECO}</div>
<div class="sec-text"><p class="sec-num">{s["num"]}</p><h1>{s["title"]}</h1></div>
<p class="sec-foot">ChallengEat 8 · {deck["short"]}</p>"""
    if k == "content":
        side = " reverse" if s.get("side") == "left" else ""
        lead = f'<p class="lead">{s["lead"]}</p>' if s.get("lead") else ""
        return f"""{title(s["title"])}
<div class="content-row{side}">
  <div class="content-text">{lead}{ul(s["bullets"], "dots")}</div>
  <div class="illus">{ill.get(s["illus"])}</div>
</div>"""
    if k == "cards":
        cards = ""
        for c in s["cards"]:
            tag = f'<p class="card-tag">{c["tag"]}</p>' if c.get("tag") else ""
            cards += f'<div class="card">{tag}<h3>{c["title"]}</h3>{ul(c["bullets"], "dots small")}</div>'
        note = f'<p class="band">{s["note"]}</p>' if s.get("note") else ""
        return f'{title(s["title"])}<div class="cards cards-{len(s["cards"])}">{cards}</div>{note}'
    if k == "routing":
        rows = ""
        for r in s["rows"]:
            rows += (
                f'<div class="route"><div class="route-who" style="background:{r["color"]}">{r["who"]}</div>'
                f'<div class="route-arrow"></div><p class="route-what">{r["what"]}</p></div>'
            )
        return f'{title(s["title"])}<div class="content-row"><div class="routes">{rows}</div><div class="illus illus-sm">{ill.get(s["illus"])}</div></div>'
    if k == "flow":
        nodes = ""
        for i, nd in enumerate(s["nodes"]):
            if i:
                nodes += '<div class="flow-arrow"><svg viewBox="0 0 40 40"><path d="M6 20h24M22 11l9 9-9 9" fill="none" stroke="#D3134A" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
            owner = f'<p class="flow-owner">{nd["owner"]}</p>' if nd.get("owner") else ""
            nodes += f'<div class="flow-node"><p class="flow-num">{i + 1}</p><h3>{nd["name"]}</h3>{owner}<p class="flow-desc">{nd["desc"]}</p></div>'
        extra = ""
        if s.get("side_actors"):
            extra = '<div class="actors">' + "".join(
                f'<div class="actor"><b>{a["name"]}</b> {a["desc"]}</div>' for a in s["side_actors"]
            ) + "</div>"
        note = f'<p class="band">{s["note"]}</p>' if s.get("note") else ""
        return f'{title(s["title"])}<div class="flow">{nodes}</div>{extra}{note}'
    if k == "steps":
        steps = "".join(
            f'<div class="step"><p class="step-num">{i + 1}</p><p class="step-text">{t}</p></div>'
            for i, t in enumerate(s["steps"])
        )
        note = f'<p class="band">{s["note"]}</p>' if s.get("note") else ""
        return f'{title(s["title"])}<div class="steps">{steps}</div>{note}'
    if k == "statement":
        return f"""
<p class="eyebrow eyebrow-light">La sfida</p>
<h1 class="statement">{s["question"]}</h1>
{ul(s["bullets"], "dots light")}"""
    if k == "objectives":
        chips = "".join(f'<li>{c}</li>' for c in s["secondary"])
        return f"""{title(s["title"])}
<div class="obj">
  <div class="obj-main"><p class="card-tag light">Obiettivo primario</p>{ul(s["primary"], "dots light")}</div>
  <div class="obj-side"><p class="card-tag">Obiettivi secondari</p><ul class="checks">{chips}</ul></div>
</div>"""
    if k == "twocol":
        return f"""{title(s["title"])}
<div class="twocol">
  <div class="panel panel-in"><h3><span class="mark">{ill.CHECK}</span>Dentro il perimetro</h3>{ul(s["inside"], "dots small")}</div>
  <div class="panel panel-out"><h3><span class="mark">{ill.CROSS}</span>Fuori dal perimetro</h3>{ul(s["outside"], "dots small")}</div>
</div>"""
    if k == "timeline":
        weeks = ""
        for w in s["weeks"]:
            cls = " week-tbc" if w.get("tbc") else ""
            weeks += (
                f'<div class="week{cls}"><div class="week-dot"></div><p class="week-num">Settimana {w["n"]}</p>'
                f'<p class="week-date">{w["date"]}</p><h3>{w["phase"]}</h3>{ul(w["out"], "dots tiny")}</div>'
            )
        return f'{title(s["title"])}<div class="timeline"><div class="timeline-line"></div>{weeks}</div>'
    if k == "criteria":
        pct = {"Alta": 100, "Media-Alta": 75, "Media": 50}
        rows = ""
        for c, w in s["rows"]:
            rows += (
                f'<div class="crit"><p class="crit-name">{c}</p>'
                f'<div class="crit-bar"><div style="width:{pct[w]}%"></div></div><p class="crit-w">{w}</p></div>'
            )
        return f'{title(s["title"])}<p class="crit-head"><span>Criterio</span><span>Peso orientativo</span></p><div class="crits">{rows}</div>'
    if k == "questions":
        qs = "".join(
            f'<div class="q"><p class="q-num">{i + 1:02d}</p><p class="q-text">{q}</p></div>'
            for i, q in enumerate(s["questions"])
        )
        lead = f'<p class="lead">{s["lead"]}</p>' if s.get("lead") else ""
        return f'{title(s["title"])}{lead}<div class="qgrid">{qs}</div>'
    if k == "stats":
        st = "".join(
            f'<div class="stat"><p class="stat-num">{a}</p><p class="stat-label">{b}</p></div>' for a, b in s["stats"]
        )
        note = f'<p class="band">{s["note"]}</p>' if s.get("note") else ""
        return f'{title(s["title"])}<div class="stats">{st}</div>{note}'
    if k == "closing":
        return f"""
<div class="closing">
  <span class="logo closing-logo" role="img" aria-label="Food Hub"></span>
  <h1>{s["title"]}</h1>
  <p class="subtitle">{s["subtitle"]}</p>
  <p class="closing-meta">{s["meta"]}</p>
</div>"""
    raise ValueError(k)


BG = {"section": "sec", "statement": "dark"}


def build(deck, out):
    slides = deck["slides"]
    total = len(slides)
    parts = []
    for i, s in enumerate(slides, 1):
        body = render(s, deck)
        if s["type"] not in ("cover", "section", "closing", "statement"):
            body += footer(deck, i, total)
        parts.append(f'<section class="slide t-{s["type"]} bg-{BG.get(s["type"], "light")}" data-n="{i}">{body}</section>')
    doc = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(deck["title"])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=DM+Sans:wght@400;500;700&display=swap">
<style>
{CSS}
.logo {{ display: inline-block; background: url({LOGO}) center / contain no-repeat; }}
</style>
</head>
<body>
<main class="deck">
{chr(10).join(parts)}
</main>
<div class="hud"><span id="hud-n"></span> · ← → per navigare · F schermo intero · O panoramica · stampa per il PDF</div>
<script>
{JS}
</script>
</body>
</html>
"""
    (HERE / out).write_text(doc, encoding="utf-8")
    print(f"{out}: {total} slide")


if __name__ == "__main__":
    build(content_naturitalia.DECK, "naturitalia.html")
    build(content_rago.DECK, "rago.html")
