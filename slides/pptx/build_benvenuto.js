// Costruisce slides/benvenuto.pptx (stesso contenuto e stile di benvenuto.html).
// Uso: NODE_PATH=<cartella con pptxgenjs e sharp> node slides/pptx/build_benvenuto.js
//   python3 slides/pptx/export_assets.py   (prima, per generare deck.json e gli SVG)
// Variabili: SKILL_DIR = cartella della skill pptx (per apply_theme.js)
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const sharp = require("sharp");
const JSZip = require("jszip");

const HERE = __dirname;
const BUILD = path.join(HERE, "build");
const OUT = path.resolve(HERE, "..", "benvenuto.pptx");
const SKILL_DIR = process.env.SKILL_DIR;
const deck = JSON.parse(fs.readFileSync(path.join(BUILD, "deck.json"), "utf8"));
const labels = JSON.parse(fs.readFileSync(path.join(BUILD, "labels.json"), "utf8"));
const LOGO = path.resolve(HERE, "..", "foodhub-logo.png");

// ---------- Tema (colori dal logo Food Hub) ----------
const THEME = {
  name: "ChallengEat 8",
  headFontFace: "Arial",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "2A1E22", lt1: "FFFFFF", dk2: "4A3F42", lt2: "FBF6F1",
    accent1: "D3134A", accent2: "F4A269", accent3: "48B17A",
    accent4: "FCE8DA", accent5: "A80F3B", accent6: "2E7D53",
    hlink: "D3134A", folHlink: "A80F3B",
  },
};
const HEX = { line: "EADFD6", muted: "8A7F82", lightText: "EBDCD3" };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333" x 7.5"
pres.title = deck.title;
pres.author = "Food Hub";
pres.company = "Food Hub";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const W = 13.333, H = 7.5, L = 0.89, CW = 11.553;
const CYCLE = [C.accent1, C.accent2, C.accent3];

// ---------- Utilità ----------
function runs(html, opts = {}, emColor) {
  // <b>..</b> grassetto, <em>..</em> colore di accento
  const out = [];
  let bold = false, em = false;
  for (const part of html.split(/(<\/?b>|<\/?em>)/)) {
    if (part === "<b>") bold = true;
    else if (part === "</b>") bold = false;
    else if (part === "<em>") em = true;
    else if (part === "</em>") em = false;
    else if (part) {
      const o = { ...opts };
      if (bold) o.bold = true;
      if (em) { o.color = emColor || C.accent1; o.bold = true; }
      out.push({ text: part, options: o });
    }
  }
  return out;
}

function paragraphs(items, base, bulletOpts, emColor) {
  // una lista di paragrafi con punti elenco; ogni voce può contenere <b> e <em>
  const out = [];
  items.forEach((html, i) => {
    const rs = runs(html, { ...base }, emColor);
    rs.forEach((r, j) => {
      if (j === 0 && bulletOpts) r.options.bullet = bulletOpts;
      if (j === 0) r.options.paraSpaceAfter = base.paraSpaceAfter;
      if (j === rs.length - 1 && i < items.length - 1) r.options.breakLine = true;
    });
    out.push(...rs);
  });
  return out;
}

const shadow = () => ({ type: "outer", color: "000000", blur: 8, offset: 2, angle: 90, opacity: 0.12 });

function card(slide, x, y, w, h, name) {
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.12, fill: { color: C.lt1 === undefined ? "FFFFFF" : "FFFFFF" },
    line: { color: HEX.line, width: 1 }, shadow: shadow(), objectName: name,
  });
}

function band(slide, html, y) {
  slide.addShape(pres.ShapeType.roundRect, {
    x: L, y, w: CW, h: 0.62, rectRadius: 0.1, fill: { color: C.accent4 }, line: { color: C.accent4, width: 0 },
    objectName: "Nota",
  });
  slide.addText(runs(html, { fontSize: 16, color: C.text1 }), {
    x: L + 0.25, y, w: CW - 0.5, h: 0.62, valign: "middle", margin: 0, isTextBox: true, objectName: "Testo nota",
  });
}

