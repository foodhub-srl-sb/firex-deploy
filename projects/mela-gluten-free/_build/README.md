# Come è stato costruito «La mela nel gluten-free»

Video di riferimento del format «talking head Food Hub» (ottobre 2026): hook all'aperto, studio con LED verde, sottotitoli stile Geopop, frasi su nero a macchina da scrivere. Questi script ripercorrono i passaggi; per un nuovo video copiali e cambia tempi, testi e percorsi.

Gli script hanno i percorsi scritti in cima (`ROOT`, nomi dei file in `input/`): aggiornali prima di usarli.

## 1. Trascrizione dei take

```bash
python scripts/transcribe.py input/<take>.mp4 --language it --model medium --names "Food Hub,..."
```

Whisper colloca l'inizio delle parole circa 0,05-0,2 s in ritardo: per questo il montaggio lascia più margine prima della parola (LEAD 0,20 s) che dopo (TAIL 0,10 s).

## 2. Montaggio dai take migliori

`build_roughcut.py`: elenco dei segmenti (sorgente, da, a), taglio delle pause sopra 0,30 s, conversione **HDR → SDR** (le riprese del telefono sono HLG BT.2020 a 10 bit: senza conversione i colori escono sbagliati), dissolvenze audio di 10 ms a ogni taglio, volume uniformato. Scrive `renders/<nome>.mp4` e la mappa dei tagli `renders/<nome>.cuts.json`.

`check_edges.py`: per ogni taglio misura se c'è parlato appena fuori dal bordo (attacchi o code di parola tagliati). `loud.py <file> <da> <a> [passo]`: volume nel tempo, per trovare dove inizia davvero una parola.

## 3. Tracce del progetto (velocità +8%, ritaglio 1,8x, colore)

```powershell
$enc = '-c:v','libx264','-preset','slow','-crf','16','-g','30','-keyint_min','30','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart','-an'
# hook: com'è, solo accelerato
ffmpeg -i renders\roughcut-v3.mp4 -filter_complex "[0:v]trim=0:6.45,setpts=(PTS-STARTPTS)/1.08,fps=30[v]" -map "[v]" @enc assets\video\hook.mp4
# studio: verdi del LED -40%, pelle riportata al tono dell'hook, ritaglio dalla cintura in su
$grade = "huesaturation=saturation=-0.4:colors=g+c:strength=2,eq=saturation=0.75,huesaturation=saturation=-0.4:hue=6:colors=r+m+y:strength=1.5:lightness=1,curves=all='0/0 0.45/0.56 1/1'"
ffmpeg -i renders\roughcut-v3.mp4 -filter_complex "[0:v]trim=start=6.45,setpts=(PTS-STARTPTS)/1.08,fps=30,$grade,crop=600:1067:228:633,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5[v]" -map "[v]" @enc assets\video\studio.mp4
# voce
ffmpeg -i renders\roughcut-v3.mp4 -vn -af "atempo=1.08" -ar 48000 -ac 2 audio\voice.wav
```

`-g 30` serve a HyperFrames (senza fotogrammi chiave fitti il video si blocca nel render). Il ritaglio `600:1067:228:633` vale per l'inquadratura di questo set: per un altro set rifai la prova con più livelli di zoom.

`skin.py "<immagine>@x0,y0,x1,y1"`: misura saturazione e tinta della pelle; obiettivo come nell'hook, saturazione circa 0,38 e rapporto R/G circa 1,5. Non usare il preset `skin-soft` di HyperFrames su queste riprese: aggiunge rosso.

## 4. Grafica e suoni

`make_assets.py` legge `type_cards.json` (testo e tempi delle frasi su nero) e crea:
- `audio/type-*.wav`: colpi di macchina da scrivere sintetizzati, uno per lettera, negli stessi tempi usati in `index.html` (`TW`);
- `assets/img/festival/p*.png`: il logo del festival diviso nei cinque petali (lo sfondo dell'originale è trasparente: si tiene l'alfa e ogni pixel va al petalo pieno più vicino).

## 5. Composizione e render

`index.html`, poi `npm run check` e `npm run render -- -q draft -o ../../renders/<nome>-bozza.mp4`. Ogni `<audio>` deve avere un `id`, altrimenti nel render è muto.
