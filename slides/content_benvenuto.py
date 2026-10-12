"""Contenuti delle slide di benvenuto ChallengEat 8 (valide per tutti i gruppi)."""

M, O, G = "#D3134A", "#E07F3C", "#2E9B63"

DECK = {
    "title": "ChallengEat 8 · Benvenuto",
    "short": "Benvenuto",
    "slides": [
        {
            "type": "cover",
            "title": "Benvenuti in ChallengEat 8",
            "subtitle": "Il percorso, il calendario e il modo di lavorare insieme",
            "date": "12 ottobre · 16 novembre 2026",
            "duration": "5 settimane",
            "mentor_label": "A cura di",
            "mentors": ["<b>Food Hub</b>"],
            "illus": "team",
        },
        {"type": "section", "num": "01", "title": "Il percorso"},
        {
            "type": "cards",
            "title": "Due sfide, cinque gruppi",
            "cards": [
                {
                    "tag": "Sfida 1",
                    "title": "Naturitalia",
                    "bullets": [
                        "Tracciabilità e interoperabilità nella filiera del kiwi",
                        "Il viaggio di prodotto e confezione, dal campo allo scaffale",
                        "Un linguaggio comune per i dati di filiera",
                        "Mentor: Greta Gubellini e Andrea Severi",
                    ],
                },
                {
                    "tag": "Sfida 2",
                    "title": "RAGO",
                    "bullets": [
                        "Tracciabilità e sicurezza alimentare nella IV gamma",
                        "La temperatura da dato registrato a decisione in tempo reale",
                        "Shelf-life residua e accettazione della merce",
                        "Mentor: Giuseppe Esposito",
                    ],
                },
            ],
            "note": "<b>25 partecipanti, 5 gruppi da 5 persone</b> con competenze complementari: tre gruppi lavorano su una sfida, due sull'altra.",
        },
        {
            "type": "timeline",
            "title": "Cinque settimane, cinque tappe",
            "weeks": [
                {"n": 1, "date": "12 · 18 ottobre", "phase": "Gap analysis e mappatura", "out": [
                    "La mappa della filiera",
                    "Dove si perde l'informazione",
                ]},
                {"n": 2, "date": "19 · 25 ottobre", "phase": "Benchmark tecnologico", "out": [
                    "Le soluzioni possibili a confronto",
                    "Una scelta motivata",
                ]},
                {"n": 3, "date": "26 ottobre · 1 novembre", "phase": "Modello di soluzione", "out": [
                    "La vostra proposta",
                    "Regole, ruoli e accesso ai dati",
                ]},
                {"n": 4, "date": "2 · 8 novembre", "phase": "Piano pilota e KPI", "out": [
                    "Un pilota concreto",
                    "Indicatori e costi",
                ]},
                {"n": 5, "date": "9 · 16 novembre", "phase": "Presentazione finale", "out": [
                    "Preparazione della presentazione",
                    "<b>16 novembre</b>: presentazione finale",
                ]},
            ],
        },
        {"type": "section", "num": "02", "title": "Calendario"},
        {
            "type": "cards",
            "title": "Due appuntamenti a settimana",
            "cards": [
                {
                    "tag": "Martedì",
                    "title": "Sessione condivisa, 1 ora",
                    "bullets": [
                        "Dalle 17:30 alle 18:30, tutti insieme",
                        "Con i partner tecnici e i mentor",
                        "Confronto tra gruppi e tra sfide diverse",
                        "Problemi comuni, domande, aggiornamenti",
                    ],
                },
                {
                    "tag": "Venerdì",
                    "title": "Mentoring privato, 30 minuti",
                    "bullets": [
                        "Il vostro gruppo con il mentor dell'azienda",
                        "Alle 16:00, 16:30, 17:00 o 17:30, secondo il gruppo",
                        "Domande mirate sulla vostra sfida",
                        "Gruppo, orario e mentor vi vengono comunicati",
                    ],
                },
            ],
            "note": "Sessioni condivise e private si svolgono <b>tutte sulla piattaforma</b>: niente link da cercare altrove.",
        },
        {
            "type": "calendar",
            "title": "Le date, settimana per settimana",
            "tue_label": "Sessione condivisa 17:30",
            "fri_label": "Mentoring privato",
            "weeks": [
                {"n": 1, "phase": "Gap analysis", "tue": "13 ottobre", "fri": "16 ottobre"},
                {"n": 2, "phase": "Benchmark", "tue": "20 ottobre", "fri": "23 ottobre"},
                {"n": 3, "phase": "Modello", "tue": "27 ottobre", "fri": "30 ottobre"},
                {"n": 4, "phase": "Pilota e KPI", "tue": "3 novembre", "fri": "6 novembre"},
                {"n": 5, "phase": "Presentazione", "tue": "10 novembre", "fri": "13 novembre"},
            ],
            "note": "<b>Lunedì 16 novembre</b>: presentazione finale dei gruppi.",
        },
        {"type": "section", "num": "03", "title": "Lavoro in gruppo"},
        {
            "type": "content",
            "title": "Il cuore del percorso è il lavoro autonomo",
            "bullets": [
                "Le sessioni sono solo una parte: il lavoro vero lo fate <b>voi, nel gruppo</b>, tra un incontro e l'altro",
                "Ogni gruppo ha <b>libertà di movimento</b>: decidete come organizzarvi, quando vedervi, quali strumenti usare",
                "Le tappe settimanali sono la traccia, il modo di percorrerla è vostro",
                "I mentor orientano e stimolano, le scelte restano al gruppo",
            ],
            "illus": "team",
        },
        {
            "type": "content",
            "title": "Collaborare davvero",
            "bullets": [
                "<b>Mettete in comune le competenze</b>: nel gruppo ci sono profili diversi, usateli",
                "<b>Incontratevi con regolarità</b>, anche solo per 15 minuti di aggiornamento",
                "<b>Condividete idee, dubbi e bozze</b>: il confronto migliora il lavoro",
                "<b>Date spazio a tutti</b>: ogni punto di vista conta",
                "Nelle sessioni condivise confrontatevi <b>anche con gli altri gruppi</b>, sulla stessa sfida e sull'altra",
            ],
            "illus": "puzzle",
            "side": "left",
        },
        {
            "type": "steps",
            "title": "Come prepararsi alle sessioni",
            "steps": [
                "<b>Raccogliete le domande</b> nel gruppo, prima di ogni incontro",
                "<b>Scegliete le più importanti</b>: in 30 minuti ne servono poche e buone",
                "<b>Capite a chi rivolgerle</b>: mentor, normativa o dati",
                "<b>Portate qualcosa su cui discutere</b>: dati, bozze, schemi",
                "<b>Prendete appunti</b> durante la sessione",
                "<b>Condividete le risposte</b> con tutto il gruppo e decidete i passi successivi",
            ],
        },
        {
            "type": "routing",
            "title": "A chi rivolgere le domande",
            "rows": [
                {"who": "Mentor aziendali", "color": M, "what": "Prodotto, processi, filiera e vincoli operativi dell'azienda"},
                {"who": "MV Consulting", "color": O, "what": "Normativa, sicurezza alimentare, standard e certificazioni"},
                {"who": "Wiseside", "color": G, "what": "Struttura del dato, interoperabilità e strumenti digitali"},
            ],
            "illus": "routing",
            "note": "Nelle sessioni condivise potete portare anche dubbi che riguardano tutti i gruppi.",
        },
        {"type": "section", "num": "04", "title": "La piattaforma"},
        {
            "type": "content",
            "title": "Tutto su www.challengeat.it",
            "bullets": [
                "<b>Un unico punto di riferimento</b> per tutto il percorso: www.challengeat.it",
                "Accessibile da <b>computer e da telefono</b>, grazie a Moodle",
                "Anche le <b>sessioni, condivise e private</b>, si svolgono tramite la piattaforma",
                "Faremo insieme un <b>tutorial</b> per imparare a usarla",
            ],
            "illus": "devices",
        },
        {
            "type": "steps",
            "title": "I prossimi passi",
            "steps": [
                "<b>Accedete</b> a www.challengeat.it",
                "<b>Guardate il tutorial</b> sulla piattaforma",
                "<b>Scoprite gruppo, orario e mentor</b> del vostro venerdì",
                "<b>Conoscetevi</b>: scegliete come restare in contatto nel gruppo",
                "<b>Preparate le prime domande</b> per la sessione di mentoring",
                "<b>Partecipate alla prima sessione condivisa</b>: [data da confermare]",
            ],
        },
        {"type": "section", "num": "05", "title": "Il valore del percorso"},
        {
            "type": "statement",
            "eyebrow": "Prima di cominciare",
            "question": "Il valore del percorso sta nell'<em>esperienza</em> e nell'<em>impegno</em> che ci metterete.",
            "bullets": [
                "Non ci sono risposte già pronte: contano il metodo, il confronto e le scelte fatte insieme",
                "Provare, sbagliare e correggere fa parte del lavoro",
                "Porterete a casa competenze, relazioni e un'esperienza vera, a contatto con aziende reali",
                "Più ci mettete, più il percorso restituisce",
            ],
        },
        {
            "type": "closing",
            "title": "Buon lavoro, team!",
            "subtitle": "Ci vediamo in sessione condivisa",
            "meta": "ChallengEat 8 · Food Hub · Edizione 2026",
        },
    ],
}
