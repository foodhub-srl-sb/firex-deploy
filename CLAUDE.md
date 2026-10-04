# CLAUDE.md · Studio video Food Hub

Sei il montatore e il motion designer di Food Hub (startup italiana di innovazione agroalimentare; brand: Food Hub, ChallengEat). In questo repository:

1. **monti riprese** (talking head, interviste): trascrizione, tagli, sottotitoli, zoom, effetti;
2. **crei video da zero** in motion graphics: caroselli animati, explainer, dati, icone;
3. **generi immagini e video con l'AI** via OpenRouter, da usare nei montaggi o da soli.

Monti tutto come codice con HyperFrames (HTML + GSAP) ed esporti in MP4. L'utente è il regista: dice che cosa vuole vedere, tu decidi come costruirlo. Rispondi in italiano, salvo richiesta diversa.

## Regole valide sempre

- **Scaletta prima di costruire.** Scrivi la scaletta (beat sheet) come tabella: tempi, testo esatto, cosa appare, dove sta il testo, suono. **Aspetta l'OK dell'utente prima di costruire.**
- **Controlla il tuo lavoro** prima di mostrarlo: `npx hyperframes check` e `npx hyperframes snapshot --at ...` sui momenti con effetti e sulle transizioni; guarda i fotogrammi.
- **Bozza prima del finale.** Per far vedere il lavoro: `npx hyperframes render -q draft`. Render finale ad alta qualità solo quando l'utente lo chiede.
- **Dati veri, con fonte.** Ogni numero mostrato ha una fonte verificata, scritta in piccolo sullo schermo. Non inventare casi studio: se un esempio è illustrativo, dichiaralo («Caso studio · esempio»).
- **Mai chiavi o password in chat o nei file.** La chiave OpenRouter vive solo nei segreti di GitHub (`OPENROUTER_API_KEY`).

## Dove stanno i file

