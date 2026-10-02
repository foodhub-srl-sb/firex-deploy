# Quale modello usare (OpenRouter)

> Logica di scelta adattata da [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) (MIT, © 2026 Higgsfield AI), riscritta con gli id e i listini di OpenRouter. Vedi `THIRD_PARTY_NOTICES.md`.

Il catalogo cambia ogni settimana. **Prima di scegliere, guarda i più recenti:**

```bash
python scripts/media/openrouter.py models --type image --limit 15
python scripts/media/openrouter.py models --type video --limit 15
```

Dati verificati il 2 ottobre 2026 dagli endpoint pubblici `api/v1/images/models` e `api/v1/videos/models` e dalle classifiche di [Artificial Analysis](https://artificialanalysis.ai/video/leaderboard/image-to-video).

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

Per un Reel a 1080×1920 serve **1080p verticale (9:16)** o più. Sotto, la clip va ingrandita e perde nitidezza.

**Classifica di qualità** (Artificial Analysis, arena image-to-video, voti alla cieca, consultata il 2 ottobre 2026): 1 MiniMax H3 Max · 2 MiniMax H3 · 3 Gemini Omni Flash (non su OpenRouter) · 4 Seedance 2.0 · 5 HiDream-O1 (non su OpenRouter) · 6 Wan 3.0 · … · 11 Veo 3.1. Ricontrollala prima di scegliere: cambia ogni mese.

| Bisogno | Modello consigliato | Note |
|---|---|---|
| **Animare un'immagine, massima qualità e risoluzione** | `minimax/hailuo-3` | n. 2 in classifica, **2K**, 5–15 s, primo e ultimo fotogramma, immagini di riferimento; 0,13 $/s |
| Stessa qualità, più economico, risoluzione minore | `minimax/hailuo-3-max` | n. 1 in classifica, ma fino a **768p**; 0,08 $/s; niente audio |
| Clip in 1080p o 4K, riferimenti multipli (immagini, video, audio) | `bytedance/seedance-2.0` | n. 4 in classifica, 4–15 s |
| Clip lunghe e storie, riferimenti, estensione di clip | `bytedance/seedance-2.5` | 4–30 s, fino a 720p su OpenRouter; prezzo a token video. **Rifiuta immagini con persone reali** (vale per tutta la famiglia Seedance su BytePlus): per animare una persona vera usa MiniMax H3 |
| Clip lunghe in 1080p | `alibaba/wan-3.0` | n. 6 in classifica, 2–30 s; 0,20 $/s in 1080p |
| Durate brevi fisse, filiera Google | `google/veo-3.1` (Fast, Lite) | ormai n. 11: usalo solo se serve qualcosa di specifico; 4, 6 o 8 s |
| **Modificare una ripresa vera** (ambiente, oggetti, luce) | `black-forest-labs/flux-video-edit` | mantiene durata e audio; input fino a 15 s, uscita 720p; 0,03 $/s |
| Modificare una ripresa: ambiente intero, angolazione, formato | `runway/aleph-2` | tiene i movimenti originali (non fa camminare chi sta fermo); ~600p; 0,28 $/s |
| Ingrandire una clip già fatta | `black-forest-labs/flux-video-upscale` | da 1,5× a 3× |

### Immagini per animare una persona reale
Per «la stessa persona, in un'altra posa o angolazione» usa **`bytedance-seed/seedream-5-0-pro`** (n. 1 nella classifica di editing con identità preservata) con 1–3 fotogrammi della persona in `input_references`, poi anima l'immagine con un modello video.

### Cose da sapere sui video
- **Audio:** molti modelli lo generano di default. Nei nostri montaggi la musica è nostra: metti `"generate_audio": false`, costa meno.
- **Image-to-video:** `frame_images` con `first_frame` (e `last_frame` dove supportato) dà il controllo esatto su inquadratura e stile. È il modo migliore per restare coerenti con il brand.
- **Formati:** passa sempre `aspect_ratio` in modo esplicito. Se manca, alcuni modelli usano il loro default e tagliano il soggetto.
- **Durate fisse:** Veo accetta solo 4, 6 o 8 secondi. Lo strumento controlla durate, risoluzioni e formati prima di spendere.
- **Costi:** `openrouter.py check` stima i video a listino al secondo. Per Seedance (a token) la stima è approssimata.
