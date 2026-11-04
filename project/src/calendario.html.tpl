<!doctype html>
<html lang="it">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1350" />
    <!-- GENERATO da src/build.py: non modificare a mano, modifica src/calendario.html.tpl e src/giornate.js -->
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "BC"; font-weight: 200; src: url(assets/fonts/barlow-condensed-latin-200-normal.woff2) format("woff2"); }
      @font-face { font-family: "BC"; font-weight: 200; src: url(assets/fonts/barlow-condensed-latin-ext-200-normal.woff2) format("woff2"); unicode-range: U+0100-024F, U+1E00-1EFF; }
      @font-face { font-family: "BC"; font-weight: 300; src: url(assets/fonts/barlow-condensed-latin-300-normal.woff2) format("woff2"); }
      @font-face { font-family: "BC"; font-weight: 300; src: url(assets/fonts/barlow-condensed-latin-ext-300-normal.woff2) format("woff2"); unicode-range: U+0100-024F, U+1E00-1EFF; }
      @font-face { font-family: "BC"; font-weight: 400; src: url(assets/fonts/barlow-condensed-latin-400-normal.woff2) format("woff2"); }
      @font-face { font-family: "BC"; font-weight: 500; src: url(assets/fonts/barlow-condensed-latin-500-normal.woff2) format("woff2"); }
      @font-face { font-family: "BC"; font-weight: 500; src: url(assets/fonts/barlow-condensed-latin-ext-500-normal.woff2) format("woff2"); unicode-range: U+0100-024F, U+1E00-1EFF; }

      :root { --cream: #fcfcf6; --green-dark: #517053; --green-soft: #adcf92; --ink: #111; }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1350px; overflow: hidden; background: var(--cream); }
      #root { position: relative; width: 1080px; height: 1350px; overflow: hidden; background: var(--cream); font-family: "BC", sans-serif; color: var(--ink); }

      /* Palco con le coordinate esatte del PDF (1081.31 x 1353.74 pt) */
      #stage { position: absolute; left: 0; top: 0; width: 1081.31px; height: 1353.74px; transform: scale(0.998789); transform-origin: 0 0; }

      /* ---------- Intestazione ---------- */
      #waves { position: absolute; left: 0; top: 0; width: 1081.31px; height: 1353.74px; z-index: 5; overflow: visible; }
      .hdr { position: absolute; z-index: 6; color: #fff; white-space: nowrap; }
      #title { left: 57px; top: 54.6px; font-weight: 500; font-size: 66.8px; line-height: 66.8px; }
      #title .ch { display: inline-block; }
      .sb #title { overflow: hidden; padding-right: 6px; }
      #giornata { left: 0; top: 131.4px; width: 400px; height: 40px; font-weight: 300; font-size: 37.2px; line-height: 37.2px; }
      #giornata .gc { position: absolute; top: 0; }
      #festMark { position: absolute; z-index: 6; overflow: visible; }
      #festMark path { transform-box: fill-box; transform-origin: 50% 100%; }
      #festTxt { left: 877px; top: 68.5px; font-size: 27.27px; line-height: 26px; font-weight: 300; }
      #festTxt b { font-weight: 500; }
      #festEd { left: 0; top: 154px; width: 1081px; height: 16px; font-size: 11.4px; line-height: 15px; font-weight: 500; }
      #festEd span { position: absolute; top: 0; }
      #festEd .sm { font-size: 7.3px; line-height: 10px; }

      /* ---------- Programma ---------- */
      #viewport { position: absolute; left: 0; top: 0; width: 1081.31px; height: 1353.74px; z-index: 2; }
      .row { position: absolute; left: 0; width: 1081px; height: 60px; }
      .dash { position: absolute; top: 28px; height: 2px; transform-origin: 0 50%; }
      .sb .dash { transform-origin: 100% 50%; }
      .p1 .dash { left: 12.39px; width: 120.8px; background: repeating-linear-gradient(90deg, var(--green-dark) 0 12.714px, transparent 12.714px 25.428px); }
      .p2 .dash { left: -2.63px; width: 136px;
        background: linear-gradient(90deg, var(--green-dark) 0 6px, transparent 6px 18.37px),
                    repeating-linear-gradient(90deg, var(--green-dark) 0 12.379px, transparent 12.379px 24.758px) 18.37px 0 / 117.6px 2px no-repeat; }
      .dot { position: absolute; left: calc(137px + var(--dx, 0px)); top: 14px; width: 30px; height: 30px; border-radius: 50%; background: var(--green-soft); }
      .dot i { position: absolute; left: 7.5px; top: 7.5px; width: 15px; height: 15px; border-radius: 50%; background: var(--green-dark); }
      .head { position: absolute; left: calc(182px + var(--dx, 0px)); top: 0.5px; height: 50px; font-size: 39.4px; line-height: 50px; white-space: nowrap; }
      .sb .head { overflow: hidden; padding-right: 4px; }
      .head .tm, .head .co { display: inline-block; font-weight: 500; }
      .head .sep { font-weight: 200; display: inline-block; }
      .head .sp { font-weight: 300; display: inline-block; }
      .ttl { position: absolute; left: calc(182px + var(--dx, 0px)); font-size: 32.8px; line-height: 39.5px; font-weight: 300; white-space: nowrap; color: #2a2a2a; }
      .ttl .w, .ttl .ln { display: inline-block; }
      .row.green .head { color: var(--green-dark); }
      .dash.free { left: 0; background: none; }
      .dash .seg { position: absolute; top: 0; height: 2px; background: var(--green-dark); }
      .sc .ttl .lnw { display: inline-block; overflow: hidden; vertical-align: top; }
      .sc #cta { overflow: hidden; }

      /* Food Hub */
      .row.fh .blob { position: absolute; left: 55px; top: -51px; width: 840px; height: 175px; overflow: visible; }
      .row.fh .logo { position: absolute; left: 70px; top: 7.75px; width: 96.91px; height: 96.91px; }
      .row.fh .logo svg { width: 100%; height: 100%; display: block; }
      .row.fh .head, .row.fh .ttl { color: var(--cream); }

      /* ---------- Fascia finale (pagina 2) ---------- */
      #cta { position: absolute; left: 0; top: 1197.13px; width: 1081px; height: 70px; z-index: 7; }
      #cta svg { position: absolute; left: 0; top: 0; width: 943px; height: 70px; overflow: visible; }
      #cta .lbl { position: absolute; left: var(--lbl, 183px); top: 3.4px; color: #fff; font-size: 42.7px; line-height: 56px; white-space: nowrap; }
      #cta .lbl b { font-weight: 500; display: inline-block; }
      #cta .lbl span { font-weight: 300; display: inline-block; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{{DURATION}}" data-width="1080" data-height="1350">
      <div id="stage" class="clip" data-start="0" data-duration="{{DURATION}}">

        <svg id="waves" viewBox="0 0 1081.31 1353.74">
          <path id="waveDark" fill="#517053" d="{{WAVE_DARK}}" />
          <path id="waveLight" fill="#72AD47" fill-opacity="0.55" d="{{WAVE_LIGHT}}" />
        </svg>

        <div id="title" class="hdr"></div>
        <div id="giornata" class="hdr"></div>
        {{FEST_MARK}}
        <div id="festTxt" class="hdr">Festival<br />dell’<b>Innovazione</b><br /><b>Agroalimentare</b></div>
        <div id="festEd" class="hdr"></div>

        <div id="viewport"></div>

        <div id="cta">
          <svg viewBox="0 1197.13 943 70"><path id="ctaBand" fill="#D3134B" d="{{BANNER}}" /></svg>
          <div class="lbl"><b id="ctaDate">9-12 NOVEMBRE 2026</b><span id="ctaMid">&nbsp;- EVENTO ONLINE&nbsp;</span><b id="ctaFree">GRATUITO</b></div>
        </div>
      </div>

      <!-- Effetti sonori (sintetizzati, in assets/sfx). La musica la aggiunge il cliente. -->
      <div id="sfx"></div>
    </div>

    <script>
{{DATA}}
      const DAY = "{{DAY}}";
      const PAGE = {{PAGE}};
      const DURATION = {{DURATION}};
      const FOODHUB_LOGO = `{{FH_LOGO}}`;
      const BLOB = `<svg class="blob" viewBox="55 890 840 175" preserveAspectRatio="none">
        <path class="bd" fill="#517053" d="{{BLOB_DARK}}"/>
        <path class="bl" fill="#72AD47" fill-opacity="0.55" d="{{BLOB_LIGHT}}"/></svg>`;

      const G = GIORNATE[DAY];
      const P = G.pages[PAGE];
      const STYLE = G.style;
      const ROWS = P.rows;
      const AT = P.at;
      const CTA_AT = P.cta;
      document.getElementById("root").classList.add("s" + STYLE);

      const words = (s) => s.split(" ").map((w) => `<span class="w">${w}</span>`).join(" ");

      // ------------------------------------------------------------------
      // Intestazione (posizioni dei caratteri prese dalla grafica)
      // ------------------------------------------------------------------
      document.getElementById("title").innerHTML = G.date.split("").map((c) => `<span class="ch">${c === " " ? "&nbsp;" : c}</span>`).join("");
      document.getElementById("giornata").innerHTML = G.giornata.map(([c, x]) => `<span class="gc" style="left:${x}px">${c}</span>`).join("");
      const EDIZ = [["5", 878, ""], ["a", 883, "sm"], ["E", 901, ""], ["D", 918, ""], ["I", 936, ""], ["Z", 952, ""], ["I", 969, ""], ["O", 984, ""], ["N", 1002, ""], ["E", 1020, ""]];
      document.getElementById("festEd").innerHTML = EDIZ.map(([c, x, k]) => `<span class="${k}" style="left:${x}px">${c}</span>`).join("");

      // ------------------------------------------------------------------
      // Righe del programma
      // ------------------------------------------------------------------
      const vp = document.getElementById("viewport");
      ROWS.forEach((r, i) => {
        const el = document.createElement("div");
        el.className = `row p${PAGE} ${r.k || ""}`;
        el.id = "r" + i;
        el.style.top = r.y + "px";
        if (G.dx) el.style.setProperty("--dx", G.dx + "px");
        let html;
        if (r.k === "fh") {
          // Box del blob e del logo: predefiniti del 9 novembre, sovrascrivibili per giornata
          const b = Object.assign({ left: 55, top: -51, w: 840, h: 175 }, G.fhBlob || {});
          const l = Object.assign({ left: 70, top: 7.75, size: 96.91 }, G.fhLogo || {});
          html = BLOB.replace('class="blob"', `class="blob" style="left:${b.left}px;top:${b.top}px;width:${b.w}px;height:${b.h}px"`) +
            `<div class="logo" style="left:${l.left}px;top:${l.top}px;width:${l.size}px;height:${l.size}px">${FOODHUB_LOGO}</div>`;
        } else if (G.dash) {
          // Tratteggio a segmenti separati: inizio, passo, lunghezza, fine (pt)
          const d = G.dash[PAGE];
          let segs = "";
          for (let x = d.start; x < d.end; x += d.period) {
            const a = Math.max(0, x), z = Math.min(d.end, x + d.len);
            if (z > a) segs += `<i class="seg" style="left:${a.toFixed(2)}px;width:${(z - a).toFixed(2)}px"></i>`;
          }
          html = `<div class="dash free" style="width:${d.end}px">${segs}</div><div class="dot" style="top:${r.dot ?? 14}px"><i></i></div>`;
        } else {
          html = `<div class="dash"></div><div class="dot" style="top:${r.dot ?? 14}px"><i></i></div>`;
        }
        if (r.sp) {
          html += `<div class="head"><span class="tm">${r.tm}</span> <span class="co">${r.co}</span><span class="sep">&nbsp;|&nbsp;</span><span class="sp">${r.sp}</span></div>`;
        } else {
          html += `<div class="head"><span class="tm">${r.tm}</span><span class="sep">&nbsp;|&nbsp;</span><span class="co">${r.co}</span></div>`;
        }
        if (r.t) {
          const lines = STYLE === "b" ? r.t.map((l) => `<span class="ln">${l}</span>`)
            : STYLE === "c" ? r.t.map((l) => `<span class="lnw"><span class="ln">${l}</span></span>`)
            : r.t.map(words);
          html += `<div class="ttl" style="top:${r.off + 1.5}px">${lines.join("<br>")}</div>`;
        }
        el.innerHTML = html;
        vp.appendChild(el);
      });
      if (PAGE !== 2) document.getElementById("cta").remove();
      else if (G.cta) {
        const c = document.getElementById("cta");
        c.style.top = G.cta.top + "px";
        c.style.setProperty("--lbl", G.cta.lblLeft + "px");
        if (G.cta.band) document.getElementById("ctaBand").setAttribute("d", G.cta.band);
        if (G.cta.vbY) c.querySelector("svg").setAttribute("viewBox", `0 ${G.cta.vbY} 943 70`);
      }

      // ------------------------------------------------------------------
      // Effetti sonori: mai lo stesso due volte di fila
      // ------------------------------------------------------------------
      const SFX_LEN = {
        "whoosh-1": 0.6, "whoosh-2": 0.5, "whoosh-3": 0.45, "pop-1": 0.18, "pop-2": 0.16, "pop-3": 0.2,
        "tick-1": 0.05, "tick-2": 0.05, "tick-3": 0.05, "impact-1": 0.6,
        "pluck-1": 0.6, "pluck-2": 0.6, "pluck-3": 0.6, "pluck-4": 0.6, "pluck-5": 0.6, "pluck-6": 0.6,
        "swish-1": 0.45, "swish-2": 0.55, "bloop-1": 0.35, "chime-1": 1.3,
        "flip-1": 0.14, "flip-2": 0.14, "flip-3": 0.14, "shimmer-1": 1.0, "drop-1": 0.3, "riser-1": 0.7, "ding-1": 2.0,
      };
      const sfxBox = document.getElementById("sfx");
      P.cues(AT, CTA_AT).forEach(([t, name, vol], i) => {
        const a = document.createElement("audio");
        a.id = "sfx" + i;
        a.className = "clip";
        a.src = `assets/sfx/${name}.wav`;
        a.dataset.start = t.toFixed(2);
        a.dataset.duration = SFX_LEN[name];
        a.dataset.volume = vol;
        a.dataset.trackIndex = 10 + (i % 3);
        sfxBox.appendChild(a);
      });

      // ------------------------------------------------------------------
      // Timeline
      // ------------------------------------------------------------------
      const tl = gsap.timeline({ paused: true });
      ROWS.forEach((r, i) => tl.set("#r" + i, { opacity: 0 }, 0));

      if (STYLE === "a") {
        // ===== Stile A (9 novembre): onde dall'alto, lettere che rimbalzano =====
        tl.fromTo("#waveDark", { y: -330 }, { y: 0, duration: 0.8, ease: "power3.out" }, 0);
        tl.fromTo("#waveLight", { y: -380, scaleY: 1.06 }, { y: 0, scaleY: 1, duration: 0.95, ease: "power3.out", transformOrigin: "50% 0%" }, 0.06);
        tl.fromTo("#title .ch", { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.8)", stagger: 0.035 }, 0.35);
        document.querySelectorAll("#giornata .gc").forEach((el, i) => {
          tl.fromTo(el, { x: -i * 13, opacity: 0 }, { x: 0, opacity: 1, duration: 0.7, ease: "power3.out" }, 0.65);
        });
        tl.fromTo("#festMark path", { scaleY: 0 }, { scaleY: 1, duration: 0.5, ease: "back.out(1.6)", stagger: 0.06 }, 0.55);
        tl.fromTo("#festTxt, #festEd", { opacity: 0, x: 18 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 0.85);

        ROWS.forEach((r, i) => {
          const t = AT[i];
          const id = "#r" + i;
          tl.set(id, { opacity: 1 }, t);

          if (r.k === "fh") {
            tl.fromTo(id + " .bd", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.45, ease: "power3.out" }, t);
            tl.fromTo(id + " .bl", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.5, ease: "power3.out" }, t + 0.08);
            tl.fromTo(id + " .logo", { scale: 0, rotation: -120 }, { scale: 1, rotation: 0, duration: 0.55, ease: "back.out(2)" }, t + 0.4);
            tl.fromTo(id + " .head .tm, " + id + " .head .co", { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: "power3.out", stagger: 0.06 }, t + 0.3);
            tl.fromTo(id + " .head .sep, " + id + " .head .sp", { opacity: 0 }, { opacity: 1, duration: 0.3 }, t + 0.5);
            tl.fromTo(id + " .ttl .w", { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.25, ease: "power2.out", stagger: 0.025 }, t + 0.6);
            // punch-in 1.2x ancorato alla riga Food Hub, poi rientro
            tl.set("#viewport", { transformOrigin: `40px ${r.y + 55}px` }, t);
            tl.to("#viewport", { scale: 1.2, duration: 0.5, ease: "power3.out" }, t + 0.25);
            tl.to("#viewport", { scale: 1, duration: 0.6, ease: "power2.inOut" }, t + 1.95);
            return;
          }

          tl.fromTo(id + " .dash", { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power2.out" }, t);
          tl.fromTo(id + " .dot", { scale: 0 }, { scale: 1, duration: 0.35, ease: "back.out(2.5)" }, t + 0.12);
          tl.fromTo(id + " .head .tm", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }, t + 0.1);
          tl.fromTo(id + " .head .co", { x: -30, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: "power3.out" }, t + 0.18);
          tl.fromTo(id + " .head .sep", { opacity: 0 }, { opacity: 1, duration: 0.2 }, t + 0.2);
          if (r.lunch) {
            tl.fromTo(id + " .head", { scale: 1.12, transformOrigin: "0% 50%" }, { scale: 1, duration: 0.5, ease: "power3.out" }, t + 0.1);
          }
          if (r.sp) {
            tl.fromTo(id + " .head .sp", { opacity: 0, x: 12 }, { opacity: 1, x: 0, duration: 0.3, ease: "power2.out" }, t + 0.26);
            tl.fromTo(id + " .ttl .w", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.22, ease: "power2.out", stagger: 0.018 }, t + 0.3);
          }
        });

        if (PAGE === 2) {
          tl.fromTo("#ctaBand", { x: -950 }, { x: 0, duration: 0.6, ease: "power3.out" }, CTA_AT);
          tl.fromTo("#ctaDate", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, CTA_AT + 0.3);
          tl.fromTo("#ctaMid", { opacity: 0 }, { opacity: 1, duration: 0.3 }, CTA_AT + 0.5);
          tl.fromTo("#ctaFree", { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.2)" }, CTA_AT + 0.75);
          tl.to("#ctaFree", { scale: 1.08, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 3 }, CTA_AT + 1.4);
        }
      } else if (STYLE === "c") {
        // ===== Stile C (11 novembre): tendina, macchina da scrivere, righe che si ribaltano =====
        tl.fromTo("#waveDark", { scaleY: 0, transformOrigin: "50% 0%" }, { scaleY: 1, duration: 0.7, ease: "back.out(1.4)" }, 0);
        tl.fromTo("#waveLight", { scaleY: 0, transformOrigin: "50% 0%" }, { scaleY: 1, duration: 0.8, ease: "back.out(1.4)" }, 0.12);
        tl.fromTo("#title .ch", { opacity: 0 }, { opacity: 1, duration: 0.01, stagger: 0.055 }, 0.45);
        tl.fromTo("#giornata .gc", { opacity: 0, x: 22 }, { opacity: 1, x: 0, duration: 0.35, ease: "power2.out", stagger: { each: 0.035, from: "end" } }, 0.8);
        tl.fromTo("#festMark path", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)", stagger: { each: 0.05, from: "center" } }, 0.5);
        tl.fromTo("#festTxt", { opacity: 0, x: -18 }, { opacity: 1, x: 0, duration: 0.45, ease: "power2.out" }, 0.75);
        tl.fromTo("#festEd", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.95);

        const flipIn = (sel, t) =>
          tl.fromTo(sel, { rotationX: -90, opacity: 0, transformOrigin: "50% 0%", transformPerspective: 600 }, { rotationX: 0, opacity: 1, duration: 0.45, ease: "power3.out" }, t);
        const wipeIn = (id, t) =>
          tl.fromTo(id + " .ttl .ln", { xPercent: -101 }, { xPercent: 0, duration: 0.45, ease: "power3.out", stagger: 0.1 }, t);

        ROWS.forEach((r, i) => {
          const t = AT[i];
          const id = "#r" + i;
          tl.set(id, { opacity: 1 }, t);

          if (r.k === "fh") {
            // Food Hub: il blob si gonfia dal logo, il logo cade e rimbalza, poi il blob "respira"
            tl.fromTo(id + " .blob", { scale: 0, transformOrigin: "4% 50%" }, { scale: 1, duration: 0.55, ease: "back.out(1.3)" }, t);
            tl.fromTo(id + " .bl", { opacity: 0 }, { opacity: 1, duration: 0.3 }, t + 0.15);
            tl.fromTo(id + " .logo", { y: -90, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: "bounce.out" }, t + 0.25);
            flipIn(id + " .head", t + 0.4);
            wipeIn(id, t + 0.6);
            tl.to(id + " .blob", { scale: 1.035, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 3 }, t + 1.1);
            return;
          }
          tl.fromTo(id + " .dot", { scale: 0, rotation: 180 }, { scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }, t);
          tl.fromTo(id + " .dot i", { scale: 0 }, { scale: 1, duration: 0.25, ease: "power2.out" }, t + 0.15);
          tl.fromTo(id + " .dash .seg", { opacity: 0, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.12, stagger: { each: 0.05, from: "end" } }, t + 0.05);
          flipIn(id + " .head", t + 0.08);
          if (r.t) wipeIn(id, t + 0.25);
          if (r.lunch) tl.to(id + " .dot", { rotation: 360, duration: 0.6, ease: "power2.inOut" }, t + 0.45);
        });

        if (PAGE === 2) {
          tl.fromTo("#ctaBand", { y: 75 }, { y: 0, duration: 0.5, ease: "power4.out" }, CTA_AT);
          tl.fromTo("#ctaDate", { y: 60 }, { y: 0, duration: 0.45, ease: "power4.out" }, CTA_AT + 0.2);
          tl.fromTo("#ctaMid", { y: 60 }, { y: 0, duration: 0.45, ease: "power4.out" }, CTA_AT + 0.3);
          tl.fromTo("#ctaFree", { y: 60 }, { y: 0, duration: 0.45, ease: "power4.out" }, CTA_AT + 0.4);
          tl.to("#ctaFree", { opacity: 0.25, duration: 0.12, yoyo: true, repeat: 3, ease: "none" }, CTA_AT + 0.95);
          tl.to("#ctaFree", { scale: 1.08, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 3 }, CTA_AT + 1.5);
        }
      } else {
        // ===== Stile B (10 novembre): onde laterali, testi che salgono da una maschera =====
        tl.fromTo("#waveLight", { x: 1100 }, { x: 0, duration: 0.9, ease: "expo.out" }, 0);
        tl.fromTo("#waveDark", { x: -1150 }, { x: 0, duration: 0.95, ease: "expo.out" }, 0.08);
        tl.fromTo("#title .ch", { y: 72 }, { y: 0, duration: 0.6, ease: "expo.out", stagger: 0.03 }, 0.4);
        tl.fromTo("#giornata .gc", { y: -26, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power2.out", stagger: 0.04 }, 0.7);
        tl.fromTo("#festMark path", { opacity: 0, y: -14 }, { opacity: 1, y: 0, duration: 0.45, ease: "power2.out", stagger: 0.05 }, 0.55);
        tl.fromTo("#festTxt", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.45, ease: "power2.out" }, 0.8);
        tl.fromTo("#festEd span", { opacity: 0 }, { opacity: 1, duration: 0.2, stagger: 0.03 }, 0.95);

        ROWS.forEach((r, i) => {
          const t = AT[i];
          const id = "#r" + i;
          tl.set(id, { opacity: 1 }, t);
          // prima il puntino, poi il tratteggio che corre verso sinistra
          tl.fromTo(id + " .dot", { scale: 0 }, { scale: 1, duration: 0.3, ease: "back.out(3)" }, t);
          tl.fromTo(id + " .dot i", { scale: 0 }, { scale: 1, duration: 0.25, ease: "power2.out" }, t + 0.1);
          tl.fromTo(id + " .dash", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power2.out" }, t + 0.08);
          // riga principale: sale dalla maschera
          tl.fromTo(id + " .head .tm", { y: 52 }, { y: 0, duration: 0.4, ease: "expo.out" }, t + 0.06);
          tl.fromTo(id + " .head .sep", { y: 52 }, { y: 0, duration: 0.4, ease: "expo.out" }, t + 0.1);
          tl.fromTo(id + " .head .co", { y: 52 }, { y: 0, duration: 0.4, ease: "expo.out" }, t + 0.12);
          if (r.sp) tl.fromTo(id + " .head .sp", { y: 52 }, { y: 0, duration: 0.4, ease: "expo.out" }, t + 0.18);
          if (r.t) tl.fromTo(id + " .ttl .ln", { opacity: 0, x: 26 }, { opacity: 1, x: 0, duration: 0.4, ease: "power3.out", stagger: 0.09 }, t + 0.22);
          if (r.lunch) {
            tl.to(id + " .dot", { scale: 1.35, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: 1 }, t + 0.35);
          }
        });

        if (PAGE === 2) {
          tl.fromTo("#ctaBand", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.55, ease: "expo.out" }, CTA_AT);
          tl.fromTo("#ctaDate, #ctaMid", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "expo.out", stagger: 0.1 }, CTA_AT + 0.25);
          tl.fromTo("#ctaFree", { opacity: 0, scale: 0.4, rotation: -8 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2.5)" }, CTA_AT + 0.8);
          tl.to("#ctaFree", { y: -6, duration: 0.35, ease: "sine.inOut", yoyo: true, repeat: 3 }, CTA_AT + 1.5);
        }
      }
      tl.to({}, { duration: 0.01 }, DURATION - 0.01);

      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
