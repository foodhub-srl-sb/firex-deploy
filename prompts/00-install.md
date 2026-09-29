# 00 · Installa tutto una volta sola

Circa quindici minuti, una sola volta. Installa prima Claude Code (app desktop da [claude.com/download](https://claude.com/download), scheda Code), poi scegli una strada:

- lancia lo script del tuo sistema: `scripts/install-mac.sh`, `scripts/install-windows.ps1` o `scripts/install-linux.sh`;
- oppure apri una nuova sessione di Claude Code, in qualsiasi cartella, e incolla il prompt qui sotto. Claude chiede conferma prima di ogni installazione.

## Lascia che Claude installi il resto

**Italiano**

```text
Voglio che tu monti i miei video con HyperFrames. Controlla se su questo computer ci sono Node.js 22 o più recente, FFmpeg, Python 3 e Whisper (faster-whisper su Windows, whisper-cpp su Mac). Installa ciò che manca e chiedimi conferma prima di ogni installazione. Poi esegui claude plugin marketplace add heygen-com/hyperframes e claude plugin install hyperframes@hyperframes, e lancia npx hyperframes doctor. Risolvi tutto ciò che segnala e chiudi con l'elenco di ciò che è installato, con le versioni.
```

**English (originale)**

```text
I want you to edit my videos with HyperFrames. Check if this computer has Node.js 22 or newer, FFmpeg, Python 3 and Whisper (faster-whisper on Windows, whisper-cpp on Mac). Install anything that is missing, and ask me before each install. Then run claude plugin marketplace add heygen-com/hyperframes and claude plugin install hyperframes@hyperframes, and run npx hyperframes doctor. Fix whatever it flags and finish with a list of what is installed, with versions.
```

## Comandi manuali (se preferisci farlo da te)

| Passo | Windows | Mac (con [Homebrew](https://brew.sh)) |
|---|---|---|
| Claude Code | `irm https://claude.ai/install.ps1 \| iex` | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Node.js, FFmpeg, Python | `winget install OpenJS.NodeJS.LTS`, `winget install Gyan.FFmpeg`, `winget install Python.Python.3.13` | `brew install node ffmpeg python` |
| Whisper | `python -m pip install faster-whisper` | `brew install whisper-cpp` (HyperFrames trascrive da solo) |
| Plugin HyperFrames | `claude plugin marketplace add heygen-com/hyperframes` poi `claude plugin install hyperframes@hyperframes` | idem |
| Verifica | `npx hyperframes doctor` | idem |

Il modello di Whisper si scarica la prima volta che lo usi.

**Nota:** dopo l'installazione apri un nuovo terminale, o una nuova sessione di Claude, così il computer trova i nuovi strumenti. Se un comando fallisce, incolla l'errore a Claude e chiedigli di risolverlo.