async function png(name, sizePx) {
  const svg = fs.readFileSync(path.join(BUILD, "svg", name + ".svg"));
  const buf = await sharp(svg, { density: 300 }).resize(sizePx, sizePx).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

function image(slide, data, x, y, w, h, alt, name) {
  slide.addImage({ data, x, y, w, h, altText: alt, objectName: name });
}

function footerLayout() {
  return [
    { image: { x: L, y: 6.93, w: 0.34, h: 0.34, path: LOGO, altText: "Logo Food Hub" } },
    { text: { text: "ChallengEat 8 · " + deck.short, options: { x: L + 0.45, y: 6.93, w: 5, h: 0.34, fontSize: 12, color: C.text2, valign: "middle", margin: 0 } } },
  ];
}

// ---------- Layout (cornici) ----------
const titlePh = (extra = {}) => ({
  placeholder: {
    options: Object.assign({ name: "title", type: "title", x: L, y: 0.55, w: CW, h: 0.95, fontSize: 36, bold: true, color: C.text1, margin: 0, valign: "middle", align: "left" }, extra),
    text: "",
  },
});

pres.defineSlideMaster({
  title: "CONTENUTO", background: { color: C.background2 },
  objects: [titlePh(), ...footerLayout()],
  slideNumber: { x: W - L - 1.5, y: 6.93, w: 1.5, h: 0.34, fontSize: 12, color: C.text2, align: "right" },
});
pres.defineSlideMaster({
  title: "COPERTINA", background: { color: C.background2 },
  objects: [titlePh({ x: L, y: 2.2, w: 6.5, h: 2.1, fontSize: 54, valign: "top" })],
});
pres.defineSlideMaster({
  title: "SEZIONE", background: { color: C.accent1 },
  objects: [
    { placeholder: { options: { name: "num", type: "body", x: L, y: 2.15, w: 3, h: 0.5, fontSize: 20, bold: true, color: C.accent4, margin: 0, charSpacing: 4 }, text: "" } },
    titlePh({ x: L, y: 2.7, w: 7.6, h: 2.8, fontSize: 72, color: C.background1, valign: "top" }),
    { text: { text: "ChallengEat 8 · " + deck.short, options: { x: L, y: 6.93, w: 5, h: 0.34, fontSize: 12, color: C.accent4, valign: "middle", margin: 0 } } },
  ],
});
pres.defineSlideMaster({
  title: "SCURO", background: { color: C.text1 },
  objects: [],
});
pres.defineSlideMaster({
  title: "CHIUSURA", background: { color: C.background2 },
  objects: [titlePh({ x: L, y: 3.15, w: CW, h: 1.2, fontSize: 54, align: "center", valign: "middle" })],
});


// pptxgenjs scrive un <a:pPr> prima di ogni run: nei paragrafi con più run (grassetto, accenti)
// quelli successivi al primo sono fuori posto e annullano il punto elenco. Teniamo solo il primo.
async function fixParagraphProps(file) {
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const pPr = /<a:pPr\b[^>]*?(?:\/>|>[\s\S]*?<\/a:pPr>)/g;
  for (const name of Object.keys(zip.files).filter((n) => /^ppt\/slides\/slide\d+\.xml$/.test(n))) {
    const xml = await zip.file(name).async("string");
    const fixed = xml.replace(/<a:p>[\s\S]*?<\/a:p>/g, (para) => {
      let seen = 0;
      return para.replace(pPr, (m) => (seen++ === 0 ? m : ""));
    });
    zip.file(name, fixed);
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

// ---------- Costruzione ----------
const SECTIONS = [
  ["Apertura", 0], ["Il percorso", 1], ["Calendario", 4], ["Lavoro in gruppo", 7], ["La piattaforma", 12], ["Il valore del percorso", 15],
];

(async () => {
  const IMG = {};
  for (const n of ["team", "puzzle", "devices", "routing"]) IMG[n] = await png(n, 1100);
  // decorazione delle slide di sezione: ritaglio della parte visibile
  {
    const svg = fs.readFileSync(path.join(BUILD, "svg", "deco.svg"));
    const full = await sharp(svg, { density: 300 }).resize(1800, 1800).png().toBuffer();
    const buf = await sharp(full).extract({ left: 0, top: 0, width: 1440, height: 1359 }).png().toBuffer();
    IMG.deco = "image/png;base64," + buf.toString("base64");
  }

  deck.slides.forEach((s, idx) => {
    const sec = SECTIONS.find(([, i]) => i === idx);
    if (sec) pres.addSection({ title: sec[0] });
    const sectionTitle = [...SECTIONS].reverse().find(([, i]) => i <= idx)[0];
    const k = s.type;

    if (k === "cover") {
      const slide = pres.addSlide({ masterName: "COPERTINA", sectionTitle });
      slide.addImage({ path: LOGO, x: L, y: 0.7, w: 0.75, h: 0.75, altText: "Logo Food Hub", objectName: "Logo" });
      slide.addText("CHALLENGEAT 8 · EDIZIONE 2026", { x: L, y: 1.75, w: 6.5, h: 0.4, fontSize: 14, bold: true, color: C.accent1, charSpacing: 3, margin: 0, isTextBox: true, objectName: "Sopratitolo" });
      slide.addText(s.title, { placeholder: "title" });
      slide.addText(s.subtitle, { x: L, y: 4.45, w: 6.4, h: 1.0, fontSize: 24, color: C.text2, valign: "top", margin: 0, isTextBox: true, objectName: "Sottotitolo" });
      slide.addShape(pres.ShapeType.roundRect, { x: L, y: 5.7, w: 3.7, h: 0.5, rectRadius: 0.25, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, objectName: "Etichetta date" });
      slide.addText(s.date, { x: L, y: 5.7, w: 3.7, h: 0.5, fontSize: 14, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Testo date" });
      slide.addShape(pres.ShapeType.roundRect, { x: L + 3.9, y: 5.7, w: 1.9, h: 0.5, rectRadius: 0.25, fill: { color: C.accent4 }, line: { color: C.accent4, width: 0 }, objectName: "Etichetta durata" });
      slide.addText(s.duration, { x: L + 3.9, y: 5.7, w: 1.9, h: 0.5, fontSize: 14, bold: true, color: C.accent5, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Testo durata" });
      image(slide, IMG[s.illus], 7.55, 1.2, 4.9, 4.9, labels[s.illus], "Illustrazione");
      slide.addText(runs(`${s.mentor_label}: <b>Food Hub</b>`, { fontSize: 14, color: C.text2 }), { x: L, y: 6.75, w: 8, h: 0.35, margin: 0, isTextBox: true, objectName: "A cura di" });
      slide.addNotes("Benvenuto ai partecipanti: presentiamo il percorso, il calendario e il modo di lavorare insieme.");
    }

    else if (k === "section") {
      const slide = pres.addSlide({ masterName: "SEZIONE", sectionTitle });
      slide.addImage({ data: IMG.deco, x: 8.333, y: 2.78, w: 5.0, h: 4.72, altText: "", objectName: "Decorazione" });
      slide.addText(s.num, { placeholder: "num" });
      slide.addText(s.title, { placeholder: "title" });
    }

    else if (k === "content") {
      const slide = pres.addSlide({ masterName: "CONTENUTO", sectionTitle });
      slide.addText(s.title, { placeholder: "title" });
      const left = s.side === "left";
      const ix = left ? L : W - L - 4.2;
      const tx = left ? L + 4.2 + 0.5 : L;
      const tw = CW - 4.2 - 0.5;
      image(slide, IMG[s.illus], ix, 2.05, 4.2, 4.2, labels[s.illus], "Illustrazione");
      slide.addText(
        paragraphs(s.bullets, { fontSize: 20, color: C.text1, paraSpaceAfter: 12 }, { indent: 20 }),
        { x: tx, y: 1.85, w: tw, h: 4.7, valign: "middle", margin: 0, isTextBox: true, objectName: "Elenco" }
      );
    }

    else if (k === "cards") {
      const slide = pres.addSlide({ masterName: "CONTENUTO", sectionTitle });
      slide.addText(s.title, { placeholder: "title" });
      const n = s.cards.length, gap = 0.4, cw = (CW - gap * (n - 1)) / n, cy = 1.8, ch = 3.85;
      s.cards.forEach((c, i) => {
        const x = L + i * (cw + gap);
        card(slide, x, cy, cw, ch, "Card " + (i + 1));
        slide.addText(c.tag.toUpperCase(), { x: x + 0.3, y: cy + 0.22, w: cw - 0.6, h: 0.3, fontSize: 12, bold: true, color: CYCLE[i % 3] === C.accent2 ? C.accent5 : (CYCLE[i % 3] === C.accent3 ? C.accent6 : C.accent1), charSpacing: 2, margin: 0, isTextBox: true });
        slide.addText(c.title, { x: x + 0.3, y: cy + 0.55, w: cw - 0.6, h: 0.5, fontSize: 24, bold: true, color: C.text1, margin: 0, isTextBox: true });
        slide.addText(paragraphs(c.bullets, { fontSize: 18, color: C.text1, paraSpaceAfter: 8 }, { indent: 18 }), {
          x: x + 0.3, y: cy + 1.15, w: cw - 0.6, h: ch - 1.35, valign: "top", margin: 0, isTextBox: true, objectName: "Elenco card " + (i + 1),
        });
      });
      if (s.note) band(slide, s.note, 5.95);
    }

    else if (k === "timeline") {
      const slide = pres.addSlide({ masterName: "CONTENUTO", sectionTitle });
      slide.addText(s.title, { placeholder: "title" });
      const n = s.weeks.length, gap = 0.25, cw = (CW - gap * (n - 1)) / n;
      slide.addShape(pres.ShapeType.line, { x: L + 0.15, y: 2.3, w: CW - 0.3, h: 0, line: { color: HEX.line, width: 3 }, objectName: "Linea del tempo" });
      s.weeks.forEach((w, i) => {
        const x = L + i * (cw + gap);
        slide.addShape(pres.ShapeType.ellipse, { x, y: 2.15, w: 0.3, h: 0.3, fill: { color: CYCLE[i % 3] }, line: { color: C.background2, width: 3 }, objectName: "Punto settimana " + w.n });
        slide.addText("SETTIMANA " + w.n, { x, y: 2.65, w: cw, h: 0.3, fontSize: 12, bold: true, color: C.accent1, charSpacing: 1, margin: 0, isTextBox: true });
        slide.addText(w.date, { x, y: 2.95, w: cw, h: 0.3, fontSize: 12, color: C.text2, margin: 0, isTextBox: true });
        slide.addText(w.phase, { x, y: 3.3, w: cw, h: 0.75, fontSize: 18, bold: true, color: C.text1, valign: "top", margin: 0, isTextBox: true });
        slide.addText(paragraphs(w.out, { fontSize: 14, color: C.text1, paraSpaceAfter: 6 }, { indent: 14 }), {
          x, y: 4.15, w: cw, h: 2.3, valign: "top", margin: 0, isTextBox: true, objectName: "Elenco settimana " + w.n,
        });
      });
    }

    else if (k === "calendar") {
      const slide = pres.addSlide({ masterName: "CONTENUTO", sectionTitle });
      slide.addText(s.title, { placeholder: "title" });
      const n = s.weeks.length, gap = 0.22, cw = (CW - gap * (n - 1)) / n, cy = 1.75, ch = 4.25;
      s.weeks.forEach((w, i) => {
        const x = L + i * (cw + gap);
        card(slide, x, cy, cw, ch, "Settimana " + w.n);
        slide.addText("SETTIMANA " + w.n, { x: x + 0.18, y: cy + 0.15, w: cw - 0.36, h: 0.3, fontSize: 12, bold: true, color: C.accent1, charSpacing: 1, margin: 0, isTextBox: true });
        slide.addText(w.phase, { x: x + 0.18, y: cy + 0.48, w: cw - 0.36, h: 0.45, fontSize: 16, bold: true, color: C.text1, margin: 0, valign: "top", isTextBox: true });
        slide.addShape(pres.ShapeType.roundRect, { x: x + 0.15, y: cy + 1.05, w: cw - 0.3, h: 1.45, rectRadius: 0.1, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, objectName: "Martedì " + w.n });
        slide.addText([
          { text: "Martedì", options: { fontSize: 12, bold: true, color: C.accent4, breakLine: true } },
          { text: w.tue, options: { fontSize: 18, bold: true, color: C.background1, breakLine: true } },
          { text: s.tue_time, options: { fontSize: 14, bold: true, color: C.background1, breakLine: true } },
          { text: s.tue_label, options: { fontSize: 12, color: C.background1 } },
        ], { x: x + 0.28, y: cy + 1.05, w: cw - 0.56, h: 1.45, valign: "middle", margin: 0, isTextBox: true, objectName: "Testo martedì " + w.n });
        slide.addShape(pres.ShapeType.roundRect, { x: x + 0.15, y: cy + 2.65, w: cw - 0.3, h: 1.45, rectRadius: 0.1, fill: { color: C.accent4 }, line: { color: C.accent4, width: 0 }, objectName: "Venerdì " + w.n });
        slide.addText([
          { text: "Venerdì", options: { fontSize: 12, bold: true, color: C.accent5, breakLine: true } },
          { text: w.fri, options: { fontSize: 18, bold: true, color: C.text1, breakLine: true } },
          { text: s.fri_time, options: { fontSize: 14, bold: true, color: C.text1, breakLine: true } },
          { text: s.fri_label, options: { fontSize: 12, color: C.text1 } },
        ], { x: x + 0.28, y: cy + 2.65, w: cw - 0.56, h: 1.45, valign: "middle", margin: 0, isTextBox: true, objectName: "Testo venerdì " + w.n });
      });
      band(slide, s.note, 6.15);
    }

    else if (k === "steps") {
      const slide = pres.addSlide({ masterName: "CONTENUTO", sectionTitle });
      slide.addText(s.title, { placeholder: "title" });
      const cols = 3, gap = 0.22, cw = (CW - gap * (cols - 1)) / cols, ch = 2.1;
      s.steps.forEach((t, i) => {
        const x = L + (i % cols) * (cw + gap), y = 1.85 + Math.floor(i / cols) * (ch + 0.25);
        card(slide, x, y, cw, ch, "Passo " + (i + 1));
        slide.addText(String(i + 1), { x: x + 0.25, y, w: 0.7, h: ch, fontSize: 40, bold: true, color: C.accent1, valign: "middle", margin: 0, isTextBox: true });
        slide.addText(runs(t, { fontSize: 18, color: C.text1 }), { x: x + 1.0, y: y + 0.15, w: cw - 1.25, h: ch - 0.3, valign: "middle", margin: 0, isTextBox: true, objectName: "Testo passo " + (i + 1) });
      });
    }

    else if (k === "routing") {
      const slide = pres.addSlide({ masterName: "CONTENUTO", sectionTitle });
      slide.addText(s.title, { placeholder: "title" });
      const fills = [C.accent1, C.accent2, C.accent6], txt = [C.background1, C.text1, C.background1];
      s.rows.forEach((r, i) => {
        const y = 2.0 + i * 1.2;
        slide.addShape(pres.ShapeType.roundRect, { x: L, y, w: 2.9, h: 0.85, rectRadius: 0.12, fill: { color: fills[i] }, line: { color: fills[i], width: 0 }, objectName: "Chi " + (i + 1) });
        slide.addText(r.who, { x: L + 0.2, y, w: 2.5, h: 0.85, fontSize: 18, bold: true, color: txt[i], valign: "middle", margin: 0, isTextBox: true });
        slide.addShape(pres.ShapeType.rightArrow, { x: L + 3.05, y: y + 0.28, w: 0.45, h: 0.3, fill: { color: HEX.line }, line: { color: HEX.line, width: 0 }, objectName: "Freccia " + (i + 1) });
        slide.addText(r.what, { x: L + 3.7, y, w: 4.3, h: 0.85, fontSize: 16, color: C.text1, valign: "middle", margin: 0, isTextBox: true, objectName: "Per cosa " + (i + 1) });
      });
      image(slide, IMG[s.illus], W - L - 3.7, 1.95, 3.7, 3.7, labels[s.illus], "Illustrazione");
      if (s.note) band(slide, s.note, 5.95);
    }

    else if (k === "statement") {
      const slide = pres.addSlide({ masterName: "SCURO", sectionTitle });
      slide.addShape(pres.ShapeType.ellipse, { x: 10.6, y: -1.1, w: 3.9, h: 3.9, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, objectName: "Decorazione magenta" });
      slide.addShape(pres.ShapeType.ellipse, { x: 9.9, y: 1.95, w: 0.8, h: 0.8, fill: { color: C.accent2 }, line: { color: C.accent2, width: 0 }, objectName: "Decorazione arancio" });
      slide.addText((s.eyebrow || "La sfida").toUpperCase(), { x: 1.1, y: 1.35, w: 8, h: 0.4, fontSize: 14, bold: true, color: C.accent2, charSpacing: 3, margin: 0, isTextBox: true });
      slide.addText(runs(s.question, { fontSize: 36, bold: true, color: C.background1 }, C.accent2), { x: 1.1, y: 1.85, w: 8.6, h: 2.2, valign: "top", margin: 0, isTextBox: true, objectName: "Frase chiave" });
      slide.addText(paragraphs(s.bullets, { fontSize: 18, color: HEX.lightText, paraSpaceAfter: 10 }, { indent: 18 }), { x: 1.1, y: 4.2, w: 9.6, h: 2.5, valign: "top", margin: 0, isTextBox: true, objectName: "Elenco" });
    }

    else if (k === "closing") {
      const slide = pres.addSlide({ masterName: "CHIUSURA", sectionTitle });
      slide.addImage({ path: LOGO, x: (W - 1.25) / 2, y: 1.55, w: 1.25, h: 1.25, altText: "Logo Food Hub", objectName: "Logo" });
      slide.addText(s.title, { placeholder: "title" });
      slide.addText(s.subtitle, { x: L, y: 4.5, w: CW, h: 0.5, fontSize: 22, color: C.text2, align: "center", margin: 0, isTextBox: true });
      slide.addText(s.meta, { x: L, y: 5.15, w: CW, h: 0.4, fontSize: 14, color: C.text2, align: "center", margin: 0, isTextBox: true });
    }
  });

  await pres.writeFile({ fileName: OUT });
  if (SKILL_DIR) {
    const { applyTheme } = require(path.join(SKILL_DIR, "scripts", "apply_theme.js"));
    await applyTheme(OUT, THEME);
  }
  await fixParagraphProps(OUT);
  console.log("scritto", OUT);
})();
