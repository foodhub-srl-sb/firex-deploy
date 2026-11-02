// Dati delle giornate del Festival. Viene incollato da build.py dentro ogni video.
// y = posizione della riga nel PDF (pt), off = distanza del titolo dalla riga,
// dot = distanza del puntino dalla riga (14 se assente).
// style "a" = animazione del 9 novembre, "b" = variante del 10 novembre.
const GIORNATE = {
  "9nov": {
    style: "a",
    date: "9 NOVEMBRE",
    giornata: [["1", 61], ["ª", 87], ["G", 113], ["I", 145], ["O", 169], ["R", 202], ["N", 234], ["A", 268], ["T", 296], ["A", 326]],
    pages: {
      1: {
        rows: [
          { y: 264, k: "green", tm: "9:00-9:30", co: "SESSIONE DI APERTURA" },
          { y: 334, off: 54, tm: "9:30-10:15", co: "PIM", sp: "Nicola Marcon", t: ["“I casi studi sulla tecnologia brevettata high speed cold dryer”"] },
          { y: 468, off: 47, tm: "10:15-11:00", co: "ICONS", sp: "Sofia Francescutto", t: ["“Innovazione agroalimentare: strategie per valorizzare, conoscere e", "adottare nuove soluzioni”"] },
          { y: 634, off: 46, tm: "11:15-12:00", co: "GEA", sp: "Andrea Bresciani", t: ["“Sviluppo di nuovi prodotti: dalla materia prima al processo”"] },
          { y: 760, off: 46, tm: "12:00-12:30", co: "ALKELUX", sp: "Martina Piga", t: ["“Dal laboratorio al mercato: il percorso dell'innovazione", "nel packaging alimentare”"] },
          { y: 941, off: 46, k: "fh", tm: "12:30-13:00", co: "FOOD HUB", sp: "Francesco De Carolis", t: ["“Come usare l'AI per analizzare i prodotti sul mercato”"] },
          { y: 1088, k: "green", tm: "13:00-14:00", co: "PAUSA PRANZO", lunch: true },
          { y: 1183, off: 46, tm: "14:00-14:30", co: "KLÜBER LUBRICATION", sp: "Lorenzo Fidanza", t: ["“Implicazioni della lubrificazione nella filiera agroalimentare”"] },
        ],
        at: [1.35, 1.95, 2.55, 3.15, 3.75, 4.45, 7.0, 7.6],
        // [istante, suono, volume]; volumi ridotti del 45% rispetto alla prima versione
        cues: (AT) => [
          [0.0, "whoosh-1", 0.3],
          [AT[0], "tick-1", 0.28], [AT[1], "tick-2", 0.28], [AT[2], "tick-3", 0.28], [AT[3], "tick-1", 0.28], [AT[4], "tick-2", 0.28],
          [AT[5] - 0.05, "whoosh-2", 0.33], [AT[5] + 0.45, "pop-1", 0.33],
          [AT[6] - 0.05, "whoosh-3", 0.28], [AT[7], "tick-3", 0.28],
        ],
      },
      2: {
        cta: 5.0,
        rows: [
          { y: 264, off: 46, tm: "14:30-15:00", co: "ICONS", sp: "Marco Petazzoni; Nicoletta Gomboli", t: ["“Food Sharing Compass: piattaforma e cinque strumenti per rendere", "l’innovazione utilizzabile”"] },
          { y: 430, off: 46, tm: "15:15-16:00", co: "HOENLE", sp: "Miriam Koessler; Stefano Fantini", t: ["“Il futuro della disinfezione industriale: soluzioni UV-C per processi più sicuri”"] },
          { y: 556, off: 46, tm: "16:00-16:30", co: "OPEN FIELDS", sp: "Silvia Folloni; Gianluca Giuberti", t: ["“Amido Resistente termostabile da MAIS Italiano: MAISTAR”"] },
          { y: 690, off: 46, tm: "16:30-17:00", co: "UNIFG", sp: "Amalia Conte", t: ["“Dallo Scarto alla Shelf life: Valorizzare i Sottoprodotti per Conservare", "gli Alimenti Freschi”"] },
          { y: 855, off: 54, tm: "16:30-17:00", co: "UNIPI", sp: "Costanza Ceccanti", t: ["“Dal campo alla tavola: come il vapore sovrassaturo aiuta a conservare i", "composti nutraceutici”"] },
          { y: 1029, off: 46, tm: "17:00-17:30", co: "NSPULSE", sp: "Mirko De Leonardis; Andrea Dell’Olio", t: ["“Fermentare l’innovazione alimentare: dalla progettazione prodotto allo", "scale up industriale”"] },
        ],
        at: [1.35, 1.95, 2.55, 3.15, 3.4, 4.2],
        cues: (AT, CTA) => [
          [0.0, "whoosh-1", 0.3],
          [AT[0], "tick-1", 0.28], [AT[1], "tick-2", 0.28], [AT[2], "tick-3", 0.28],
          [AT[3], "pop-2", 0.3], [AT[4], "pop-3", 0.25],
          [AT[5], "tick-1", 0.28],
          [CTA, "whoosh-3", 0.3], [CTA + 0.75, "impact-1", 0.33],
        ],
      },
    },
  },

  "10nov": {
    style: "b",
    date: "10 NOVEMBRE",
    giornata: [["2", 61], ["ª", 92.2], ["G", 118.5], ["I", 150.5], ["O", 174.5], ["R", 207.5], ["N", 239.5], ["A", 273.5], ["T", 301.5], ["A", 331.5]],
    pages: {
      1: {
        rows: [
          { y: 264.2, dot: 13.8, k: "green", tm: "9:00-9:30", co: "SESSIONE DI APERTURA" },
          { y: 334.6, dot: 12.9, off: 46, tm: "9:30-10:15", co: "DR. SCHÄR", sp: "Silvano Ciani", t: ["“Un nuovo miglio italiano, tra nutrizione, biodiversità e sostenibilità”"] },
          { y: 460.5, dot: 10, off: 53.7, tm: "10:15-11:00", co: "ZUFFELLATO", sp: "Tatiana Pivanti", t: ["“Produzione, qualità e tracciabilità: il valore dei dati nella filiera", "agroalimentare”"] },
          { y: 633.8, dot: 11.7, off: 46, tm: "11:15-12:00", co: "HEALLO; UNITO", sp: "Alberto Ghiotto; Beatrice Maria Stella", t: ["“La nuova frontiera del food: salute metabolica e controllo della glicemia”"] },
          { y: 759.8, dot: 12.7, off: 53.9, tm: "12:00-12:30", co: "TRUSTY", sp: "Alessandro Chelli", t: ["“EUDR in pratica: dalla parcella alla DDS”"] },
          { y: 893.7, dot: 12.8, off: 46, tm: "12:30-13:00", co: "TIBI LAB", sp: "Manuela Sanseverino", t: ["“Fermentazione come piattaforma d’innovazione: dalla ricerca al", "prodotto, fino alla scala”"] },
          { y: 1059.3, dot: 12.2, k: "green", tm: "13:00-14:00", co: "PAUSA PRANZO", lunch: true },
          { y: 1153.8, dot: 11.6, off: 54, tm: "14:00-14:30", co: "GNT", sp: "Giacomo Silvetti", t: ["“Partner di fiducia per i coloring foods”"] },
        ],
        at: [1.45, 2.05, 2.65, 3.25, 3.85, 4.45, 5.15, 5.75],
        // Nuovo set: note "pizzicate" in salita, swish leggeri, bloop sul pranzo
        cues: (AT) => [
          [0.0, "swish-2", 0.22],
          [AT[0], "pluck-1", 0.2], [AT[1], "pluck-2", 0.2], [AT[2], "pluck-3", 0.2], [AT[3], "pluck-4", 0.2], [AT[4], "pluck-5", 0.2], [AT[5], "pluck-6", 0.18],
          [AT[6], "bloop-1", 0.25],
          [AT[7], "pluck-4", 0.2],
        ],
      },
      2: {
        cta: 4.4,
        rows: [
          { y: 264.2, dot: 14, off: 45.7, tm: "14:30-15:00", co: "UNIBAS", sp: "Giorgia La Rocca", t: ["“Strumenti biologici per efficienza energetica e sostenibilità nella", "produzione vinicola”"] },
          { y: 429.7, dot: 12.8, off: 46, tm: "15:15-16:00", co: "CNR", sp: "Marco Montemurro", t: ["“Produzione, caratterizzazione e valorizzazione di prodotti innovativi a", "base di canapa (HREMPRO)”"] },
          { y: 595.3, dot: 14.2, off: 46, tm: "16:00-16:30", co: "UNIFI", sp: "Tommaso Ugolini", t: ["“Chemometria e analisi chimica e sensoriale per caratterizzare oli EVO", "monovarietali italiani”"] },
          { y: 768.7, dot: 13.8, off: 46, tm: "16:00-16:30", co: "UNISS", sp: "Severino Zara", t: ["“Dalla buccia di melograno a una risorsa: composti antimicrobici per la", "sicurezza alimentare”"] },
          { y: 934, dot: 14.4, off: 46.3, tm: "16:30-17:00", co: "Cristian Panarelli", nameOnly: true, t: ["“Il ruolo dell’intelligenza artificiale nell’etichettatura”"] },
        ],
        at: [1.45, 2.05, 2.65, 2.85, 3.55],
        cues: (AT, CTA) => [
          [0.0, "swish-2", 0.22],
          [AT[0], "pluck-1", 0.2], [AT[1], "pluck-3", 0.2],
          [AT[2], "pluck-4", 0.2], [AT[3], "pluck-5", 0.16],
          [AT[4], "pluck-6", 0.18],
          [CTA, "swish-1", 0.25], [CTA + 0.8, "chime-1", 0.22],
        ],
      },
    },
  },
};
