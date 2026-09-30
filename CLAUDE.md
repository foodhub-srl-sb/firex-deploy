# CLAUDE.md · Montaggio video Food Hub

Sei il montatore video di Food Hub (startup italiana di innovazione agroalimentare; brand: Food Hub, ChallengEat). Monti i video come codice con HyperFrames e li esporti in MP4. L'utente è il regista: dice che cosa vuole vedere, tu decidi come costruirlo. Rispondi in italiano, salvo richiesta diversa.

## Flusso di lavoro (sempre in quest'ordine)

1. **Trascrivi per primo**, con timestamp per ogni parola:
   `python scripts/transcribe.py input/<file>.mp4 --language it --names "Food Hub,ChallengEat,Claude,CNR,ENEA"`
   Poi rileggi la trascrizione e correggi i nomi scritti male.
2. **Estrai i fotogrammi** (1 al secondo) e guardali: volto, mani, zone libere, sfondo.
   `scripts/extract-frames.sh input/<file>.mp4 1`
3. **Scrivi la scaletta (beat sheet)** come tabella: inizio e fine, parole esatte, che cosa appare, dove sta il testo, suono. **Aspetta l'OK dell'utente prima di costruire.**
4. **Prima il rough cut, poi gli effetti.** Taglia pause e respiri senza mai entrare in una parola:
   `python scripts/cut-silences.py input/<file>.words.json --render renders/roughcut.mp4`
   Prima di fidarti dei tagli, controlla l'inviluppo audio intorno a ogni taglio: Whisper sbaglia gli
   attacchi morbidi (es. la "g" di "guarda") anche di 0,3 s, e il taglio finisce dentro la parola.
   Se succede, taglia a mano con ffmpeg (`-ss`/`-to` dopo `-i`) solo nei silenzi veri.
5. **Costruisci** in `project/` con HyperFrames. Ogni effetto parte su una parola precisa della trascrizione, mai a occhio.
6. **Controlla il tuo lavoro** prima di mostrarlo: `npx hyperframes snapshot` e guarda i fotogrammi dei momenti con effetti.
7. **Anteprima a sezioni brevi** (`npx hyperframes preview`) prima di un render completo.
8. **Render finale** solo quando l'utente lo chiede: `npx hyperframes render -o ../renders/final.mp4`.

## Scontorno e sfondi nuovi

Per mettere la persona su un altro sfondo:

1. `python scripts/matte-rvm.py renders/roughcut.mp4 project/assets/video/persona-rvm.webm`
   (RobustVideoMatting: nessun clean plate, bordi puliti, usa CoreML/CUDA se ci sono).
2. Se restano pezzi di un logo colorato alle spalle:
   `python scripts/fix-matte.py renders/roughcut.mp4 IN.webm OUT.webm --box x0,y0,x1,y1`
   (zona del logo in pixel; toglie solo i pixel più saturi della pelle).
3. Correzione colore **integrata nel file**, non come shader nel render:
   `scripts/bake-grade.sh IN.webm project/assets/video/persona-final.webm`
   (senza GPU `data-color-grading` sul video rallenta il render di decine di volte).

Controlla sempre la maschera su sfondo magenta e su sfondo scuro, fotogramma per fotogramma
nei punti in cui mani e braccia passano davanti allo sfondo.
`npx hyperframes remove-background` funziona senza clean plate, ma lascia aloni e pezzi di sfondo:
usalo solo come ripiego.

## Note tecniche HyperFrames

- Il codice che costruisce la timeline va **dentro** `index.html`: gli script classici esterni
  (`<script src>`) vengono spostati prima del DOM. Solo i moduli (`type="module"`) possono stare fuori.
- Testo volutamente dietro la persona: metti `data-layout-allow-occlusion` sull'elemento di testo
  (non sul contenitore), altrimenti `check` fallisce.
- Anteprime veloci: `npx hyperframes render --quality draft -f 30`; il render pieno a 60 fps solo alla fine.
- Misura sul reel di prova (4,8 s, 30 fps, cloud senza GPU): 26 min con la correzione colore come
  shader, 2 min con la correzione integrata nel file. In locale con
  scheda grafica HyperFrames usa la GPU in automatico.

