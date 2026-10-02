# Quale modello usare (OpenRouter)

> Logica di scelta adattata da [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) (MIT, © 2026 Higgsfield AI), riscritta con gli id e i listini di OpenRouter. Vedi `THIRD_PARTY_NOTICES.md`.

Il catalogo cambia ogni settimana. **Prima di scegliere, guarda i più recenti:**

```bash
python scripts/media/openrouter.py models --type image --limit 15
python scripts/media/openrouter.py models --type video --limit 15
```

Dati verificati il 2 ottobre 2026 dagli endpoint pubblici `api/v1/images/models` e `api/v1/videos/models`.

## Regola d'oro

**Bozza economica, poi modello finale.** Prova inquadratura e prompt con un modello veloce o a bassa risoluzione. Passa al modello di qualità solo quando la bozza convince. Un video costa da 10 a 100 volte un'immagine: prima l'immagine giusta, poi la si anima.

## Immagini

| Bisogno | Modello consigliato | Note |
|---|---|---|
| **Oggetto scontornato** (frutta, prodotto, confezione) | `openai/gpt-image-2.5-sunburst` | `background: "transparent"`, `quality: "high"`: niente scontorno a mano |
| Stessa cosa, molte varianti, più veloce | `openai/gpt-image-2.5-flare` | trasparenza nativa, tier veloce |
| Testo leggibile nell'immagine, grafica, banner | `openai/gpt-image-2.5-sunburst` | il migliore sul testo; resta comunque meglio aggiungere i testi in HyperFrames |
| **Scena fotografica realistica** (campo, laboratorio, mercato) | `google/gemini-3-pro-image` | «Nano Banana Pro», fino a 4K, ottimo con immagini di riferimento |
| Scena realistica, più economica e veloce | `google/gemini-3.1-flash-image` | «Nano Banana 2», da 512 a 4K, formati estremi (1:4, 8:1) |
| Volti e persone coerenti tra più immagini | `bytedance-seed/seedream-5-0-pro` | fino a 10 riferimenti; 0,045 $ (0,09 $ in alta risoluzione) |
| Modifica precisa di un'immagine esistente | `black-forest-labs/flux-3-image` | fino a 10 riferimenti, fino a 4K; da 0,048 $ (1K) |
| **Icone e illustrazioni vettoriali** | `recraft/recraft-v4.1-pro-vector` | esce in **SVG**: si anima pezzo per pezzo in HyperFrames; 0,30 $ |
| Prima bozza velocissima | `google/gemini-3.1-flash-lite-image` | per provare il prompt |

## Video

Per un Reel a 1080×1920 serve **1080p verticale (9:16)**. Sotto, la clip va ingrandita e perde nitidezza.

| Bisogno | Modello consigliato | Note |
|---|---|---|
| **Clip di qualità, default** | `bytedance/seedance-2.5` | 4–30 s, fino a 720p, primo e ultimo fotogramma; prezzo a token video |
| Clip in **1080p o 4K** | `bytedance/seedance-2.0` | 4–15 s, 480p–4K |
| Realismo cinematografico, durate brevi | `google/veo-3.1` | solo 4, 6 o 8 s, 16:9 o 9:16, fino a 4K; 0,20 $/s senza audio |
| Stessa qualità Veo, più economica | `google/veo-3.1-fast` / `google/veo-3.1-lite` | 0,10 $/s e 0,05 $/s senza audio in 1080p |
| Fisica naturale (liquidi, frutta che cade), alta risoluzione | `minimax/hailuo-3` | 5–15 s in **2K**; 0,13 $/s |
| Bozza economica di movimento | `minimax/hailuo-3-max` | fino a 768p; 0,08 $/s |
| Clip lunghe in 1080p | `alibaba/wan-3.0` | 2–30 s; 0,20 $/s in 1080p |
| Massima qualità e durata, budget alto | `openai/sora-2-pro` | 4–20 s in 1080p; 0,50 $/s; niente fotogrammi di partenza |
| Movimento semplice su un solo piano | `kwaivgi/kling-v3.0-std` | 720p; 0,084 $/s |
| Ingrandire una clip già fatta | `black-forest-labs/flux-video-upscale` | upscale video |

### Cose da sapere sui video
- **Audio:** molti modelli lo generano di default. Nei nostri montaggi la musica è nostra: metti `"generate_audio": false`, costa meno.
- **Image-to-video:** `frame_images` con `first_frame` (e `last_frame` dove supportato) dà il controllo esatto su inquadratura e stile. È il modo migliore per restare coerenti con il brand.
- **Formati:** passa sempre `aspect_ratio` in modo esplicito. Se manca, alcuni modelli usano il loro default e tagliano il soggetto.
- **Durate fisse:** Veo accetta solo 4, 6 o 8 secondi. Lo strumento controlla durate, risoluzioni e formati prima di spendere.
- **Costi:** `openrouter.py check` stima i video a listino al secondo. Per Seedance (a token) la stima è approssimata.
