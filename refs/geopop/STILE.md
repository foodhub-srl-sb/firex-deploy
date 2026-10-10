# Stile GEOPOP · analisi per i contenuti Food Hub

Analisi di 11 video verticali di GEOPOP (TikTok @geopop, settembre-ottobre 2026), scelti tra i più visti, quelli su cibo e innovazione e tre contenuti sponsorizzati (#adv). Per ogni video: trascrizione parola per parola, rilevamento dei tagli, fotogrammi.

Obiettivo: capire la **grammatica** del formato e adattarla a Food Hub. Per scrivere i copioni, il metodo operativo è in [`copioni/LINEE-GUIDA.md`](../../copioni/LINEE-GUIDA.md). **Simile, non una copia**: colori, logo, set e conduttori di GEOPOP restano loro.

I video scaricati restano in locale (`refs/geopop/*.mp4`, esclusi da git). Si rigenerano con i comandi in fondo.

## 1. I numeri del campione

| Video | Durata | Visualizzazioni | Like / visual. | Parole al minuto | Prima parola | Durata media inquadratura |
|---|---|---|---|---|---|---|
| Proteine in polvere: servono? | 10:11 | 1,5 mln | 6,8% | 134 | 0,0 s | 7,4 s |
| Sangue di San Gennaro | 4:09 | 1,4 mln | 6,5% | 164 | 0,0 s | 24,9 s |
| Specchio coperto da un foglio | 2:26 | 830 mila | 6,7% | 164 | 0,5 s | 20,8 s |
| Polpa di pomodoro (#adv Mutti) | 11:18 | 785 mila | 3,1% | 160 | 1,5 s | 5,0 s |
| 4 ottobre festa nazionale | 2:12 | 760 mila | 6,6% | 152 | 0,0 s | 8,8 s |
| Riscaldamento globale (#adv) | 1:59 | 646 mila | 3,4% | 162 | 0,0 s | 4,6 s |
| Padella con l'olio in fiamme | 5:07 | 538 mila | 9,4% | 136 | 0,4 s | 3,9 s |
| Strade del futuro (#adv) | 2:51 | 364 mila | 2,7% | 156 | 0,3 s | 3,5 s |
| Microscopio: che cos'è? | 0:45 | 292 mila | 2,8% | 184 | 0,0 s | 8,9 s |
| Indovinello delle mele | 3:19 | 277 mila | 6,6% | 138 | 0,0 s | 9,5 s |
| Tavolini in aereo | 1:07 | 104 mila | 8,2% | 166 | 0,0 s | 4,5 s |

Dati TikTok al 10 ottobre 2026. Durata media inquadratura = durata / (tagli rilevati + 1).

**Cosa dicono i numeri:**

- **La durata non è un limite.** I due video più visti durano 10 e 4 minuti. Su TikTok GEOPOP pubblica da 45 secondi a 11 minuti; su YouTube Shorts gli stessi temi in 2-3 minuti.
- **Si parla subito e veloce.** Prima parola entro 1,5 secondi in tutti gli 11 video (a 0,0 secondi in 7). Ritmo tra 134 e 184 parole al minuto, mediana 160. Pochissime pause sopra 0,6 secondi.
- **Il ritmo del montaggio cambia con il formato:** 3,5-5 secondi a inquadratura nei video su processi e filiere, oltre 20 secondi nei monologhi da studio. Funzionano entrambi: polpa di pomodoro (5 s) a 785 mila, San Gennaro (25 s) a 1,4 milioni.
- **I contenuti sponsorizzati raggiungono, ma coinvolgono meno:** like tra 2,7% e 3,4% delle visualizzazioni, contro 6,5-9,4% dei video editoriali.

## 2. La formula in sei punti

1. **L'aggancio è la prima parola.** Nessuna sigla, nessun logo animato, nessun "ciao a tutti". In 6 video su 11 l'apertura è una domanda concreta e controintuitiva ("Come fa il sangue di San Gennaro a liquefarsi?", "Ma come fa la polpa di pomodoro fresco a durare mesi e mesi?"). Negli altri è una notizia ("Da quest'anno il 4 ottobre è diventato festa nazionale"), un'affermazione che spiazza ("Questa macchina si guida completamente da sola e non è una novità"), un indovinello ("Indovinello! Abbiamo dieci casse di mele...") o un avvertimento urgente ("Padella con olio bollente... non buttare l'acqua!"). Titolo, descrizione e prima frase dicono la stessa cosa.
2. **Un oggetto in mano fin dal primo secondo.** Il misurino di proteine, il bicchiere d'acqua, il foglio rosso contro lo specchio, la lattina di pomodoro. L'oggetto rende la domanda fisica e trattiene il pollice.
3. **Una persona, che parla a te.** Conduttore a mezzo busto, centrato, sguardo in camera, "ragazzi", "guardate". Tono da amico competente, ironico, mai accademico. Più volti ricorrenti, tutti con la maglietta del brand.
4. **Spiegazione a gradini, con una metafora.** Domanda → "Allora, dal punto di vista chimico..." → 2-3 passaggi → un numero → una cautela ("è solo un'ipotesi", "i dati vanno presi con cautela") → battuta finale. Una metafora tiene in piedi tutto: "il riscaldamento globale è un cicchetto di troppo in un bicchiere pieno".
5. **Parlato denso, senza vuoti.** Il ritmo nasce dai jump cut sul parlato (pause tagliate quasi a zero) e dagli spezzoni di immagini, non da effetti.
6. **Chiusura breve e fissa.** Una battuta o un "ciao", oppure la frase di rito "vi do appuntamento al prossimo video, sempre qui su Geopop, le scienze nella vita di tutti i giorni", poi il logo animato. A volte un invito a commentare con una parola precisa ("scriveteci *cedolino* nei commenti") o un rimando al magazine. Nei contenuti sponsorizzati il ringraziamento al partner arriva solo alla fine.

## 3. Grafica a schermo

| Elemento | Come lo fa GEOPOP | Posizione |
|---|---|---|
| Logo | Wordmark bianco piccolo, sempre presente | in alto a sinistra, circa 5% dell'altezza |
| Sottotitoli | **Frase intera** (1-2 righe, 4-7 parole per riga), carattere sans regolare bianco, piccolo, su rettangolo grigio semitrasparente. **Non** parola per parola | centrati, **73-78% dell'altezza** |
| Parola chiave | Cartello grande in grassetto: testo nero su blocco giallo acido (circa `#F0F800`), oppure testo bianco e giallo su blocco nero per i concetti lunghi | allineato a sinistra o centrato, 50-65% dell'altezza, sopra i sottotitoli |
| Numeri e formule | Stesso cartello: "30 minuti dopo", "90 secondi", "60x0.9", "1.6/2.2 g di proteine per kg" | come sopra |
| Etichette | Segnaposto + luogo ("Parma", sottotitolo "Campo di pomodori"); ingrandimento "4x" / "10x" | luogo a sinistra, ingrandimento in alto a destra |
| Animazioni 3D | Molecole, oggetti che ruotano su griglia nera ("CO₂", "Passata e concentrato") | a tutto schermo |
| Inserto a cerchio | Il conduttore dentro un cerchio con bordo giallo, sfondo in bianco e nero | centro |
| Bianco e nero | Per gli a parte comici, i rimandi e i blooper finali | a tutto schermo |
| Chiusura | "G" del logo animata in giallo, oppure cartello "Video completo sul canale YouTube" | centro |

Il colore accento compare **solo** nei cartelli delle parole chiave. Il resto dello schermo è immagine pulita.

## 4. Montaggio e immagini

- **Spezzoni di immagini ogni 3-5 secondi** nei video che spiegano un processo (pomodoro, estintori, strade del futuro): campo, macchinari, primi piani di prodotto, monitor con i dati, filmati di repertorio. Il parlato del conduttore continua sotto.
- **Inquadratura fissa per 20-25 secondi** nei monologhi da studio (San Gennaro, specchio): lì tengono il ritmo il conduttore, i gesti e il cambio dei sottotitoli.
- **Set riconoscibili**: laboratorio con scaffali e luci blu, studio con il logo al neon, cucina. Luce calda di taglio, sfondo sfocato.
- **Riprese con lo smartphone** (San Francesco, specchio) funzionano quanto quelle da studio: 760-830 mila visualizzazioni. L'idea conta più della produzione.
- **Zoom**: nei fotogrammi analizzati non emergono punch-in evidenti; il ritmo lo fanno tagli e spezzoni.

## 5. I formati ricorrenti

| Formato | Esempio | Durata | Adattamento Food Hub |
|---|---|---|---|
| **"Perché...?" da studio** | San Gennaro, settembre, tavolini | 1-4 min | "Perché il parmigiano non ha lattosio?", "Perché la carne coltivata costa così tanto?" |
| **Esperimento in laboratorio** | Proteine in polvere, caglio | 3-10 min | Demo con un centro di ricerca partner (CNR, ENEA, università): un esperimento, un risultato |
| **Reportage in azienda (#adv)** | Polpa di pomodoro con Mutti: campo, analisi, stabilimento | 11 min | Il format di contenuto sponsorizzato per aziende e startup: "Come nasce...?" dentro la filiera del cliente |
| **Quiz "Che cos'è?"** | Microscopio sul tappo di sughero | 45 s | Ingrediente innovativo al microscopio o in macro, rivelato alla fine |
| **Commento a una notizia, con lo smartphone** | 4 ottobre festa nazionale | 2 min | Una notizia del settore (regolamento UE, bando, dato di mercato) spiegata in 90 secondi |
| **Metafora con oggetti** | Riscaldamento globale e cicchetto (#adv) | 2 min | Un dato complesso spiegato con oggetti da cucina |
| **Approfondimento per addetti ai lavori** (Food Hub) | Nessuno: GEOPOP parla al grande pubblico | 3-3:30 | Un tema verticale in 9 blocchi, dal meccanismo al nodo normativo. Esempio: [`copioni/01-chimosina.md`](../../copioni/01-chimosina.md) |

**Il cibo funziona per GEOPOP**: proteine in polvere (1,5 mln), polpa di pomodoro (785 mila), caglio (410 mila su YouTube). È lo spazio naturale di Food Hub, con in più l'accesso diretto a startup, aziende e ricerca.

## 6. Il modello del contenuto sponsorizzato

Il video Mutti mostra come GEOPOP vende contenuti alle aziende senza sembrare pubblicità:

- etichetta "ADV" piccola in alto, `#adv` in descrizione;
- la domanda è del pubblico ("come fa a durare mesi?"), non del marchio;
- il marchio compare **nei luoghi** (insegna dello stabilimento, camion, reparti), non nei cartelli;
- persone dell'azienda e dati reali (Brix, pH, colore, licopene) sullo schermo;
- ringraziamento al partner **solo alla fine**.

Attenzione al prezzo: nel campione i video #adv hanno la metà dei like in proporzione alle visualizzazioni. Per tenere alto il coinvolgimento conviene alternarli a molti contenuti editoriali.

Per Food Hub è un servizio dell'Area 1 (posizionamento e visibilità) da proporre a startup e aziende del network.

## 7. Cosa adattare e cosa no

**Da adattare:**

- aggancio dalla prima parola (entro 1 secondo), oggetto in mano, nessuna sigla;
- una frase di chiusura fissa che diventa il motto di Food Hub;
- conduttore ricorrente con maglietta Food Hub, tono diretto e ironico;
- sottotitoli a frase intera, discreti, più cartelli grandi solo per parole chiave e numeri;
- spezzoni di immagini ogni 3-5 secondi nei video su processi e filiere;
- cautela esplicita sui dati (coerente con il nostro stile data-driven);
- reportage sponsorizzato in filiera come prodotto per i clienti.

**Da non copiare:** il giallo `#F0F800` come colore di brand, il logo "G", i set, le grafiche in 3D identiche, i loro conduttori. Servono i colori e i font Food Hub (in `CLAUDE.md` sono ancora `TODO`).

**Differenze dalle impostazioni attuali del progetto** (`CLAUDE.md`), da decidere:

| Impostazione attuale | GEOPOP | Proposta |
|---|---|---|
| Sottotitoli parola per parola, 2-3 parole, grassetto | Frase intera, carattere regolare, su rettangolo grigio | Preset "divulgazione" stile GEOPOP accanto a quello attuale |
| Sottotitoli al 65% dell'altezza | 73-78% | 72-76%, dentro la safe zone (sopra l'80%) |
| Parola chiave colorata dentro i sottotitoli | Cartello separato e grande | Cartello separato nel colore accento Food Hub |
| Punch-in 1.2x ogni 5 secondi al massimo | Quasi assenti | Usarli poco; il ritmo lo danno spezzoni e jump cut |

## 8. Scaletta tipo (2 minuti)

Per il pubblico generalista. Per gli addetti ai lavori la struttura è più lunga (9 blocchi, 3-3:30): vedi [`copioni/LINEE-GUIDA.md`](../../copioni/LINEE-GUIDA.md), sezione 2.

| Tempo | Che cosa succede | A schermo |
|---|---|---|
| 0:00-0:03 | Domanda (o affermazione che spiazza), oggetto in mano | Primo piano, cartello con la parola chiave |
| 0:03-0:10 | Perché è sorprendente ("potrebbe sembrare... ma in realtà") | Spezzone di immagini |
| 0:10-1:30 | 2-3 passaggi di spiegazione, una metafora, un numero | Alternanza conduttore e immagini ogni 3-5 s, cartelli sui numeri |
| 1:30-1:45 | Cautela o limite del dato | Conduttore |
| 1:45-2:00 | Battuta, invito a commentare con una parola, frase di rito, logo | Chiusura con logo Food Hub |

## Come rigenerare il materiale

```bash
# elenco video del profilo TikTok (YouTube blocca i download dal server cloud)
yt-dlp --impersonate chrome --flat-playlist --print "%(id)s|%(title).80s|%(duration)s|%(view_count)s" --playlist-end 40 "https://www.tiktok.com/@geopop"
# download di un video
yt-dlp --impersonate chrome --write-info-json -o "refs/geopop/tt_%(id)s.%(ext)s" "https://www.tiktok.com/@geopop/video/<ID>"
# trascrizione e fotogrammi
python scripts/transcribe.py refs/geopop/tt_<ID>.mp4 --language it --names "Geopop"
scripts/extract-frames.sh refs/geopop/tt_<ID>.mp4 1
```
