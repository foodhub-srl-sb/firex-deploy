# 08 · Quando qualcosa non va

La maggior parte dei problemi si risolve con una riga. Descrivi che cosa vedi e quando, oppure incolla l'errore, e lascia lavorare Claude. Questi sono i primi che incontrerai.

## Le 6 soluzioni

### 1. Nomi scritti male

Dai a Claude nomi e brand già nel primo prompt. Corregge trascrizione e sottotitoli.

```text
Nella trascrizione e nei sottotitoli correggi questi nomi: Food Hub, ChallengEat, Claude, CNR, ENEA.
```

```text
Fix these names in the transcript and the captions: Food Hub, ChallengEat, Claude, CNR, ENEA.
```

### 2. Testo nascosto dai pulsanti dell'app

Indica a Claude la safe zone: niente nel 20% inferiore dello schermo né vicino al bordo destro.

```text
Rispetta la safe zone: niente testo nel 20% inferiore dello schermo e niente vicino al bordo destro.
```

```text
Keep the safe zone: nothing in the bottom 20% of the screen or near the right edge.
```

### 3. L'effetto arriva in ritardo

Indica la parola su cui deve partire. Claude ha l'orario esatto di ogni parola.

```text
L'effetto a 0:21 arriva tardi. Fallo partire sulla parola "[parola]".
```

```text
The effect at 0:21 lands late. Start it on the word "[word]".
```

### 4. Claude dice che ha finito, ma si vede male

Chiedigli di fare lo snapshot e controllare da solo. Così vede quello che vedi tu.

```text
Fai lo snapshot del fotogramma a 0:07 e controllalo tu stesso.
```

```text
Snapshot the frame at 0:07 and check it yourself.
```

### 5. L'anteprima o il render non partono

Lancia `npx hyperframes doctor`, poi incolla l'errore a Claude.

```text
Ho lanciato npx hyperframes doctor e ho ottenuto questo errore: [incolla l'errore]. Risolvilo.
```

```text
I ran npx hyperframes doctor and got this error: [paste the error]. Fix it.
```

**Windows, «Un criterio di controllo dell'applicazione ha bloccato il file»** (`DLL load failed` importando `av`, `scipy` o `faster_whisper`): è Smart App Control, che blocca i pacchetti Python appena scaricati. Per disattivarlo: Sicurezza di Windows → Controllo app e browser → Impostazioni di Smart App Control → Disattivato. Su molte versioni di Windows 11 non si può riattivare senza reinstallare il sistema: decidilo tu.

### 6. Una modifica ha rotto qualcosa

Chiedi a Claude di salvare una versione prima di ogni giro (v1, v2...), così puoi sempre tornare indietro.

```text
Prima di ogni giro di modifiche salva una versione del progetto in versions/ (v1, v2...). Ora torna alla v2.
```

```text
Save a version before each round (v1, v2...) so I can always go back. Now go back to v2.
```

## Abitudini: lavora come un regista

- Una modifica per messaggio.
- Dai sempre l'orario: "a 0:07".
- Di' che cosa vuoi vedere, non come programmarlo.
- Approva il piano prima della costruzione.

## Scorciatoie: risparmia tempo su ogni video

- Prima il rough cut, poi gli effetti.
- Guarda l'anteprima di sezioni brevi prima di un render completo.
- Tieni le regole di stile (font, colori, safe zone) nel file `CLAUDE.md` della cartella. Claude lo legge ogni volta.
- Quando un effetto funziona, chiedi a Claude di salvarlo come template.

```text
Questo effetto funziona: salvalo come template riutilizzabile per i prossimi video.
```

```text
This effect works: save it as a template I can reuse on the next videos.
```
