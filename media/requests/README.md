# Richieste di generazione (OpenRouter)

**Ogni file `.json` aggiunto o modificato in questa cartella avvia la GitHub Action «Genera media»**, che usa la chiave OpenRouter salvata nei segreti del repository e **spende credito**. Gli esempi da copiare stanno in `media/examples/` e lì non avviano nulla.

## Flusso
1. Scrivi la richiesta in `media/requests/<id>.json` (l'id è il nome del file).
2. Controllala, senza spendere: `python scripts/media/openrouter.py check media/requests/<id>.json`
3. Committala e pubblicala sul branch: l'Action parte da sola.
4. I risultati arrivano nel branch `media-store`, in `<id>/`, con un `result.json` (modelli, prompt, costi, errori).
5. Scaricali: `scripts/media/fetch.sh <id> projects/<progetto>/assets/ai`

L'Action si può anche lanciare a mano da GitHub: Actions → «Genera media» → Run workflow, indicando il percorso del file.

## Formato
```json
{
  "max_usd": 3,
  "jobs": [
    {
      "name": "mela",
      "type": "image",
      "model": "openai/gpt-image-2.5-sunburst",
      "prompt": "Photorealistic studio photo of a red apple ..., isolated on a fully transparent background",
      "aspect_ratio": "1:1",
      "quality": "high",
      "background": "transparent"
    },
    {
      "name": "mela-gira",
      "type": "video",
      "model": "bytedance/seedance-2.5",
      "prompt": "The apple slowly rotates on itself. Camera locked, no zoom ...",
      "duration": 5,
      "resolution": "720p",
      "aspect_ratio": "9:16",
      "generate_audio": false,
      "frame_images": [{ "ref": "@mela", "frame_type": "first_frame" }]
    }
  ]
}
```

| Campo | Significato |
|---|---|
| `max_usd` | Tetto di spesa della richiesta (default 5 $). Se la stima lo supera, non parte nulla; durante l'esecuzione i job oltre il tetto vengono saltati. |
| `jobs[].name` | Nome del file in uscita: minuscole, numeri, punto e trattino. |
| `jobs[].type` | `image` o `video`. |
| `jobs[].model` | Id OpenRouter: vedi `docs/ai/modelli.md` oppure `openrouter.py models`. |
| `jobs[].prompt` | In inglese: vedi `docs/ai/prompt.md`. |
| altri campi | Passano così come sono all'API: `aspect_ratio`, `resolution`, `quality`, `background`, `n`, `seed`, `duration`, `generate_audio`, `provider`, ... |

### Immagini da usare come input (`frame_images`, `input_references`)
- `"@nome"`: l'output di un job precedente della stessa richiesta.
- `"@nome:last"` / `"@nome:first"`: l'ultimo o il primo fotogramma reale di un video precedente, per concatenare le clip.
- `"input/foto.jpg"`: un file del repository (percorso dalla radice).
- `"https://..."`: un URL pubblico.

I job vengono eseguiti in ordine. Se un job fallisce, quelli che dipendono da lui vengono saltati, senza costi.
