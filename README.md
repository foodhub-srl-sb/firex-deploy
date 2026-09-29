# Let Claude Edit Your Videos · Food Hub

Workspace per montare i video di **Food Hub**, **ChallengEat** e **FIREX** senza aprire un programma di montaggio. Si gira una ripresa, si mette il file nella cartella `input/` e si chiede a Claude che cosa deve comparire sullo schermo. Claude ascolta ogni parola, guarda i fotogrammi e costruisce il montaggio come codice con HyperFrames, poi lo esporta in MP4.

Non esiste una timeline: tu parli, Claude costruisce, tu guardi e dai le note.

Il metodo viene dalla guida *Let Claude Edit Your Videos* di **@pauloshimas** (The Creator Stack, 2026), adattata qui per il team di Food Hub.

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
├── CLAUDE.md          regole che Claude legge a ogni sessione (stile, safe zone, flusso)
├── input/             le riprese grezze (take.mp4, test.mp4) e le trascrizioni
├── refs/              riferimenti di stile: screenshot, GIF, clip brevi
├── sfx/               effetti sonori (whoosh, pop, ...)
├── music/             musiche di sottofondo con diritti d'uso
├── assets/            logo Food Hub, ChallengEat, FIREX e altre immagini
├── frames/            fotogrammi estratti da FFmpeg (generati, non versionati)
├── renders/           MP4 esportati (generati, non versionati)
├── versions/          versioni salvate del progetto prima di ogni giro di note (v1, v2, ...)
├── project/           il progetto HyperFrames (il montaggio scritto come pagina web)
├── prompts/           i prompt da copiare, in italiano e in inglese
├── docs/              checklist e materiali di supporto
└── scripts/           script di installazione e di supporto
```

I file multimediali restano in locale: `.gitignore` esclude video, audio, fotogrammi ed esportazioni.

---

## Script di supporto

**Trascrizione con timestamp per parola** (salva `input/take.words.json` e i sottotitoli):

```bash
python scripts/transcribe.py input/take.mp4 --language it --names "Food Hub,ChallengEat,FIREX,Claude"
```

**Estrazione dei fotogrammi** (uno al secondo, in `frames/`):

```bash
scripts/extract-frames.sh input/take.mp4 1
```

**Taglio delle pause** (dal file delle parole a un rough cut):

```bash
python scripts/cut-silences.py input/take.words.json --render renders/roughcut.mp4
```

## Comandi HyperFrames

Da lanciare nella cartella `project/`:

| Comando | A cosa serve |
|---|---|
| `npx hyperframes doctor` | controlla Node.js, FFmpeg e Chrome e dice che cosa manca |
| `npx hyperframes preview` | apre l'anteprima nel browser |
| `npx hyperframes snapshot` | salva i fotogrammi del montaggio, per il controllo di Claude |
| `npx hyperframes render -o final.mp4` | esporta l'MP4 finale |
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

Metodo e prompt originali: *Let Claude Edit Your Videos*, di **@pauloshimas**, The Creator Stack (2026). L'autore invita ad adattare e remixare il flusso di lavoro: questa è la versione di Food Hub, tradotta e adattata in italiano.
