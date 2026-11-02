<!doctype html>
<html lang="it">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1350" />
    <!-- GENERATO da src/build.py: non modificare a mano, modifica src/calendario.html.tpl -->
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
      .p1 .dash { left: 12.39px; width: 120.8px; background: repeating-linear-gradient(90deg, var(--green-dark) 0 12.714px, transparent 12.714px 25.428px); }
      .p2 .dash { left: -2.63px; width: 136px;
        background: linear-gradient(90deg, var(--green-dark) 0 6px, transparent 6px 18.37px),
                    repeating-linear-gradient(90deg, var(--green-dark) 0 12.379px, transparent 12.379px 24.758px) 18.37px 0 / 117.6px 2px no-repeat; }
      .dot { position: absolute; left: 137px; top: 14px; width: 30px; height: 30px; border-radius: 50%; background: var(--green-soft); }
      .dot i { position: absolute; left: 7.5px; top: 7.5px; width: 15px; height: 15px; border-radius: 50%; background: var(--green-dark); }
      .head { position: absolute; left: 182px; top: 0.5px; height: 50px; font-size: 39.4px; line-height: 50px; white-space: nowrap; }
      .head .tm, .head .co { display: inline-block; font-weight: 500; }
      .head .sep { font-weight: 200; }
      .head .sp { font-weight: 300; display: inline-block; }
      .ttl { position: absolute; left: 182px; font-size: 32.8px; line-height: 39.5px; font-weight: 300; white-space: nowrap; color: #2a2a2a; }
      .ttl .w { display: inline-block; }
      .row.green .head { color: var(--green-dark); }

      /* Food Hub */
      .row.fh .blob { position: absolute; left: 55px; top: -51px; width: 840px; height: 175px; overflow: visible; }
      .row.fh .logo { position: absolute; left: 70px; top: 7.75px; width: 96.91px; height: 96.91px; }
      .row.fh .logo svg { width: 100%; height: 100%; display: block; }
      .row.fh .head, .row.fh .ttl { color: var(--cream); }

      /* ---------- Fascia finale (pagina 2) ---------- */
      #cta { position: absolute; left: 0; top: 1197.13px; width: 1081px; height: 70px; z-index: 7; }
      #cta svg { position: absolute; left: 0; top: 0; width: 943px; height: 70px; }
      #cta .lbl { position: absolute; left: 183px; top: 3.4px; color: #fff; font-size: 42.7px; line-height: 56px; white-space: nowrap; }
      #cta .lbl b { font-weight: 500; display: inline-block; }
      #cta .lbl span { font-weight: 300; }
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
          <div class="lbl"><b id="ctaDate">9-12 NOVEMBRE 2026</b><span id="ctaMid"> - EVENTO ONLINE </span><b id="ctaFree">GRATUITO</b></div>
        </div>
      </div>

      <!-- Effetti sonori (sintetizzati, in assets/sfx). La musica la aggiunge il cliente. -->
      <div id="sfx"></div>
    </div>

    <script>
      const PAGE = {{PAGE}};
      const DURATION = {{DURATION}};
      const FOODHUB_LOGO = `{{FH_LOGO}}`;
      const BLOB = `<svg class="blob" viewBox="55 890 840 175" preserveAspectRatio="none">
        <path class="bd" fill="#517053" d="{{BLOB_DARK}}"/>
        <path class="bl" fill="#72AD47" fill-opacity="0.55" d="{{BLOB_LIGHT}}"/></svg>`;

      // ------------------------------------------------------------------
      // Programma: y = posizione esatta nel PDF, off = distanza del titolo
      // ------------------------------------------------------------------
      const PAGES = {
        1: [
          { y: 264, k: "green", tm: "9:00-9:30", co: "SESSIONE DI APERTURA" },
          { y: 334, off: 54, tm: "9:30-10:15", co: "PIM", sp: "Nicola Marcon", t: ["“I casi studi sulla tecnologia brevettata high speed cold dryer”"] },
          { y: 468, off: 47, tm: "10:15-11:00", co: "ICONS", sp: "Sofia Francescutto", t: ["“Innovazione agroalimentare: strategie per valorizzare, conoscere e", "adottare nuove soluzioni”"] },
          { y: 634, off: 46, tm: "11:15-12:00", co: "GEA", sp: "Andrea Bresciani", t: ["“Sviluppo di nuovi prodotti: dalla materia prima al processo”"] },
          { y: 760, off: 46, tm: "12:00-12:30", co: "ALKELUX", sp: "Martina Piga", t: ["“Dal laboratorio al mercato: il percorso dell'innovazione", "nel packaging alimentare”"] },
          { y: 941, off: 46, k: "fh", tm: "12:30-13:00", co: "FOOD HUB", sp: "Francesco De Carolis", t: ["“Come usare l'AI per analizzare i prodotti sul mercato”"] },
          { y: 1088, k: "green", tm: "13:00-14:00", co: "PAUSA PRANZO", lunch: true },
          { y: 1183, off: 46, tm: "14:00-14:30", co: "KLÜBER LUBRICATION", sp: "Lorenzo Fidanza", t: ["“Implicazioni della lubrificazione nella filiera agroalimentare”"] },
        ],
        2: [
          { y: 264, off: 46, tm: "14:30-15:00", co: "ICONS", sp: "Marco Petazzoni; Nicoletta Gomboli", t: ["“Food Sharing Compass: piattaforma e cinque strumenti per rendere", "l’innovazione utilizzabile”"] },
          { y: 430, off: 46, tm: "15:15-16:00", co: "HOENLE", sp: "Miriam Koessler; Stefano Fantini", t: ["“Il futuro della disinfezione industriale: soluzioni UV-C per processi più sicuri”"] },
          { y: 556, off: 46, tm: "16:00-16:30", co: "OPEN FIELDS", sp: "Silvia Folloni; Gianluca Giuberti", t: ["“Amido Resistente termostabile da MAIS Italiano: MAISTAR”"] },
          { y: 690, off: 46, tm: "16:30-17:00", co: "UNIFG", sp: "Amalia Conte", t: ["“Dallo Scarto alla Shelf life: Valorizzare i Sottoprodotti per Conservare", "gli Alimenti Freschi”"] },
          { y: 855, off: 54, tm: "16:30-17:00", co: "UNIPI", sp: "Costanza Ceccanti", t: ["“Dal campo alla tavola: come il vapore sovrassaturo aiuta a conservare i", "composti nutraceutici”"] },
          { y: 1029, off: 46, tm: "17:00-17:30", co: "NSPULSE", sp: "Mirko De Leonardis; Andrea Dell’Olio", t: ["“Fermentare l’innovazione alimentare: dalla progettazione prodotto allo", "scale up industriale”"] },
        ],
      };
      // Istanti di ingresso (s). Stesso ritmo della versione approvata.
      const TIMES = {
        1: [1.35, 1.95, 2.55, 3.15, 3.75, 4.45, 7.0, 7.6],
        2: [1.35, 1.95, 2.55, 3.15, 3.4, 4.2], // UNIFG e UNIPI quasi insieme: sono parallele
      };
      const ROWS = PAGES[PAGE];
      const AT = TIMES[PAGE];
      const CTA_AT = 5.0;

      const words = (s) => s.split(" ").map((w) => `<span class="w">${w}</span>`).join(" ");

      // ------------------------------------------------------------------
      // Intestazione (posizioni dei caratteri prese dal PDF)
      // ------------------------------------------------------------------
      document.getElementById("title").innerHTML = "9 NOVEMBRE".split("").map((c) => `<span class="ch">${c === " " ? "&nbsp;" : c}</span>`).join("");
      const GIORNATA = [["1", 61], ["ª", 87], ["G", 113], ["I", 145], ["O", 169], ["R", 202], ["N", 234], ["A", 268], ["T", 296], ["A", 326]];
      document.getElementById("giornata").innerHTML = GIORNATA.map(([c, x]) => `<span class="gc" style="left:${x}px">${c}</span>`).join("");
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
        let html = r.k === "fh" ? BLOB + `<div class="logo">${FOODHUB_LOGO}</div>` : `<div class="dash"></div><div class="dot"><i></i></div>`;
        if (!r.sp) {
          html += `<div class="head"><span class="tm">${r.tm}</span><span class="sep"> | </span><span class="co">${r.co}</span></div>`;
        } else {
          html += `<div class="head"><span class="tm">${r.tm}</span> <span class="co">${r.co}</span><span class="sep"> | </span><span class="sp">${r.sp}</span></div>`;
          html += `<div class="ttl" style="top:${r.off + 1.5}px">${r.t.map(words).join("<br>")}</div>`;
        }
        el.innerHTML = html;
        vp.appendChild(el);
      });
      if (PAGE !== 2) document.getElementById("cta").remove();

      // ------------------------------------------------------------------
      // Effetti sonori: mai lo stesso due volte di fila
      // ------------------------------------------------------------------
      const SFX_LEN = { "whoosh-1": 0.6, "whoosh-2": 0.5, "whoosh-3": 0.45, "pop-1": 0.18, "pop-2": 0.16, "pop-3": 0.2, "tick-1": 0.05, "tick-2": 0.05, "tick-3": 0.05, "impact-1": 0.6 };
      const CUES = {
        1: [
          [0.0, "whoosh-1", 0.55],
          [AT[0], "tick-1", 0.5], [AT[1], "tick-2", 0.5], [AT[2], "tick-3", 0.5], [AT[3], "tick-1", 0.5], [AT[4], "tick-2", 0.5],
          [AT[5] - 0.05, "whoosh-2", 0.6], [AT[5] + 0.45, "pop-1", 0.6],
          [AT[6] - 0.05, "whoosh-3", 0.5], [AT[7], "tick-3", 0.5],
        ],
        2: [
          [0.0, "whoosh-1", 0.55],
          [AT[0], "tick-1", 0.5], [AT[1], "tick-2", 0.5], [AT[2], "tick-3", 0.5],
          [AT[3], "pop-2", 0.55], [AT[4], "pop-3", 0.45],
          [AT[5], "tick-1", 0.5],
          [CTA_AT, "whoosh-3", 0.55], [CTA_AT + 0.75, "impact-1", 0.6],
        ],
      }[PAGE];
      const sfxBox = document.getElementById("sfx");
      CUES.forEach(([t, name, vol], i) => {
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
      // Timeline (stessa animazione della versione approvata, senza scorrimento)
      // ------------------------------------------------------------------
      const tl = gsap.timeline({ paused: true });

      tl.fromTo("#waveDark", { y: -330 }, { y: 0, duration: 0.8, ease: "power3.out" }, 0);
      tl.fromTo("#waveLight", { y: -380, scaleY: 1.06 }, { y: 0, scaleY: 1, duration: 0.95, ease: "power3.out", transformOrigin: "50% 0%" }, 0.06);
      tl.fromTo("#title .ch", { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "back.out(1.8)", stagger: 0.035 }, 0.35);
      document.querySelectorAll("#giornata .gc").forEach((el, i) => {
        tl.fromTo(el, { x: -i * 13, opacity: 0 }, { x: 0, opacity: 1, duration: 0.7, ease: "power3.out" }, 0.65);
      });
      tl.fromTo("#festMark path", { scaleY: 0 }, { scaleY: 1, duration: 0.5, ease: "back.out(1.6)", stagger: 0.06 }, 0.55);
      tl.fromTo("#festTxt, #festEd", { opacity: 0, x: 18 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" }, 0.85);

      ROWS.forEach((r, i) => tl.set("#r" + i, { opacity: 0 }, 0));

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
      tl.to({}, { duration: 0.01 }, DURATION - 0.01);

      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
