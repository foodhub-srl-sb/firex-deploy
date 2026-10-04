# Studio video Food Hub

Il repository con cui Food Hub crea i suoi video senza aprire un programma di montaggio. Tu descrivi che cosa vuoi vedere, Claude costruisce il video come codice con HyperFrames e lo esporta in MP4. Tre usi:

| | Che cosa fa | Da dove partire |
|---|---|---|
| **Montaggio** | riprese con trascrizione, tagli, sottotitoli, zoom, effetti | [`prompts/01-first-prompt.md`](prompts/01-first-prompt.md) |
| **Video da zero** | caroselli animati, explainer, dati e icone in motion graphics | [`prompts/09-video-da-zero.md`](prompts/09-video-da-zero.md) |
| **Generazione AI** | immagini e clip video con i modelli più recenti via OpenRouter | [`prompts/10-genera-con-ai.md`](prompts/10-genera-con-ai.md) |

Non esiste una timeline: tu parli, Claude costruisce, tu guardi e dai le note.

Il metodo di montaggio viene dalla guida *Let Claude Edit Your Videos* di **@pauloshimas** (The Creator Stack, 2026), adattata qui per il team di Food Hub.

---

## Gli strumenti

Sei strumenti, cinque sono gratuiti. Si installano una volta sola.