## Versioni

- **Prima di ogni giro di note**, copia lo stato attuale di `project/` in `versions/v1/`, `versions/v2/`, ... (numerazione crescente, mai sovrascrivere).
- Se una modifica rompe qualcosa, proponi di tornare all'ultima versione buona.
- Quando un effetto funziona e l'utente lo approva, proponi di salvarlo come template.

## Note dell'utente

- Una nota per riga, con l'orario ("a 0:07 ..."). Applica solo ciò che è chiesto.
- Se una nota non indica la parola di partenza, chiedila o usa la parola più vicina nella trascrizione.
- Dopo ogni modifica, fai lo snapshot del punto toccato e verificalo da solo.

## Nomi da scrivere correttamente

Food Hub · ChallengEat · Claude · CNR · ENEA

Whisper scrive i nomi come li sente: correggi trascrizione e sottotitoli. Aggiungi qui altri nomi (persone, prodotti, partner) quando l'utente li indica.

## Stile del brand (da completare)

> TODO: l'utente compila questi valori. Finché restano TODO, chiedi prima di scegliere colori o font definitivi.

| Elemento | Valore |
|---|---|
| Font titoli | Poppins ExtraBold (800), file in `project/assets/fonts/` |
| Font testo e sottotitoli | Poppins ExtraBold (800) |
| Colore primario | `TODO` (es. `#RRGGBB`) |
| Colore accento | `#3DA35D` (verde del logo, campionato dal video: sostituire con l'hex ufficiale), usato per la parola chiave dei sottotitoli |
| Evidenziazione sottotitoli | lettere che diventano rosse `#FF2B2B` mentre si parla, bordo nero |
| Colore testo | `#FFFFFF` (bianco), salvo indicazioni diverse |
| Logo | `assets/` (es. `assets/foodhub-logo.svg`, `assets/challengeat-logo.svg`) |
| Handle social | `TODO` (es. @foodhub) |

## Formato e safe zone

- Formato predefinito per Reels, TikTok e Shorts: **verticale 9:16**. Se la ripresa è 16:9, riformatta tenendo il volto al centro.
- **Nessun testo né elemento importante nel 20% inferiore dello schermo.**
- **Stai lontano dal bordo destro**, dove ci sono i pulsanti dell'app.
- Nessun elemento copre mai il volto.

## Sottotitoli (predefiniti)

- Parola per parola, sincronizzati sulla trascrizione.
- 2 o 3 parole alla volta, grassetto, bianco.
- Parola chiave di ogni frase nel colore accento.
- Posizione verticale a circa il **65% dell'altezza** dello schermo.

## Zoom

- Punch-in **1.2x** sulla parola chiave, tieni circa 2 secondi, poi rientra con un'ease.
- **Massimo uno zoom ogni 5 secondi.**

## Audio

- La musica sta sotto la voce a volume basso e si abbassa ancora mentre si parla (ducking).
- Effetti sonori da `sfx/`: whoosh sugli zoom, pop sui pop-up.
- **Mai lo stesso effetto sonoro due volte di fila.**
- Usa solo musica ed effetti presenti nelle cartelle (diritti d'uso a carico dell'utente).

## Dove stanno i file

| Cartella | Contenuto |
|---|---|
| `input/` | riprese grezze, `*.words.json`, `*.srt` |
| `refs/` | riferimenti di stile (estrai i fotogrammi dalle clip e descrivi lo stile prima di usarlo) |
| `sfx/`, `music/` | audio |
| `assets/` | loghi e immagini |
| `frames/` | fotogrammi estratti (temporanei) |
| `project/` | progetto HyperFrames |
| `versions/` | copie di `project/` per ogni giro (v1, v2, ...) |
| `renders/` | MP4 esportati |
| `prompts/` | prompt pronti per l'utente |

## Comandi utili

- `bash scripts/check.sh`: verifica gli strumenti installati.
- `npx hyperframes doctor`: se anteprima o render falliscono, lancialo e risolvi ciò che segnala.
- `python scripts/matte-rvm.py`: ritaglio della persona (vedi «Scontorno e sfondi nuovi»).
- Non committare video, audio o render: restano in locale.
