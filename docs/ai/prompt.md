# Come scrivere i prompt per immagini e video

> Contiene schemi e regole adattati da [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) (MIT, © 2026 Higgsfield AI): schema a blocchi per le clip, blocco negativo per image-to-video, continuità tra clip, storyboard prima del video, principi di scrittura. Tradotti e riscritti per OpenRouter e HyperFrames. Vedi `THIRD_PARTY_NOTICES.md`.

**I prompt si scrivono in inglese.** In italiano restano solo i testi che appaiono nel video, e quelli li mette HyperFrames, mai il modello.

## Principi

1. **Concreto e sensoriale:** soggetto + ambiente + stile + luce + inquadratura. Esempio: «a single red apple on a wooden table, soft morning window light, 85mm, shallow depth of field».
2. **Breve:** sotto le 200 parole circa. I prompt lunghi distorcono il risultato.
3. **In positivo:** «tack sharp» invece di «no blur», «empty orchard» invece di «no people».
4. **Niente testo generato.** Scrivi sempre «no text, no letters, no logos, no watermark». I testi del video li aggiungiamo noi in HyperFrames: sono nitidi, nel font giusto e modificabili.
5. **Niente marchi o persone reali.** I modelli li rifiutano, e non dobbiamo inventare prodotti o aziende veri. L'AI tende a stampare marchi finti sulle confezioni (es. «Sunnyside Orchard»): chiedi superfici neutre.
6. **Modificare un'immagine:** il prompt descrive solo **che cosa cambia**, non tutta l'immagine.
7. **Animare un'immagine:** il prompt descrive solo **il movimento**. L'immagine è già il soggetto.

## Immagini

### Oggetto scontornato (da animare nel video)
```text
Photorealistic studio product photo of {subject}, {angle: three-quarter view / top view}, soft even studio lighting, crisp detail, natural colors, fully visible with margin on every side, no text, no logos, isolated on a fully transparent background
```
Parametri: `gpt-image-2.5-sunburst`, `"background": "transparent"`, `"quality": "high"`, `"aspect_ratio": "1:1"`.
L'oggetto deve avere **margine su tutti i lati**: un soggetto tagliato dal bordo non si recupera dopo.

### Scena di sfondo (sotto i nostri testi)
```text
Vertical photograph of {place}, {time of day and light}, {one hero subject} centered, clean low-detail background with generous negative space in the upper and lower thirds, natural colors, no people, no text
```
Lo **spazio vuoto** in alto e in basso è dove andranno le etichette. Uno sfondo pieno di dettagli rende illeggibili i testi.

### Coerenza tra più immagini (stessa persona o prodotto)
Passa l'immagine di riferimento in `input_references` e apri il prompt con:
```text
IDENTITY LOCK: reproduce exactly the {person/product} in the reference image: same shape, proportions, colors, materials and details. Do not restyle, beautify or average it. Only change: {what changes}.
```

### Stile coerente per tutto il video
Scegli **un solo descrittore di stile** e incollalo identico in ogni prompt del video. Esempi:
- fotografico: `editorial photography, natural daylight, soft contrast, warm natural colors, 35mm`
- illustrato: `flat 2D vector illustration, bold clean shapes, solid flat fills, no gradients, palette #D3134A #45B07A #F5A269 #FFFFFF`
- materico: `hand-painted gouache, soft textures, warm muted palette, visible brush strokes`

Per uno stile illustrato, chiudi sempre con `non-photorealistic, illustrated, not a photo`.

## Video

### Schema a blocchi (una clip per ogni momento del video)
```text
STYLE: {lo stesso descrittore di stile, identico in ogni clip}
SCENE: {cosa si vede, con UNA sola azione chiara}
MOTION: {movimento di camera e del soggetto: slow push-in, gentle drift, orbit, rise, steady tracking}
AUDIO: none
NEGATIVE: color drift, flicker, warping, extra objects, captions, on-screen text, logos, watermark
```
Regole:
- **Una sola azione per clip.** Un secondo verbo nel prompt è un difetto: il modello riempie la durata improvvisando.
- **Lo stesso STYLE** in ogni clip e, se puoi, la stessa immagine di partenza come riferimento di stile.
- Parti da un'immagine (`frame_images`, `first_frame`) ogni volta che puoi: inquadratura e colori restano sotto controllo.

### Animare un'immagine (image-to-video): il blocco negativo
Il prompt descrive **solo il movimento**, poi aggiunge **sempre** un blocco negativo:
```text
{movimento}: the leaves sway gently in the breeze, light haze drifts slowly.
Camera locked, no camera movement, no zoom, the subject stays fully in frame. Only this happens, nothing else. The {object} stays still and unchanged. The subject keeps facing the same direction.
```
Togli «camera locked» solo se il movimento di camera è proprio quello che vuoi (es. «slow push-in»): in quel caso descrivilo come unico movimento.
Senza blocco negativo il modello improvvisa: zoom non richiesti, oggetti che cambiano, soggetti che si girano.

### Clip che si collegano (continuità)
- **Usa l'ultimo fotogramma reale** della clip precedente come primo fotogramma della successiva: nelle richieste si scrive `"ref": "@clip-1:last"`.
- Mantieni **direzione e velocità** del movimento a cavallo del taglio.
- **Loop perfetto:** stessa immagine come `first_frame` e `last_frame` (solo per azioni cicliche, come foglie al vento o vapore). Mai per azioni che si concludono.

### Footage che deve ospitare testi
- **Un solo movimento continuo**, lento e costante: push-in, orbit, rise. Niente tagli interni.
- **Soggetto al centro** con spazio pulito intorno: lì vanno le etichette.
- **Sfondo poco dettagliato** e luminosità costante, senza flicker.
- Ricorda la safe zone 9:16: niente elementi importanti nel 20% inferiore.

### Prima di spendere sul video: lo storyboard
Per una sequenza complessa, genera **una sola immagine** con 6 riquadri dello stesso movimento continuo («6-panel storyboard grid of ONE continuous camera move, NOT six different scenes, no text»). Costa come un'immagine e fissa palette, lente e progressione prima di pagare i video.

## Checklist prima di lanciare una richiesta
- [ ] Prompt in inglese, sotto le 200 parole, con «no text, no logos».
- [ ] Stesso descrittore di stile in tutte le immagini e clip del video.
- [ ] Formato esplicito (`aspect_ratio`), 9:16 per i Reel.
- [ ] Video: `generate_audio: false`, un'azione per clip, blocco negativo se parte da un'immagine.
- [ ] `python scripts/media/openrouter.py check <richiesta>` senza errori e stima sotto `max_usd`.
