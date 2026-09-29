# 03 · Il ciclo di montaggio

Pianifica, costruisci, guarda, ripeti. Due abitudini lo rendono veloce: pianificare prima che Claude costruisca qualsiasi cosa, e dare note come un regista. Di' che cosa, dove e quando, mai come.

1. **Prima il piano.** Chiedi una scaletta (beat sheet): una riga per momento, con orario, parole, che cosa appare e suono. Le modifiche sulla carta sono gratis.
2. **Taglia i tempi morti.** Claude elimina pause e respiri usando i tempi delle parole, senza tagliare dentro una parola. Prima il rough cut, poi gli effetti.
3. **Costruisci.** Claude scrive il montaggio in HyperFrames e sincronizza ogni effetto sulla sua parola.
4. **Anteprima e note.** Lancia `npx hyperframes preview` per guardarlo nel browser. Una nota per riga, con l'orario. Claude corregge e controlla i propri fotogrammi.
5. **Render.** Di' "esportalo", oppure lancia `npx hyperframes render -o final.mp4`.

## Prima il piano

Da usare dopo il [primo prompt](01-first-prompt.md).

**Italiano**

```text
Prima di costruire qualsiasi cosa, scrivi una scaletta di questo montaggio in forma di tabella: orario di inizio e fine, le mie parole esatte, che cosa appare sullo schermo, dove sta il testo e il suono. Formato: verticale 9:16 per i Reels. Tieni tutto il testo fuori dal 20% inferiore dello schermo e lontano dal bordo destro, dove ci sono i pulsanti dell'app. Aspetta il mio OK prima di costruire.
```

**English (originale)**

```text
Before you build anything, write a beat sheet for this edit as a table: start and end time, my exact words, what appears on screen, where the text sits, and the sound. Format: vertical 9:16 for Reels. Keep all text out of the bottom 20% of the screen and away from the right edge, where the app buttons are. Wait for my OK before you build.
```

## Note che funzionano

Una modifica per riga, sempre con l'orario.

**Italiano**

```text
A 0:07 il logo mi copre il volto. Spostalo accanto alla mia mano e rendilo più piccolo del 20%.
```

```text
Da 0:12 a 0:14 i sottotitoli vanno troppo veloci. Mostra due parole alla volta.
```

```text
Lo zoom a 0:21 arriva in ritardo. Fallo partire sulla parola "adesso".
```

**English (originale)**

```text
At 0:07 the logo covers my face. Move it next to my hand and make it 20% smaller.
```

```text
From 0:12 to 0:14 the captions go too fast. Show two words at a time.
```

```text
The zoom at 0:21 lands late. Start it on the word "now".
```
