# 09 · Un video da zero (motion graphics)

Per caroselli animati, explainer e video con dati e icone, senza riprese. Lo stile Food Hub è già nel template: etichette bianche inclinate, macchie di colore, transizioni liquide, chiusura con il logo.

## Il prompt

Metti il materiale in `input/` (un PDF del carosello, un testo, dei dati) e incolla:

```text
Crea un video verticale 9:16 di circa [durata] secondi a partire da input/[file], nello stile Food Hub. Mescola testi animati, icone che si muovono e immagini scontornate. Verifica i dati sulle fonti e mettile in piccolo sullo schermo. Prima proponimi la scaletta con i testi esatti e aspetta il mio OK.
```

## Che cosa succede
1. Claude legge il materiale (dai PDF estrae testi, immagini e vettoriali) e verifica i numeri.
2. Propone la scaletta: tempi, testi, animazioni, suoni. Tu approvi o correggi.
3. Crea il progetto con `scripts/new-project.sh`, costruisce, controlla i fotogrammi da solo.
4. Ti manda una bozza. Tu dai le note con l'orario, una per riga.
5. Render finale quando lo chiedi.

## Varianti utili
- «Usa solo icone vettoriali, niente foto.»
- «Genera con l'AI le immagini scontornate che servono» (vedi [`10-genera-con-ai.md`](10-genera-con-ai.md)).
- «Aggiungi una clip AI come sfondo della scena [n].»