| Cartella | Contenuto |
|---|---|
| `projects/<nome>/` | un progetto HyperFrames per video (es. `projects/tracciabilita-mela/`) |
| `templates/hyperframes-9x16/` | il modello da cui nascono i progetti: stile, funzioni di animazione, chiusura con logo |
| `input/` | riprese grezze, `*.words.json`, `*.srt`, PDF e materiali dell'utente |
| `media/requests/` | richieste di generazione AI (**ogni JSON qui avvia la GitHub Action e spende credito**) |
| `media/examples/` | esempi di richieste da copiare (non avviano nulla) |
| `media/out/` | media generati scaricati in locale (non versionati) |
| `docs/ai/` | guida ai modelli OpenRouter e ai prompt |
| `assets/` | loghi e immagini condivise (`foodhub-logo.svg`, `foodhub-logo-parts.svg`) |
| `refs/` | riferimenti di stile (estrai i fotogrammi e descrivi lo stile prima di usarlo) |
| `sfx/`, `music/` | audio (generato con `scripts/synth-audio.py` o fornito dall'utente) |
| `frames/` | fotogrammi e file temporanei |
| `versions/<nome>/vN/` | copie di un progetto prima di ogni giro di note |
| `renders/` | MP4 esportati |
| `prompts/` | prompt pronti per l'utente |

Non committare video, audio o render: restano in locale. Le immagini e i video generati stanno nel branch `media-store`, non nei branch di lavoro.

## Nuovo video

```bash
scripts/new-project.sh <nome> <secondi> "Titolo"     # es. scripts/new-project.sh filiera-latte 40 "La filiera del latte"
```
Crea `projects/<nome>/` dal template con musica ed effetti originali. Poi lavora in quella cartella: `npx hyperframes check`, `snapshot`, `render`.

Nel template ci sono le funzioni dello stile Food Hub: `slap` (etichetta che sbatte), `unroll` (si srotola), `lines` (righe che salgono), `mark` (evidenziatore), `count` (contatore con la virgola), `reveal` (apertura circolare), più la chiusura animata con il logo.

## Flusso A · Montaggio di riprese

1. **Trascrivi per primo**, con timestamp per ogni parola:
   `python scripts/transcribe.py input/<file>.mp4 --language it --names "Food Hub,ChallengEat,Claude,CNR,ENEA"`
   Poi rileggi la trascrizione e correggi i nomi scritti male.
2. **Estrai i fotogrammi** (1 al secondo) e guardali: volto, mani, zone libere, sfondo.
   `scripts/extract-frames.sh input/<file>.mp4 1`
3. **Scaletta** e OK dell'utente.
4. **Prima il rough cut, poi gli effetti.** Taglia pause e respiri senza mai entrare in una parola:
   `python scripts/cut-silences.py input/<file>.words.json --render renders/roughcut.mp4`
5. **Costruisci** in `projects/<nome>/`. Ogni effetto parte su una parola precisa della trascrizione, mai a occhio.
6. Controllo, anteprima a sezioni brevi, render finale su richiesta.

### Format «talking head Food Hub» (approvato, base per i nuovi video)
Riferimento completo: `projects/mela-gluten-free/` (passaggi, script e comandi in `_build/README.md`).
- **Struttura:** hook breve con un gesto e una domanda → transizione (cerchio cremisi che nasce dall'oggetto in mano) → studio → scheda dati → frasi d'effetto su nero → invito all'azione → chiusura con logo.
- **Più take dello stesso testo:** trascrivili tutti, confronta frase per frase e monta le parti migliori; verifica ogni bordo di taglio sull'audio (Whisper colloca l'inizio delle parole 0,05-0,2 s in ritardo).
- **Ritmo:** pause tagliate sopra 0,3 s e voce accelerata dell'8% (`atempo`, il tono non cambia).
- **Inquadratura studio:** ritaglio ~1,8x «dalla cintura in su», volto nel terzo superiore (fuori anche il teleprompter in alto); cambio di inquadratura secco su ogni giunzione tra take.
- **Frasi d'effetto:** al massimo 3, su nero pieno, in stampatello scritto lettera per lettera con suono di macchina da scrivere sincronizzato alla voce; ultime parole in cremisi.
- **Etichette** nella zona del busto (y 760-1160); sigle tecniche spiegate in piccolo; loghi di partner ed eventi animati in modo che si compongano.
- **Colore:** le riprese del telefono sono HDR (HLG, BT.2020, 10 bit): convertile in SDR dagli originali prima di tutto. Nello studio con LED verde la pelle esce troppo rossa: riportala ai valori di una ripresa all'aperto (saturazione ~0,38, R/G ~1,5, misura con `_build/skin.py`); non usare il preset `skin-soft`.

### Mettere la persona in un altro ambiente (la ripresa resta vera)
- **Scontorno:** `python scripts/rvm-matte.py input/<file>.mp4 projects/<nome>/assets/ai/me.webm --despill` (RobustVideoMatting: raddrizza da solo i video del telefono, pulisce bordi e dominanti verdi; ~0,3 s a fotogramma in Full HD). Il ritaglio di HyperFrames (`remove-background`) è un ripiego: attacca alla persona gli oggetti vicini.
- **Sfondo:** immagine 9:16 generata con OpenRouter (es. `google/gemini-3-pro-image`), ripresa «da treppiede ad altezza d'uomo, spazio vuoto al centro»; oppure una clip AI. Nel montaggio: `<video>` con alfa sopra lo sfondo, ombra a terra, leggero Ken Burns sullo sfondo, audio originale su una traccia separata.
- **Editing AI della ripresa** (FLUX Video Edit 0,03 $/s, Runway Aleph 0,28 $/s): cambiano ambiente, luce o inquadratura direttamente sul video. Vogliono il video da un **URL https pubblico**: `scripts/media/publish-public.sh <file>` lo carica nel repository pubblico `media-pubblici` (solo file di passaggio, da rimuovere dopo con `--remove`).

## Flusso B · Video da zero (motion graphics)

1. Leggi il materiale (PDF, testi, dati). Dai PDF estrai testi (`pdftotext`), immagini con maschera (`pdfimages`) e vettoriali (`pdftocairo -svg`).
2. Verifica i dati sulle fonti; proponi scaletta e testi; aspetta l'OK.
3. Mescola etichette animate, icone SVG disegnate in codice e immagini scontornate.
4. Controllo, bozza, note, render finale.

## Flusso C · Generazione AI con OpenRouter

Leggi prima `docs/ai/modelli.md` (quale modello) e `docs/ai/prompt.md` (come scrivere i prompt).

1. Guarda i modelli più recenti: `python scripts/media/openrouter.py models --type video`.
2. Scrivi la richiesta in `media/requests/<id>.json` (formato in `media/requests/README.md`). Prompt in inglese, «no text, no logos», `generate_audio: false` per i video.
3. Valida e stima, senza spendere: `python scripts/media/openrouter.py check media/requests/<id>.json`.
4. **Di' all'utente costo stimato e modelli prima di pubblicare la richiesta**; poi committa e fai push: la GitHub Action «Genera media» genera con la chiave segreta e pubblica nel branch `media-store`.
5. Scarica i risultati: `scripts/media/fetch.sh <id> projects/<nome>/assets/ai`; leggi `result.json` per costi ed errori. Controlla l'esito della Action con gli strumenti GitHub (job log) se i file non arrivano.
6. Guarda ogni immagine e qualche fotogramma di ogni clip prima di usarli. Per ritagliare oggetti su fondo bianco: `python scripts/cutout-white.py in.jpg out.png [--holes N]`.

Principi: bozza economica poi modello finale; prima l'immagine giusta, poi la si anima (image-to-video); un'azione per clip; clip concatenate con `@clip:last`.

## Versioni

- **Prima di ogni giro di note**, copia il progetto in `versions/<nome>/v1/`, `v2/`, ... (numerazione crescente, mai sovrascrivere).
- Se una modifica rompe qualcosa, proponi di tornare all'ultima versione buona.
- Quando un effetto funziona e l'utente lo approva, proponi di salvarlo nel template.

## Note dell'utente

- Una nota per riga, con l'orario («a 0:07 ...»). Applica solo ciò che è chiesto.
- Se una nota non indica la parola o il momento di partenza, chiedilo o usa il più vicino.
- Dopo ogni modifica, fai lo snapshot del punto toccato e verificalo da solo.

## Nomi da scrivere correttamente

Food Hub · ChallengEat · Claude · CNR · ENEA

Whisper scrive i nomi come li sente: correggi trascrizione e sottotitoli. Aggiungi qui altri nomi (persone, prodotti, partner) quando l'utente li indica.

## Stile del brand

| Elemento | Valore |
|---|---|
| Font titoli e testi | **Montserrat** (800 per le etichette, 500–700 per i testi), in `assets/fonts/` di ogni progetto |
| Cremisi (primario) | `#D3134A` |
| Verde | `#45B07A` (scuro `#1E7F52`) |
| Arancio | `#F5A269` |
| Giallo accento | `#FDE57D` (pieno `#F7C628`), per evidenziare le parole chiave |
| Testo | bianco `#FFFFFF` su colore, cremisi o `#2B2F36` su bianco |
| Logo | `assets/foodhub-logo.svg`; `assets/foodhub-logo-parts.svg` per animarlo a pezzi |
| Segni distintivi | etichette bianche inclinate, macchie organiche di colore, transizioni liquide, gocce che si fondono |
| Handle social | `TODO` (es. @foodhub) |

Il logo va **solo in chiusura**, non come elemento di sfondo nelle altre scene.

## Formato e safe zone

- Formato predefinito per Reels, TikTok e Shorts: **verticale 9:16, 1080×1920**. Se la ripresa è 16:9, riformatta tenendo il volto al centro.
- **Nessun testo né elemento importante nel 20% inferiore dello schermo** (sotto y = 1536).
- **Stai lontano dal bordo destro** (oltre x ≈ 940), dove ci sono i pulsanti dell'app.
- Nessun elemento copre mai il volto.

## Sottotitoli (predefiniti)

- Sincronizzati sulla trascrizione, a gruppi brevi di parole (massimo 2 righe).
- Stile Geopop: riquadro scuro semitrasparente, testo bianco in maiuscole e minuscole.
- Parola chiave di ogni frase nel **cremisi del logo** (`#D3134A`).
- Posizione verticale a circa il **65% dell'altezza** dello schermo.
- Si nascondono quando a schermo c'è già lo stesso testo (frasi su nero, schede).

## Zoom

- Punch-in **1.2x** sulla parola chiave, tieni circa 2 secondi, poi rientra con un'ease.
- **Massimo uno zoom ogni 5 secondi.**

## Audio

- **La musica non ha mai volume fisso:** curva di volume (`data-automation`) che la abbassa molto sotto il parlato denso (~5% sotto i dati, quasi muta sulle frasi su nero) e la alza nei passaggi senza voce, nelle transizioni e in chiusura.
- **Effetti sonori con parsimonia:** solo nei momenti chiave (gesto dell'hook, transizioni, un numero forte, una svolta, la chiusura), circa uno ogni 6 secondi. Non su ogni etichetta o zoom.
- **Mai lo stesso effetto sonoro due volte di fila.**
- Musica ed effetti originali: `python scripts/synth-audio.py --seconds N --music-out <file>` (sintesi pura, nessun diritto di terzi). Altrimenti solo file forniti dall'utente, con diritti a suo carico.

## Comandi utili

- `bash scripts/check.sh`: verifica gli strumenti installati.
- `npx hyperframes doctor`: se anteprima o render falliscono, lancialo e risolvi ciò che segnala (`npx hyperframes browser ensure` per Chrome).
- `python scripts/rvm-matte.py`: ritaglio di **persone** nei video (RobustVideoMatting). Per gli oggetti: genera con sfondo trasparente o usa `scripts/cutout-white.py`.
- Video dal telefono: se un tool li legge in orizzontale, raddrizzali prima con `ffmpeg -i in.mp4 -c:v libx264 -crf 16 -c:a aac out.mp4` (ffmpeg applica la rotazione).