| Ruolo | Strumento | Costo | Link |
|---|---|---|---|
| Il montatore | **Claude Code** | a pagamento (Claude Pro o superiore) | [claude.com/product/claude-code](https://claude.com/product/claude-code) |
| Il motore | **HyperFrames** (HeyGen) | gratuito, open source | [github.com/heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) |
| Le orecchie | **Whisper** / **faster-whisper** | gratuito, open source | [github.com/openai/whisper](https://github.com/openai/whisper) · [github.com/SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) |
| Gli occhi e le forbici | **FFmpeg** | gratuito, open source | [github.com/FFmpeg/FFmpeg](https://github.com/FFmpeg/FFmpeg) |
| L'aiutante | **Python 3.13** | gratuito | [python.org/downloads](https://www.python.org/downloads/) |
| Il motorino | **Node.js 22+** (LTS) | gratuito | [nodejs.org](https://nodejs.org) |
| Il generatore | **OpenRouter** (immagini e video AI) | a consumo, chiave nei segreti GitHub | [openrouter.ai](https://openrouter.ai) |

HyperFrames scarica da solo la sua copia di Chrome per il rendering. Su Windows, Git for Windows ([git-scm.com](https://git-scm.com)) è facoltativo.

**Tu porti:** il video, il logo e la musica o gli effetti sonori di cui hai i diritti.

---

## Il flusso in 5 passi

1. **Giri.** Una sola ripresa con telefono o fotocamera. Puoi chiedere gli effetti a voce mentre giri, oppure scriverli in chat dopo.
2. **Claude ascolta.** Whisper trascrive ogni parola con l'orario esatto di inizio e fine.
3. **Claude guarda.** FFmpeg estrae i fotogrammi, così Claude vede dove sei, dove sono le tue mani e che cosa c'è dietro di te.
4. **Claude costruisce.** Pianifica il montaggio, taglia le pause e aggiunge sottotitoli, zoom ed effetti, ognuno sincronizzato su una parola.
5. **Tu rivedi, Claude esporta.** Guardi l'anteprima nel browser, dai le note e ricevi l'MP4 finale.

---

## Avvio rapido

### 1. Installa

Installa prima Claude Code ([claude.com/download](https://claude.com/download), scheda Code), poi lancia lo script per il tuo sistema:

```bash
# macOS
bash scripts/install-mac.sh

# Linux
bash scripts/install-linux.sh
```

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File scripts\install-windows.ps1
```

Gli script installano Node.js, FFmpeg, gli strumenti PDF (Poppler), i pacchetti Python di [`requirements.txt`](requirements.txt) (trascrizione, audio, scontorni, RobustVideoMatting), il plugin HyperFrames con il suo Chrome per il render e i modelli RVM. Se trovano una scheda video adatta, propongono la versione accelerata di onnxruntime. Chiedono conferma prima di ogni passo; con `--yes` (`-Yes` su Windows) installano tutto.

In alternativa, apri una sessione di Claude Code e incolla il prompt in [`prompts/00-install.md`](prompts/00-install.md): Claude installa tutto e chiede conferma prima di ogni passo.

Dopo l'installazione apri un nuovo terminale (o una nuova sessione di Claude), così il sistema trova i nuovi strumenti.

### 2. Verifica

```bash
bash scripts/check.sh
npx hyperframes doctor
```

### 3. Il plugin HyperFrames

Il file [`.claude/settings.json`](.claude/settings.json) registra già il plugin HyperFrames: aprendo questa cartella in Claude Code, ti verrà proposto di attivarlo. Per installarlo a mano:

```bash
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
```

### 4. Primo video

Metti la ripresa in `input/take.mp4`, apri Claude Code in questa cartella e incolla il prompt di [`prompts/01-first-prompt.md`](prompts/01-first-prompt.md).

---

## Struttura delle cartelle

```
.
├── CLAUDE.md                regole che Claude legge a ogni sessione (stile, safe zone, flussi)
├── projects/<nome>/         un progetto HyperFrames per ogni video
├── templates/hyperframes-9x16/   il modello dei nuovi video: stile, animazioni, chiusura con logo
├── media/
│   ├── requests/            richieste di generazione AI (avviano la GitHub Action)
│   └── examples/            esempi di richieste da copiare
├── docs/ai/                 quale modello usare e come scrivere i prompt
├── .github/workflows/       la GitHub Action «Genera media» (OpenRouter)
├── input/                   riprese grezze, PDF e materiali
├── assets/                  logo Food Hub e immagini condivise
├── refs/                    riferimenti di stile
├── sfx/, music/             audio
├── scripts/                 installazione, trascrizione, tagli, audio, scontorni, generazione
├── prompts/                 i prompt da copiare
├── frames/, renders/, versions/   file generati (non versionati)
└── THIRD_PARTY_NOTICES.md   licenze dei contenuti adattati
```

I file multimediali restano in locale: `.gitignore` esclude video, audio, fotogrammi ed esportazioni. Le immagini e i video generati con l'AI stanno nel branch `media-store`.

---

## Script di supporto

**Trascrizione con timestamp per parola** (salva `input/take.words.json` e i sottotitoli):

```bash
python scripts/transcribe.py input/take.mp4 --language it --names "Food Hub,ChallengEat,Claude"
```

**Estrazione dei fotogrammi** (uno al secondo, in `frames/`):

```bash
scripts/extract-frames.sh input/take.mp4 1
```

**Taglio delle pause** (dal file delle parole a un rough cut):

```bash
python scripts/cut-silences.py input/take.words.json --render renders/roughcut.mp4
```

**Nuovo progetto video** (dal template, con musica ed effetti originali):

```bash
scripts/new-project.sh filiera-latte 40 "La filiera del latte"
```

**Musica ed effetti originali** (sintesi pura, nessun diritto di terzi):

```bash
python scripts/synth-audio.py --seconds 40 --music-out music/mio-video.wav
```

**Scontorno di oggetti su fondo bianco** (anche il bianco tra le foglie):

```bash
python scripts/cutout-white.py input/foto.jpg assets/oggetto.png --holes 40
```

## Generazione AI (OpenRouter)

La chiave non sta mai nel codice: è il segreto `OPENROUTER_API_KEY` del repository (Settings → Secrets and variables → Actions). La GitHub Action «Genera media» la usa quando arriva una richiesta.

```bash
python scripts/media/openrouter.py models --type video          # i modelli più recenti
python scripts/media/openrouter.py check media/requests/x.json  # valida e stima i costi, senza spendere
git add media/requests/x.json && git commit -m "..." && git push  # avvia la generazione
scripts/media/fetch.sh x projects/mio/assets/ai                   # scarica i risultati
```

Formato delle richieste: [`media/requests/README.md`](media/requests/README.md). Scelta del modello: [`docs/ai/modelli.md`](docs/ai/modelli.md). Prompt: [`docs/ai/prompt.md`](docs/ai/prompt.md).

## Comandi HyperFrames

Da lanciare nella cartella del progetto (`projects/<nome>/`):

| Comando | A cosa serve |
|---|---|
| `npx hyperframes doctor` | controlla Node.js, FFmpeg e Chrome e dice che cosa manca |
| `npx hyperframes preview` | apre l'anteprima nel browser |
| `npx hyperframes snapshot` | salva i fotogrammi del montaggio, per il controllo di Claude |
| `npx hyperframes check` | controlla errori, impaginazione e contrasto |
| `npx hyperframes render -q draft -o ../../renders/bozza.mp4` | bozza veloce |
| `npx hyperframes render -o ../../renders/final.mp4` | esporta l'MP4 finale |
| `npx hyperframes remove-background` | ritaglia la persona dallo sfondo |

---

## Da dove partire

1. [`docs/filming-checklist.md`](docs/filming-checklist.md): prima di girare.
2. [`prompts/02-test-shot.md`](prompts/02-test-shot.md): controlla l'inquadratura con 5 secondi di prova.
3. [`prompts/01-first-prompt.md`](prompts/01-first-prompt.md): trascrizione e fotogrammi.
4. [`prompts/03-edit-loop.md`](prompts/03-edit-loop.md): scaletta, costruzione, note.
5. [`prompts/04-everyday-edits.md`](prompts/04-everyday-edits.md): sottotitoli e pause tagliate, poi il resto.

Quando i passi di base ti vengono facili, prova un effetto 3D da [`prompts/05-show-off-edits.md`](prompts/05-show-off-edits.md). Se qualcosa non va, c'è [`prompts/08-troubleshooting.md`](prompts/08-troubleshooting.md).

**Regola pratica:** se riesci a descriverlo in una frase e a indicare la parola in cui succede, Claude lo può costruire.

---

## Crediti

Metodo e prompt originali di montaggio: *Let Claude Edit Your Videos*, di **@pauloshimas**, The Creator Stack (2026). L'autore invita ad adattare e remixare il flusso di lavoro: questa è la versione di Food Hub, tradotta e adattata in italiano.

Le guide ai prompt in `docs/ai/` adattano parti di [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) (MIT): dettagli in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
