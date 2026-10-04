# 00 · Installa tutto una volta sola

Circa quindici minuti, una sola volta. Installa prima Claude Code (app desktop da [claude.com/download](https://claude.com/download), scheda Code), poi scegli una strada:

- lancia lo script del tuo sistema: `scripts/install-mac.sh`, `scripts/install-windows.ps1` o `scripts/install-linux.sh`;
- oppure apri una nuova sessione di Claude Code, in qualsiasi cartella, e incolla il prompt qui sotto. Claude chiede conferma prima di ogni installazione.

## Lascia che Claude installi il resto

**Italiano**

```text
Voglio che tu monti i miei video con HyperFrames in questo repository. Controlla se su questo computer ci sono Node.js 22 o più recente, FFmpeg, Python 3 e Poppler (strumenti PDF). Installa ciò che manca e chiedimi conferma prima di ogni installazione. Poi installa i pacchetti Python con pip install -r requirements.txt (se ho una scheda NVIDIA usa onnxruntime-gpu, su Windows senza NVIDIA onnxruntime-directml). Esegui claude plugin marketplace add heygen-com/hyperframes e claude plugin install hyperframes@hyperframes, poi npx hyperframes browser ensure, npx hyperframes doctor e python scripts/rvm-matte.py --prepare. Risolvi tutto ciò che segnalano e chiudi con bash scripts/check.sh e l'elenco di ciò che è installato, con le versioni.
```

**English (originale)**

```text
I want you to edit my videos with HyperFrames in this repository. Check if this computer has Node.js 22 or newer, FFmpeg, Python 3 and Poppler (PDF tools). Install anything that is missing, and ask me before each install. Then install the Python packages with pip install -r requirements.txt (with an NVIDIA card use onnxruntime-gpu, on Windows without NVIDIA onnxruntime-directml). Run claude plugin marketplace add heygen-com/hyperframes and claude plugin install hyperframes@hyperframes, then npx hyperframes browser ensure, npx hyperframes doctor and python scripts/rvm-matte.py --prepare. Fix whatever they flag and finish with bash scripts/check.sh and a list of what is installed, with versions.
```

## Comandi manuali (se preferisci farlo da te)

| Passo | Windows | Mac (con [Homebrew](https://brew.sh)) |
|---|---|---|
| Claude Code | `irm https://claude.ai/install.ps1 \| iex` | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Node.js, FFmpeg, Python | `winget install OpenJS.NodeJS.LTS`, `winget install Gyan.FFmpeg`, `winget install Python.Python.3.13` | `brew install node ffmpeg python` |
| Strumenti PDF | `winget install oschwartz10612.Poppler` | `brew install poppler` |
| Pacchetti Python (trascrizione, audio, scontorni) | `python -m pip install -r requirements.txt` | `python3 -m pip install --user -r requirements.txt` |
| Scontorno più veloce sulla scheda video | NVIDIA: `pip install onnxruntime-gpu`; altre: `pip install onnxruntime-directml` | già incluso su Apple Silicon |
| Modelli RVM (scontorno persone) | `python scripts/rvm-matte.py --prepare` | `python3 scripts/rvm-matte.py --prepare` |
| Chrome per il render | `npx hyperframes browser ensure` | idem |
| Plugin HyperFrames | `claude plugin marketplace add heygen-com/hyperframes` poi `claude plugin install hyperframes@hyperframes` | idem |
| Verifica | `bash scripts/check.sh` (su Windows da Git Bash) e `npx hyperframes doctor` | idem |

Il modello di Whisper si scarica la prima volta che lo usi.

**Generazione AI dal PC (facoltativa):** di base passa dalla GitHub Action con il segreto del repository. Per generare anche in locale, imposta la chiave come variabile d'ambiente del sistema (`setx OPENROUTER_API_KEY "..."` su Windows, `export OPENROUTER_API_KEY=...` nel profilo della shell su Mac e Linux). Mai dentro un file del repository.

**Nota:** dopo l'installazione apri un nuovo terminale, o una nuova sessione di Claude, così il computer trova i nuovi strumenti. Se un comando fallisce, incolla l'errore a Claude e chiedigli di risolverlo.
