# Checklist di ripresa: gira una take che Claude può montare

Claude può montare solo ciò che la camera ha ripreso. Cinque minuti di preparazione decidono quanto saranno puliti ritagli, sottotitoli ed effetti. Basta un telefono.

## Camera e luce: prepara l'inquadratura

- [ ] Telefono o fotocamera su treppiede. L'inquadratura non si muove mai, così gli effetti restano agganciati a te.
- [ ] Formato scelto: orizzontale (16:9) lascia a Claude spazio per riformattare; verticale (9:16) se il video va solo sui Reels.
- [ ] Luce sul volto e un po' di distanza dal muro. Un bordo pulito dà un ritaglio pulito.
- [ ] Stanza silenziosa e microfono vicino a te. Whisper sente meglio, e anche le persone.
- [ ] Prima di fermare la registrazione, esci dall'inquadratura e riprendi 2 secondi di stanza vuota (clean plate): serve a Claude per nasconderti dopo.
- [ ] Se un oggetto deve prendere vita, riprendi altri 2 secondi senza l'oggetto.
- [ ] Fatta la prova di 5 secondi con [`prompts/02-test-shot.md`](../prompts/02-test-shot.md).

## Mentre parli: parla al tuo montatore

- [ ] Una richiesta per frase: "Zoom sulla mia mano." Claude la trova nella trascrizione.
- [ ] Una breve pausa dopo ogni richiesta, per dare spazio all'effetto. Claude la taglia dopo.
- [ ] Resta fermo per un secondo dove cade un effetto, per esempio con la mano aperta per un logo.
- [ ] Guarda il punto in cui apparirà l'effetto e reagisci: è questo che lo rende credibile.
- [ ] Pronuncia la call to action lentamente e chiaramente: è la frase che conta di più.
- [ ] Pronuncia bene i nomi (Food Hub, ChallengEat, FIREX) e segnali comunque nel primo prompt.

## Dopo la ripresa

- [ ] Copia il file in `input/` (es. `input/take.mp4`).
- [ ] Metti loghi in `assets/`, musica in `music/`, effetti sonori in `sfx/`, riferimenti di stile in `refs/`.
- [ ] Apri Claude Code nella cartella e parti da [`prompts/01-first-prompt.md`](../prompts/01-first-prompt.md).

**Due modi di chiedere:** pronuncia le richieste in camera, così chi guarda ti sente chiedere e vede succedere l'effetto, oppure parla normalmente e scrivi le richieste in chat dopo. Funzionano entrambi, perché Claude ha la trascrizione.
