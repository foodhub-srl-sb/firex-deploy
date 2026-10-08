"""Contenuti del pacchetto slide Naturitalia (ChallengEat 8)."""

M, O, G, D = "#D3134A", "#E07F3C", "#2E9B63", "#2A1E22"

DECK = {
    "title": "ChallengEat 8 · La sfida di Naturitalia",
    "short": "Sfida Naturitalia",
    "slides": [
        {
            "type": "cover",
            "title": "La sfida di Naturitalia",
            "subtitle": "Interoperabilità e tracciabilità nella filiera del kiwi",
            "date": "12 ottobre · 16 novembre 2026",
            "duration": "5 settimane",
            "mentor_label": "Mentor aziendali",
            "mentors": [
                "<b>Greta Gubellini</b>, Sviluppo Prodotto",
                "<b>Claudio Cecchini</b>, Responsabile Qualità Consorzio Frutteto",
            ],
            "illus": "kiwi",
        },
        {"type": "section", "num": "01", "title": "Chi propone"},
        {
            "type": "content",
            "title": "L'azienda e i mentor",
            "bullets": [
                "<b>Naturitalia</b>: ufficio commerciale di ortofrutta fresca, soci produttori in tutta Italia",
                "<b>Mercati</b>: GDO italiana ed estera, mercati nazionali",
                "<b>Kiwi</b>: 70% a marchio Jingold, circa 21.000 t nel 2025",
                "<b>Certificazioni</b>: GlobalG.A.P. e IFS Broker",
                "<b>Greta Gubellini</b> raccoglie le domande dei team e le gira ai referenti tecnici",
                "<b>Claudio Cecchini</b> risponde sul magazzino di lavorazione del kiwi",
            ],
            "illus": "crate",
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
                    "title": "Wiseside srl",
                    "bullets": [
                        "Piattaforma digitale che raccoglie e correla i dati di filiera",
                        "Architettura del dato lungo la supply chain",
                        "Interoperabilità con fornitori e clienti, KPI misurabili",
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
                {"who": "Mentor aziendali", "color": M, "what": "Prodotto, processi, magazzino, ordini e flussi della filiera del kiwi"},
                {"who": "MV Consulting", "color": O, "what": "Standard normativi, sicurezza alimentare, conformità degli imballi e PPWR"},
                {"who": "Wiseside", "color": G, "what": "Struttura del dato, identificativi, formati e interoperabilità tra sistemi"},
            ],
            "illus": "routing",
        },
        {"type": "section", "num": "02", "title": "Il problema"},
        {
            "type": "cards",
            "title": "Un settore instabile, variabile, dinamico",
            "cards": [
                {
                    "title": "Instabilità",
                    "bullets": [
                        "Clima e situazione geopolitica",
                        "Consumi e prezzi di mercato",
                        "Disponibilità di prodotto e concorrenza",
                        "Fitopatologie e insetti in campo",
                        "Errori gestionali e logistica",
                    ],
                },
                {
                    "title": "Variabilità",
                    "bullets": [
                        "Ordini con prodotto da più fornitori",
                        "Molti tipi di imballo, diversi per cliente",
                        "Calibri, categorie, standard qualitativi",
                        "Esigenze del mercato italiano ed estero",
                        "Tempi di spedizione e prezzi",
                    ],
                },
                {
                    "title": "Dinamicità",
                    "bullets": [
                        "Catena del freddo e shelf-life variabile",
                        "Tempi di raccolta",
                        "Spedizioni A×A e A×B",
                        "Ordini inseriti ogni giorno",
                        "Nuove normative da rispettare",
                    ],
                },
            ],
            "note": "Per lavorare in modo efficiente serve un <b>forte coordinamento</b> con fornitori e clienti.",
        },
        {
            "type": "flow",
            "title": "La filiera del kiwi",
            "nodes": [
                {"name": "Aziende agricole", "desc": "Producono e raccolgono; rispondono della qualità in campo (es. residui)"},
                {"name": "Coop, OP e magazzini", "owner": "Consorzio Frutteto", "desc": "Ricevono, conservano, lavorano e confezionano"},
                {"name": "Ufficio commerciale", "owner": "Naturitalia", "desc": "Raccoglie gli ordini, li gira ai magazzini, fattura"},
                {"name": "Logistica", "owner": "RLA o altri", "desc": "Ritiri, transiti in piattaforma e consegne"},
                {"name": "Clienti", "owner": "GDO, mercati", "desc": "Ordinano, possono modificare o respingere la merce"},
            ],
            "side_actors": [
                {"name": "Jingold:", "desc": "coordina la filiera dal campo al cliente, fissa standard e listini, valuta i reclami"},
                {"name": "Solonatura:", "desc": "acquista e tiene a scorta gli imballi per i soci"},
            ],
        },
        {
            "type": "cards",
            "title": "I partner della filiera",
            "cards": [
                {
                    "tag": "Club",
                    "title": "Jingold",
                    "bullets": [
                        "Consorzio dal 2001, spa dal 2012",
                        "Esclusiva mondiale del kiwi giallo Jintao",
                        "Portale ROOTS: maturazione e raccolta per lotto",
                        "8 magazzini autorizzati nel 2025",
                    ],
                },
                {
                    "tag": "Magazzino",
                    "title": "Consorzio Frutteto",
                    "bullets": [
                        "200 soci, sede a Cesena",
                        "Centri a Policoro, Latina, Rosarno",
                        "Magazzino autorizzato per il kiwi Jingold",
                        "Socio fondatore del Consorzio KiwiGold",
                    ],
                },
                {
                    "tag": "Imballi",
                    "title": "Solonatura",
                    "bullets": [
                        "Centrale d'acquisto dei materiali",
                        "Scorte per conto dei soci",
                        "Meno sprechi da cambi di marchio o di norma",
                        "WMS migliorabile con accesso diretto",
                    ],
                },
                {
                    "tag": "Logistica",
                    "title": "RLA",
                    "bullets": [
                        "3 piattaforme, 14 camion propri, 40 di terzi",
                        "Quasi 800.000 pallet l'anno",
                        "Satellitari e pallet card con barcode",
                        "80% degli ordini da gestionale (100% Jingold e Frutteto)",
                    ],
                },
            ],
        },
        {
            "type": "steps",
            "title": "Dall'ordine alla fattura",
            "steps": [
                "Il cliente ordina via <b>email, telefono o WhatsApp</b>",
                "Il commerciale verifica <b>al telefono</b> disponibilità e prezzi nei magazzini",
                "L'ordine entra in <b>Navgreen</b> e parte in automatico verso Jingold e il magazzino",
                "Il magazzino crea l'<b>ordine di lavoro</b> e collega i lotti con la scansione dei barcode",
                "RLA riceve l'ordine di carico; il magazzino segnala l'<b>orario di merce pronta</b> sul portale",
                "Consegna, riscontro di pesi e prezzi, <b>fattura</b> al cliente e liquidazione al fornitore",
            ],
            "note": "Il prodotto non passa da Naturitalia: va dal magazzino del socio alla piattaforma indicata dal cliente.",
        },
        {
            "type": "content",
            "title": "Qualità e reclami",
            "bullets": [
                "<b>Prima della raccolta</b>: analisi distruttive su colore della polpa, durezza, gradi Brix, sostanza secca",
                "<b>Dopo la raccolta</b>: campionatrice UNITEC con foto e NIR, analisi non distruttiva per lotto",
                "<b>In lavorazione</b>: ispettori terzi ogni giorno; report conforme, in deroga o non conforme",
                "<b>Reclami</b>: dal commerciale del cliente a Jingold, che valuta cause e responsabilità",
                "<b>Tracciabilità</b> in capo a ogni magazzino: produttore, lotto, ora di lavorazione",
            ],
            "illus": "magnifier",
        },
        {
            "type": "content",
            "title": "Dove si perde l'informazione",
            "bullets": [
                "Magazzini con <b>strumenti eterogenei</b>: gestionali interni, fogli di calcolo, carta",
                "Ordini e disponibilità passano da <b>email, telefono e WhatsApp</b>",
                "<b>Inserimenti manuali</b>: lenti, ripetuti, esposti a errori",
                "Lotti da collegare tra soggetti diversi, con <b>frazionamenti e aggregazioni</b>",
                "Più magazzini di origine e <b>più fornitori di imballi</b> per lo stesso ordine",
                "Molti errori nascono dai <b>tempi stretti</b> delle operazioni",
            ],
            "illus": "brokenchain",
            "side": "left",
        },
        {"type": "section", "num": "03", "title": "La sfida"},
        {
            "type": "statement",
            "question": "Come progettare una <em>tracciabilità completa</em> che racconti il viaggio del prodotto e della confezione, dal campo allo scaffale?",
            "bullets": [
                "Include logistica di prodotto e pack, lavorazione (spazzolatura, calibrazione, confezionamento) e stoccaggio",
                "Tiene conto di prodotti da più magazzini e imballi da più fornitori",
                "Usa un linguaggio che permetta di stimare KPI di sostenibilità",
                "Può integrare sicurezza alimentare e conformità degli imballi (Regolamento UE PPWR 2025/40)",
            ],
        },
        {"type": "section", "num": "04", "title": "Obiettivi"},
        {
            "type": "objectives",
            "title": "Che cosa vogliamo ottenere",
            "primary": [
                "Scambiare informazioni lungo la filiera con un <b>linguaggio informatico comune</b>",
                "Raccogliere i dati in modo lineare e adattivo, <b>scegliendo cosa condividere</b> con clienti e consumatori",
                "Dare agli operatori accesso <b>bottom-up</b> alle informazioni che oggi non hanno",
                "Soluzioni <b>modulari e scalabili</b>, estendibili ad altre filiere",
            ],
            "secondary": [
                "Tracciabilità del packaging",
                "Informazioni sulla qualità",
                "Informazioni logistiche",
                "KPI di sostenibilità",
                "KPI di monitoraggio economico",
            ],
        },
        {"type": "section", "num": "05", "title": "Perimetro e vincoli"},
        {
            "type": "twocol",
            "title": "Dentro e fuori dal perimetro",
            "inside": [
                "Modello di tracciabilità di prodotto e imballo per la filiera Naturitalia e Jingold, con il Consorzio Frutteto come riferimento",
                "Mappa dal campo al cliente e allo scaffale, separando le fasi già documentabili",
                "Legame tra origine, lotti, lavorazioni, stoccaggi, imballi e spedizioni",
                "Analisi delle fonti esistenti, anche cartacee, e set minimo di dati per il pilota",
                "Soluzioni digitali o ibride, identificativi e formati condivisi, standard aperti",
                "KPI di sostenibilità calcolabili; informazioni diverse per operatori, clienti e consumatori",
            ],
            "outside": [
                "Un sistema completo per tutta la filiera, sviluppato in 5 settimane",
                "Sostituire i gestionali o ridisegnare i processi dei magazzini",
                "Presupporre dati completi e già digitali presso tutti gli attori",
                "Intervenire sui sistemi di terzi senza verificarne la disponibilità",
                "Certificare la conformità o validare claim ambientali aggregando dati",
                "Soluzioni con costi sproporzionati rispetto ai benefici",
            ],
        },
        {
            "type": "content",
            "title": "Vincoli trasversali",
            "bullets": [
                "Esplicitare <b>costi</b> di avvio e gestione, <b>tempi</b>, competenze e impegno degli operatori",
                "Ridurre i <b>doppi inserimenti</b>, prevenire errori, gestire dati incompleti o in ritardo",
                "Rispettare la <b>riservatezza commerciale</b> con accessi e responsabilità differenziati",
                "Nessuna tecnologia esclusa a priori: ogni scelta va <b>motivata</b>",
                "Se usate l'IA, indicate come <b>verificare i risultati</b> e gestire gli errori",
                "Partire da un <b>ambito circoscritto</b>, ad esempio il legame tra lotti di imballo e prodotto confezionato",
            ],
            "illus": "shield",
        },
        {"type": "section", "num": "06", "title": "Tempistiche"},
        {
            "type": "timeline",
            "title": "Roadmap e output attesi",
            "weeks": [
                {"n": 1, "date": "12 · 18 ottobre", "phase": "Gap analysis e mappatura", "out": [
                    "Mappa di soggetti, processi e flussi",
                    "Discontinuità e responsabili del dato",
                    "Inventario: dati digitali, cartacei, non raccolti",
                ]},
                {"n": 2, "date": "19 · 25 ottobre", "phase": "Benchmark tecnologico", "out": [
                    "Modi per acquisire e scambiare i dati",
                    "Compatibilità, affidabilità, costi, impatto",
                    "Anche soluzioni semplici; scelta motivata",
                ]},
                {"n": 3, "date": "26 ottobre · 1 novembre", "phase": "Modello di soluzione", "out": [
                    "Set minimo di dati e identificativi",
                    "Legame lotti prodotto e imballo",
                    "Ruoli, accessi, dati mancanti",
                    "Schema operativo o prototipo",
                ]},
                {"n": 4, "date": "2 · 8 novembre", "phase": "Piano pilota e KPI", "out": [
                    "Flusso delimitato: soggetti, tempi, costi",
                    "Criteri di successo",
                    "KPI di funzionamento e di sostenibilità",
                ]},
                {"n": 5, "date": "9 · 16 novembre", "phase": "Presentazione finale", "tbc": True, "out": [
                    "[Da completare: formato e data della presentazione]",
                ]},
            ],
        },
        {"type": "section", "num": "07", "title": "Valutazione"},
        {
            "type": "criteria",
            "title": "Criteri di valutazione",
            "rows": [
                ("<b>Aderenza al contesto e facilità di adozione</b>, anche in magazzini poco digitalizzati", "Alta"),
                ("<b>Solidità del modello</b> di tracciabilità e di acquisizione dei dati", "Alta"),
                ("<b>Compatibilità</b> con i sistemi esistenti e replicabilità", "Media-Alta"),
                ("<b>Sostenibilità</b> economica e organizzativa, con stime trasparenti", "Media-Alta"),
                ("<b>Qualità dei KPI</b> e della comunicazione", "Media"),
                ("<b>Robustezza</b> con dati mancanti, errori, ritardi e adesione parziale", "Media"),
            ],
        },
        {"type": "section", "num": "08", "title": "Domande guida"},
        {
            "type": "questions",
            "title": "Domande per orientare il lavoro",
            "questions": [
                "Quali dati servono per il primo caso d'uso? Quali esistono, quali solo su carta, quali mancano?",
                "Come si collega il prodotto alla sua confezione, tra lotti, lavorazioni, magazzini e fornitori?",
                "Come aderisce un magazzino con pochi strumenti, senza doppi inserimenti né errori?",
                "Chi sostiene il costo e chi ne ricava il beneficio? Che cosa spinge ciascuno a condividere?",
                "Quali KPI e messaggi sono davvero attendibili? Come si separano misure, stime e dati mancanti?",
                "Qual è il primo passo sperimentabile e con quali criteri lo estendiamo ad altri magazzini?",
            ],
        },
        {
            "type": "closing",
            "title": "Buon lavoro, team!",
            "subtitle": "Domande al mentor: Greta Gubellini",
            "meta": "Naturitalia · ChallengEat 8 · Food Hub · Edizione 2026",
        },
    ],
}
