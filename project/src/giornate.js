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

  "11nov": {
    style: "c",
    date: "11 NOVEMBRE",
    giornata: [["3", 61], ["ª", 92.2], ["G", 118.5], ["I", 150.5], ["O", 174.5], ["R", 207.5], ["N", 239.5], ["A", 273.5], ["T", 301.5], ["A", 331.5]],
    dx: -45.5, // colonna spostata a sinistra rispetto al 9 e 10 novembre
    dash: {
      1: { start: -7.25, period: 25.45, len: 12.5, end: 81.6 },
      2: { start: -5.35, period: 24.75, len: 12.3, end: 81.1 },
    },
    fhBlob: { left: 6.43, top: -38.8, w: 827.8, h: 158.2 },
    fhLogo: { left: 17.3, top: 0.5, size: 100.5 },
    cta: {
      top: 1202.03,
      lblLeft: 139.9,
      band: "M821.37 1266.63L0.37 1266.63L0.37 1197.63L880.62 1197.63C883.31 1197.63 885.50 1199.81 885.50 1202.50C885.50 1237.92 856.78 1266.63 821.37 1266.63",
    },
    pages: {
      1: {
        rows: [
          { y: 264.2, dot: 13.8, k: "green", tm: "9:00-9:30", co: "SESSIONE DI APERTURA" },
          { y: 349.4, dot: -1.9, off: 46.1, tm: "9:30-10:15", co: "ZESPRI INNOVATION", sp: "Marco Mastroleo", t: ["“Zespri DSS: l'innovazione e i modelli alla portata di tutti”"] },
          { y: 475.7, dot: 13.8, off: 46, tm: "10:15-11:00", co: "HERBSTREITH & FOX", sp: "Luca Bianucci; Marco C. Roffia", t: ["“Valorizzazione di derivati della mela: fibre ed estratti per nuove", "applicazioni alimentari”"] },
          { y: 640.8, off: 46, k: "fh", tm: "11:00-11:30", co: "FOOD HUB", sp: "Francesco De Carolis", t: ["“Food Hub: AI x Food Industry”"] },
          { y: 773.7, dot: 16.8, off: 45.8, tm: "11:45-12:15", co: "KLÜBER LUBRICATION", sp: "Andrea Marotta", t: ["“Lubrificanti food grade: una leva per sicurezza, efficienza e affidabilità", "degli impianti”"] },
          { y: 936.9, dot: 16.5, off: 46, tm: "12:15-13:00", co: "KAMUT ENTERPRISES OF EUROPE", sp: "Emanuela Simonetti", t: ["“40 anni di tutela e valorizzazione di un antico cereale dalla terra alla tavola”"] },
          { y: 1064.3, dot: 13.2, k: "green", tm: "13:00-14:00", co: "PAUSA PRANZO", lunch: true },
          { y: 1148.5, dot: 13.9, off: 46.3, tm: "14:00-14:30", co: "TRUSTY", sp: "Alessandro Chelli", t: ["“Il tuo brand è sulla confezione? Allora la Dichiarazione di Conformità", "PPWR la firmi tu”"] },
        ],
        at: [1.5, 2.1, 2.7, 3.4, 5.7, 6.3, 6.9, 7.5],
        // Set C: fogli che si girano, scintillio su Food Hub, goccia sul pranzo
        cues: (AT) => [
          [0.0, "riser-1", 0.2],
          [AT[0], "flip-1", 0.22], [AT[1], "flip-2", 0.22], [AT[2], "flip-3", 0.22],
          [AT[3] + 0.2, "shimmer-1", 0.2],
          [AT[4], "flip-1", 0.22], [AT[5], "flip-2", 0.22],
          [AT[6], "drop-1", 0.22],
          [AT[7], "flip-3", 0.22],
        ],
      },
      2: {
        cta: 4.5,
        rows: [
          { y: 264.2, dot: 13.9, off: 46.2, tm: "14:45-15:30", co: "MV CONSULTING", sp: "Marco Valerio Francone", t: ["“Strumenti di Intelligenza Artificiale applicati alla Qualità Aziendale”"] },
          { y: 390.4, dot: 14.2, off: 46, tm: "15:30-16:00", co: "UNIPD", sp: "Piergiorgio Stevanato", t: ["“Zucchero biologico italiano: innovazione dal seme alla filiera”"] },
          { y: 516.3, dot: 13.2, off: 45.8, tm: "15:30-16:00", co: "UNISS", sp: "Grazia Maria Scarpa", t: ["“Il settore delle piante officinali: qualità della filiera e valorizzazione", "del prodotto”"] },
          { y: 689.8, dot: 12.7, off: 46, tm: "16:00-16:30", co: "UNICT", sp: "Chiara Pisana", t: ["“Packaging attivo con proteine del siero per il controllo di Listeria nel", "Canestrato Siciliano”"] },
          { y: 855.3, dot: 13.2, off: 46, tm: "16:30-17:00", co: "Progetto HAMTRACE", sp: "Leonardo Piccinetti", t: ["“Presentazione del progetto HAMTRACE”"] },
        ],
        at: [1.5, 2.1, 2.3, 3.05, 3.65], // UNIPD e UNISS quasi insieme: sono parallele
        cues: (AT, CTA) => [
          [0.0, "riser-1", 0.2],
          [AT[0], "flip-1", 0.22], [AT[1], "flip-2", 0.22], [AT[2], "flip-3", 0.18],
          [AT[3], "flip-1", 0.22], [AT[4], "flip-2", 0.22],
          [CTA, "riser-1", 0.2], [CTA + 0.95, "ding-1", 0.2],
        ],
      },
    },
  },

  "12nov": {
    style: "d",
    date: "12 NOVEMBRE",
    giornata: [["4", 61], ["ª", 92.5], ["G", 142], ["I", 174], ["O", 198], ["R", 231], ["N", 263.1], ["A", 297], ["T", 325.1], ["A", 355.2]],
    dash: {
      1: { start: 12.7, period: 25.5, len: 12.5, end: 50.6 },
      2: { start: -11.9, period: 24.9, len: 12.4, end: 50.2 },
    },
    cta: {
      top: 1197.13,
      lblLeft: 89.0,
      band: "M759.17 1266.63L0.37 1266.63L0.37 1197.63L818.42 1197.63C821.11 1197.63 823.30 1199.81 823.30 1202.50C823.30 1237.92 794.58 1266.63 759.17 1266.63",
    },
    pages: {
      1: {
        dx: -76.5,
        rows: [
          { y: 264.2, dot: 12.8, k: "green", tm: "9:00-9:30", co: "SESSIONE DI APERTURA" },
          { y: 349.4, dot: 12.1, off: 46.1, tm: "9:30-10:15", co: "WISESIDE; GRUPPO MARTINI", sp: "Pinuccia Zarino; Cristina Moretti", t: ["“Quante filiere ci sono dentro una filiera?”"] },
          { y: 475.7, dot: 11.8, off: 46, tm: "10:15-11:00", co: "AQUAPONIC DESIGN", sp: "Francesco Lombardo", t: ["“ROBOPONIC: tecnologia e competenze per coltivare il futuro”"] },
          { y: 601.6, dot: 11.9, off: 46.1, tm: "11:15-11:45", co: "MIREA-COSVITEC", sp: "Fracesca Luisa Fedele", t: ["“Il valore nascosto degli scarti: Dalla ricerca all’industria”"] },
          { y: 727.9, dot: 10.6, off: 46, tm: "11:45-12:30", co: "HIDEEA", sp: "Laura Magni; Giacomo Paolini", t: ["“Compliance PPWR: il futuro del packaging tra MOCA e certificazioni food”"] },
          { y: 853.9, dot: 11.6, off: 46.2, tm: "12:30-13:00", co: "UNIPV", sp: "Alma Balestrazzi", t: ["“Orphan legumes, sicurezza alimentare e clima: la strategia del progetto PROSPER”"] },
          { y: 980.1, dot: 15.3, k: "green", tm: "13:00-14:00", co: "PAUSA PRANZO", lunch: true },
          { y: 1066.5, dot: 12, off: 46, tm: "14:00-14:45", co: "FRESH4CAST", sp: "Michele Dall’Olio", t: ["“Previsione, pianificazione e S&amp;OP: il nuovo motore decisionale per il food”"] },
          { y: 1192.7, dot: 12.7, off: 46, tm: "14:45-15:15", co: "UNITO", sp: "Amedeo Reyneri", t: ["“Agricoltura rigenerativa e produzione di cereali senza residui di fitosanitari”"] },
        ],
        at: [1.45, 2.0, 2.55, 3.1, 3.65, 4.2, 4.8, 5.35, 5.9],
        // Set D: kalimba alternata, soffio d'aria iniziale, bollicina sul pranzo
        cues: (AT) => [
          [0.0, "air-1", 0.22],
          [AT[0], "kal-1", 0.2], [AT[1], "kal-2", 0.2], [AT[2], "kal-3", 0.2], [AT[3], "kal-4", 0.2], [AT[4], "kal-2", 0.2], [AT[5], "kal-3", 0.2],
          [AT[6], "bubble-1", 0.22],
          [AT[7], "kal-1", 0.2], [AT[8], "kal-4", 0.2],
        ],
      },
      2: {
        dx: -77.5,
        cta: 4.2,
        rows: [
          { y: 264.2, dot: 14, off: 46.3, tm: "15:15-15:45", co: "SFRIDOO", sp: "Mario Lazzaroni; Roberta Scassa", t: ["“Da scarto a sottoprodotto: normativa, valore e compliance per", "l’economia circolare”"] },
          { y: 429.8, dot: 10.9, off: 46, tm: "15:45-16:30", co: "UNIMI", sp: "Elisa De Marchi", t: ["“FRAME - Food Resilience through Architecturally Modelled", "Environments”"] },
          { y: 595.4, dot: 14.3, off: 46, tm: "16:30-17:00", co: "UNITO- DISAFA", sp: "Silvia Celletti", t: ["“Bioplastiche in agricoltura: innovazione sostenibile per il suolo e le", "filiere agroalimentari”"] },
          { y: 769.9, dot: 12.7, off: 46, tm: "16:30-17:00", co: "UNIVE", sp: "Giulia Bertazzoli", t: ["“Biorisorse microbiche, un potenziale per il settore agro-alimentare”"] },
          { y: 894.9, dot: 12.7, off: 49.1, tm: "17:00-17:30", co: "UNIMI", sp: "Barbara Scaglia", t: ["“Valorizzazione degli scarti di prima gamma: il caso di ZUcca e PORro", "(progetto ZUPOR)”"] },
        ],
        at: [1.45, 2.0, 2.55, 2.75, 3.4], // UNITO-DISAFA e UNIVE quasi insieme: sono parallele
        cues: (AT, CTA) => [
          [0.0, "air-1", 0.22],
          [AT[0], "kal-1", 0.2], [AT[1], "kal-2", 0.2],
          [AT[2], "kal-3", 0.2], [AT[3], "kal-4", 0.16],
          [AT[4], "kal-2", 0.2],
          [CTA, "swell-1", 0.22], [CTA + 0.7, "bell-2", 0.2],
        ],
      },
    },
  },
};
