# 10 · Immagini e video con l'AI (OpenRouter)

Claude scrive la richiesta, la GitHub Action la esegue con la chiave OpenRouter salvata nei segreti del repository, i risultati arrivano nel branch `media-store`. La chiave non passa mai dalla chat.

**Prima volta:** su GitHub, Settings → Secrets and variables → Actions → New repository secret, nome `OPENROUTER_API_KEY`. Su OpenRouter imposta un limite di spesa sulla chiave.

## Il prompt

```text
Genera con l'AI [che cosa: es. 4 immagini scontornate di frutta / una clip di 6 secondi di un frutteto all'alba] per il video [nome]. Usa i modelli più recenti adatti, dimmi modelli e costo stimato prima di lanciare, tetto massimo [N] dollari.
```

## Che cosa succede
1. Claude controlla i modelli più recenti (`openrouter.py models`) e sceglie con [`docs/ai/modelli.md`](../docs/ai/modelli.md).
2. Scrive i prompt in inglese seguendo [`docs/ai/prompt.md`](../docs/ai/prompt.md) e la richiesta in `media/requests/`.
3. La valida (`openrouter.py check`): formati, durate, costo stimato. Ti dice quanto spende.
4. Con il tuo OK la pubblica: la GitHub Action genera e salva in `media-store`.
5. Claude scarica i risultati, li guarda e li usa nel montaggio.

## Buone pratiche
- **Prima l'immagine, poi il video:** si genera un fotogramma iniziale curato e lo si anima (image-to-video).
- **Bozza economica, poi modello finale.**
- **Niente testi generati:** i testi li aggiunge HyperFrames, nel font giusto.
- **Clip che si collegano:** l'ultimo fotogramma di una clip diventa il primo della successiva (`@clip:last`).
