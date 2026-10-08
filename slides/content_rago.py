"""Contenuti del pacchetto slide RAGO (ChallengEat 8)."""

M, O, G = "#D3134A", "#E07F3C", "#2E9B63"

DECK = {
    "title": "ChallengEat 8 · La sfida di RAGO",
    "short": "Sfida RAGO",
    "slides": [
        {
            "type": "cover",
            "title": "La sfida di RAGO",
            "subtitle": "Tracciabilità e sicurezza alimentare nella cold chain della IV gamma",
            "date": "Settembre · ottobre 2026",
            "duration": "5 settimane",
            "mentor_label": "Mentor aziendale",
            "mentors": ["<b>Giuseppe Esposito</b>, Responsabile R&amp;D e Qualità"],
            "illus": "saladbag",
        },
        {"type": "section", "num": "01", "title": "Chi propone"},
        {
            "type": "content",
            "title": "L'azienda e il mentor",
            "bullets": [
                "<b>RAGO Società Cooperativa Agricola</b>",
                "<b>Settore</b>: insalatine fresche di I e IV gamma",
                "<b>Mercato</b>: GDO nazionale",
                "<b>Giuseppe Esposito</b>, Responsabile R&amp;D e Qualità, è il mentor aziendale",
                "Riferimento tecnico su <b>fisiologia post-raccolta, MAP, shelf-life, HACCP</b> e filiera IV gamma",
            ],
            "illus": "saladbag",
        },
        {
            "type": "cards",
            "title": "I partner tecnici",
            "cards": [
                {
                    "tag": "Normativa",
                    "title": "MV Consulting",
                    "bullets": [
                        "Normativa alimentare, food safety, shelf-life, certificazioni",
                        "Mappatura di Reg. CE e standard BRC, IFS, FSSC",
                        "Riferimenti scientifici e linee guida tecnico-regolatorie",
                        "Piattaforma AI su regolamenti UE, allerte, ritiri e best practice",
                    ],
                },
                {
                    "tag": "Tecnologia",
                    "title": "Weseside srl",
                    "bullets": [
                        "Piattaforma digitale che raccoglie e correla i dati di filiera",
                        "Architettura del dato lungo la supply chain",
                        "Interoperabilità con fornitori e clienti GDO, KPI misurabili",
                        "Dati da sensori, input manuali e sistemi terzi, in logica EPCIS",
                    ],
                },
            ],
            "note": "<b>Ogni settimana, per ogni team:</b> 30 minuti con il mentor aziendale (categoria e processo) e 30 minuti con i partner tecnici (normativa e tecnologia).",
        },
        {
            "type": "routing",
            "title": "A chi chiedere cosa",
            "rows": [
                {"who": "Mentor aziendale", "color": M, "what": "Fisiologia del prodotto, parametri di processo, tolleranze termiche"},
                {"who": "MV Consulting", "color": O, "what": "Standard normativi e database regolatori"},
                {"who": "Partner tecnologico", "color": G, "what": "Struttura del dato, sensori, interoperabilità"},
            ],
            "illus": "routing",
        },
        {"type": "section", "num": "02", "title": "Il problema"},
        {
            "type": "content",
            "title": "La IV gamma soffre il caldo",
            "bullets": [
                "Insalate e ortaggi tagliati e confezionati in <b>MAP</b>: la categoria refrigerata più sensibile alla temperatura",
                "Il <b>taglio</b> rompe le cellule e annulla le difese naturali del tessuto",
                "Rischio <b>microbiologico</b>: Listeria monocytogenes, E. coli, Salmonella spp.",
                "Rischio <b>sensoriale</b>: imbrunimento, perdita di turgore, off-flavour",
                "Il prodotto intero reagisce allo stress termico; <b>quello tagliato no</b>",
            ],
            "illus": "leafcut",
        },
        {
            "type": "stats",
            "title": "Conta l'esposizione cumulata, non il picco",
            "stats": [
                ("0–4 °C", "Finestra termica ottimale per la IV gamma a foglia"),
                ("8–10 °C", "Bastano esposizioni brevi per effetti non lineari sulla shelf-life"),
                ("Q10 2,5–4", "Accelerazione della crescita dei patogeni (legge di Arrhenius)"),
                ("TTI", "Time-Temperature Integral: il parametro critico lungo tutta la catena"),
            ],
            "note": "Il dato che serve è la <b>storia termica del lotto</b>, non la temperatura rilevata in un singolo punto.",
        },
        {
            "type": "content",
            "title": "La situazione di oggi in RAGO",
            "bullets": [
                "Temperature rilevate nei singoli step, ma in modo <b>passivo e non correlato</b>",
                "Manca una <b>storia termica integrata</b> del lotto",
                "Manca un <b>modello predittivo</b> di shelf-life residua",
                "Accettazione merce e TMC si basano su <b>misure puntuali</b>",
                "La TMC in etichetta è <b>conservativa</b>, non si adatta all'esposizione reale",
            ],
            "illus": "thermogaps",
            "side": "left",
        },
        {
            "type": "flow",
            "title": "Cinque nodi, sistemi che non si parlano",
            "nodes": [
                {"name": "Campo e raccolta", "owner": "RAGO", "desc": "Controllo diretto"},
                {"name": "Lavorazione e confezionamento MAP", "owner": "RAGO", "desc": "Controllo diretto"},
                {"name": "Logistica primaria a temperatura controllata", "owner": "Vettore terzo", "desc": "Leva contrattuale"},
                {"name": "Piattaforma distributiva", "owner": "Cliente GDO", "desc": "Sistemi del cliente"},
                {"name": "Punto vendita", "owner": "Fuori perimetro", "desc": "Nessun contratto diretto"},
            ],
            "note": "Il dato termico raramente passa al nodo successivo in tempo utile: la storia del lotto si ricostruisce <b>solo dopo</b>, mai in tempo reale.",
        },
        {"type": "section", "num": "03", "title": "La sfida"},
        {
            "type": "statement",
            "question": "Come trasformare la temperatura da dato registrato a <em>decisione in tempo reale</em>, lungo una cold chain discontinua?",
            "bullets": [
                "Monitorare e condividere il dato termico lungo la filiera della IV gamma",
                "Stimare la shelf-life residua del lotto",
                "Decidere se accettare o rifiutare la merce in ogni nodo",
            ],
        },
        {"type": "section", "num": "04", "title": "Obiettivi"},
        {
            "type": "objectives",
            "title": "Che cosa vogliamo ottenere",
            "primary": [
                "Conoscere la <b>storia termica reale del lotto</b> in ogni punto della catena",
                "Averla <b>nel momento della decisione</b> operativa",
                "Con un output in <b>formato standard</b> e interoperabile, utile a RAGO e agli altri nodi",
            ],
            "secondary": [
                "Il nodo con più impatto e meno investimento",
                "Governance del dato: proprietà, accesso, incentivi",
                "Modello di shelf-life residua, anche semplice",
                "KPI misurabili per un pilota reale",
                "Costo per unità compatibile con i margini",
            ],
        },
        {"type": "section", "num": "05", "title": "Perimetro e vincoli"},
        {
            "type": "twocol",
            "title": "Dentro e fuori dal perimetro",
            "inside": [
                "Nodi su cui RAGO ha controllo diretto o leva contrattuale: centrale di lavorazione, vettore primario",
                "Datalogger IoT, tag NFC/RFID con sensore termico, piattaforme cloud",
                "TTI fisici (etichette cromatiche) come complemento low-cost",
                "Dati secondo gli standard di settore, interoperabili con GDO e fornitori",
                "Integrazione con i sistemi di rintracciabilità esistenti",
            ],
            "outside": [
                "Modifiche ai processi interni di lavorazione o ai CCP",
                "Soluzioni che richiedono la cooperazione volontaria di tutti, senza leva contrattuale o normativa",
                "Blockchain come soluzione primaria: non ancora industrializzata qui",
                "Costi per unità incompatibili con i margini: ogni proposta stima il costo in più per confezione",
            ],
        },
        {"type": "section", "num": "06", "title": "Tempistiche"},
        {
            "type": "timeline",
            "title": "Roadmap e output attesi",
            "weeks": [
                {"n": 1, "date": "Gap analysis", "phase": "Mappatura della filiera", "out": [
                    "Mappa dei nodi e dei vuoti di dato termico",
                    "Chi rileva, con che strumento e frequenza",
                    "Dove si registra e se passa al nodo dopo",
                ]},
                {"n": 2, "date": "Benchmark", "phase": "Confronto tecnologico", "out": [
                    "IoT, NFC/RFID, TTI fisici, cloud",
                    "Costo per unità",
                    "Scalabilità multi-attore",
                    "Compatibilità con gli standard",
                ]},
                {"n": 3, "date": "Modello", "phase": "Proposta di soluzione", "out": [
                    "Minimal viable perimeter",
                    "Governance del dato",
                    "Soglie di allerta, shelf-life dinamica, accetta o rifiuta",
                ]},
                {"n": 4, "date": "Pilota", "phase": "Piano pilota e KPI", "out": [
                    "Esposizioni non rilevate in tempo reale",
                    "Rintracciabilità termica in caso di NC: meno di 4 ore (Reg. CE 178/2002)",
                    "Shelf-life recuperata per lotto; costo per unità",
                ]},
                {"n": 5, "date": "Demo Day", "phase": "Presentazione finale", "out": [
                    "Problema → gap → soluzione",
                    "Perimetro → KPI",
                    "Ostacoli e come superarli",
                ]},
            ],
        },
        {"type": "section", "num": "07", "title": "Valutazione"},
        {
            "type": "criteria",
            "title": "Criteri di valutazione",
            "rows": [
                ("<b>Aderenza al contesto reale</b> della IV gamma e implementabilità industriale", "Alta"),
                ("<b>Chiarezza e solidità</b> del modello di governance del dato", "Alta"),
                ("<b>Compatibilità</b> con standard e sistemi GDO esistenti", "Media-Alta"),
                ("<b>Sostenibilità economica</b>: costo stimato per unità di prodotto", "Media-Alta"),
                ("<b>Qualità e specificità</b> dei KPI proposti", "Media"),
                ("<b>Robustezza</b> senza la cooperazione volontaria di tutti gli attori", "Media"),
            ],
        },
        {"type": "section", "num": "08", "title": "Domande guida"},
        {
            "type": "questions",
            "title": "Domande per mettere alla prova le proposte",
            "questions": [
                "Chi paga il datalogger sul vettore terzo? Chi usa i suoi dati e perché dovrebbe condividerli?",
                "Se la piattaforma non è disponibile alla consegna, come si decide? Esiste un fallback?",
                "La soluzione regge se il vettore non aderisce? Qual è il perimetro minimo in cui funziona?",
                "Quanto costa in più ogni confezione, su un prodotto da 1,5–3,0 € a scaffale?",
                "Come diventa il TTI una decisione: accetta, rifiuta o accetta con shelf-life ridotta? Chi decide?",
                "Il modello di shelf-life usa dati sperimentali o stime? Quali parametri assume e quali ignora?",
            ],
        },
        {
            "type": "closing",
            "title": "Buon lavoro, team!",
            "subtitle": "Domande al mentor: Giuseppe Esposito",
            "meta": "RAGO Società Cooperativa Agricola · ChallengEat 8 · Food Hub · Edizione 2026",
        },
    ],
}
