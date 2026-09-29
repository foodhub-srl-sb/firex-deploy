# 01 · Il primo prompt: occhi e orecchie

Claude legge testo e guarda immagini, ma non può riprodurre un video. Gli servono due cose: una trascrizione con l'orario di ogni parola (Whisper, le orecchie) e i fotogrammi del video (FFmpeg, gli occhi). Così sa che cosa dici, quando lo dici e com'è l'inquadratura in quel momento.

Esempio di ciò che Claude legge:

```text
4.68s → 5.12s   First,
5.32s → 5.74s   zoom
5.74s → 5.92s   in
5.92s → 6.00s   on
6.00s → 6.10s   my
6.10s → 6.40s   hand
```

È così che uno zoom cade sulla parola esatta, che i sottotitoli restano sincronizzati e che Claude trova pause e respiri da tagliare.

## Il prompt

Metti il video in `input/take.mp4`, poi incolla:

**Italiano**

```text
Il mio video è input/take.mp4 in questa cartella. Trascrivilo con Whisper, con un timestamp per ogni parola, e salva parole e tempi in input/take.words.json. Poi usa FFmpeg per estrarre un fotogramma al secondo e guarda i fotogrammi. Dimmi che cosa dico, quando lo dico e che cosa c'è nell'inquadratura in ogni momento. Questi nomi vanno scritti correttamente: Food Hub, ChallengEat, FIREX, Claude, CNR, ENEA, [altri nomi].
```

**English (originale)**

```text
My video is take.mp4 in this folder. Transcribe it with Whisper, with a timestamp for every word, and save the words and times to take.words.json. Then use FFmpeg to pull one frame per second and look at the frames. Tell me what I say, when I say it and what is in the shot at each moment. These names must be spelled right: [your name, brand, product].
```

**[nomi]:** Whisper scrive i nomi come li sente. Nei test dell'autore della guida "Claude" è diventato "Klav". Dai a Claude i nomi e lui corregge trascrizione e sottotitoli.

## Con gli script di questo repo

```bash
python scripts/transcribe.py input/take.mp4 --language it --names "Food Hub,ChallengEat,FIREX,Claude"
scripts/extract-frames.sh input/take.mp4 1
```

**Perché conta:** è questo passo che fa sembrare il montaggio fatto a mano. Ogni effetto successivo è sincronizzato su una parola, non indovinato.
