# Handoff · Metodo "copioni per addetti ai lavori" da integrare nel repo contenuti Food Hub

**Da:** sessione nel repo `foodhub-srl-sb/firex-deploy` (montaggio video con HyperFrames), branch `ccr-2f4b45d8-bfqus1`.
**A:** nuova sessione nel repo dedicato alla generazione di contenuti Food Hub.
**Data:** 10 ottobre 2026.

---

## 1. Il compito della nuova sessione

1. **Analizza il repo contenuti:** struttura, tipi di contenuto già gestiti, template, prompt, skill, istruzioni (CLAUDE.md o simili), convenzioni di nomi e cartelle, eventuali pipeline o script.
2. **Proponi dove si inserisce** il nuovo tipo di contenuto, "video verticale divulgativo per addetti ai lavori", seguendo le convenzioni del repo. **Mostra la proposta all'utente e aspetta l'OK** prima di cambiare la struttura.
3. **Integra il metodo** adattando i file allegati al formato del repo: linee guida, modello, prompt, esempio, analisi di stile. Non duplicare ciò che il repo ha già (brand voice, regole di scrittura in italiano, fonti): collega invece di copiare.
4. **Aggiorna le istruzioni del repo**, così che una richiesta come "scrivi un copione su [tema]" segua il metodo senza spiegazioni (vedi la sezione 6).
5. **Collega il nuovo formato agli altri contenuti**, se il repo lo permette. Per esempio: dallo stesso tema e dalle stesse fonti, un post LinkedIn, una newsletter, un carosello (vedi la sezione 7).
6. **Commit e push** sul branch di sviluppo indicato nella sessione.

## 2. Che cosa è stato fatto finora

1. **Analisi di stile di GEOPOP**, canale italiano di divulgazione scientifica. 11 video verticali da TikTok (YouTube blocca i download dal server cloud), con trascrizione parola per parola, rilevamento dei tagli e fotogrammi. Risultato: `STILE.md`.
2. **Copione di prova** su un tema verticale: la chimosina da fermentazione (`01-chimosina.md`). Ricerca con fonti primarie, 524 parole, circa 3:10-3:30. L'utente l'ha approvato ("Perfetto!").
3. **Dal copione approvato, il metodo:** linee guida, modello vuoto e prompt pronto.

## 3. I file allegati

| File | Percorso nel repo di origine | Che cos'è |
|---|---|---|
| `STILE.md` | `refs/geopop/STILE.md` | Analisi GEOPOP: numeri del campione, formula in 6 punti, grafica, montaggio, formati, modello del contenuto sponsorizzato, cosa adattare e cosa no |
| `LINEE-GUIDA.md` | `copioni/LINEE-GUIDA.md` | **Il cuore del metodo:** scelta del tema, struttura in 9 blocchi, livello tecnico, voce, fonti, indicazioni a schermo, controllo finale, spunti per i prossimi temi |
| `_modello.md` | `copioni/_modello.md` | Modello vuoto da compilare, con i 9 blocchi |
| `01-chimosina.md` | `copioni/01-chimosina.md` | L'esempio di riferimento approvato dall'utente |
| `09-copione.md` | `prompts/09-copione.md` | Prompt pronti, in italiano e in inglese, per chiedere un copione o tre temi candidati |

**Link interni da sistemare.** I file si rimandano tra loro con percorsi relativi del repo di origine (per esempio `../../copioni/LINEE-GUIDA.md`, `refs/geopop/STILE.md`). Aggiornali alla struttura del nuovo repo.

**Alternativa al caricamento manuale.** Se il nuovo repo è nella stessa organizzazione GitHub, la sessione può aggiungere `foodhub-srl-sb/firex-deploy` e leggere i file direttamente dal branch `ccr-2f4b45d8-bfqus1`.

## 4. Il metodo in breve

- **Un tema solo, preciso:** al centro una cosa con un nome (molecola, enzima, processo, parametro, norma, disciplinare). Mai "il futuro del cibo".
- **Test del paradosso:** il tema contiene una tensione che chi è del settore conosce a metà. Nel copione 01, la stessa tecnologia è un enzima che non va in etichetta (Reg. CE 1332/2008) e un novel food mai autorizzato in UE (Reg. UE 2015/2283).
- **Aggancio italiano:** una DOP, un disciplinare, un'azienda, una norma che si applica qui.
- **9 blocchi:** aggancio, meccanismo, problema, svolta, passo in più, dove non entra, nodo, frontiera, chiusura. 450-550 parole, 3-3:30.
- **Livello tecnico:** lessico di settore spiegato una volta sola; ogni termine introdotto torna più avanti; al massimo un numero per blocco, sempre con una fonte.
- **Fonti prima del testo:** fonti primarie quando possibile, stime dette stime, dati che cambiano datati e segnati "da ricontrollare". Ciò che non si verifica non entra nel parlato.
- **Chiusura:** riprende l'aggancio e fa una domanda a un mestiere ("E tu, in caseificio, che caglio usi?"). I commenti degli addetti ai lavori alimentano networking e matching (Area 2).
- **Versione breve:** i blocchi 1, 2 e 7 reggono da soli un video di 60-75 secondi.

## 5. Che cosa resta nel repo video

Il repo `firex-deploy` resta il posto del **montaggio** (trascrizione, fotogrammi, HyperFrames, render). Nel repo contenuti va il **copione**: il passaggio dall'uno all'altro avviene quando il video è girato. Le indicazioni "A schermo" del copione ("cartello X su 'parola'") sono scritte apposta per il montaggio, dove ogni effetto parte da una parola della trascrizione.

Non portare nel repo contenuti le parti puramente tecniche del montaggio (posizioni dei sottotitoli, preset, safe zone), a meno che il repo non gestisca anche quelle.

## 6. Istruzioni da aggiungere nel repo contenuti

Testo usato nel `CLAUDE.md` di origine, da adattare ai percorsi del nuovo repo:

```markdown
## Copioni video (addetti ai lavori)

Quando l'utente chiede un copione o un tema per un video, segui `[percorso]/LINEE-GUIDA.md` e parti da `[percorso]/_modello.md`. Esempio di riferimento: `[percorso]/01-chimosina.md`.

- **Un tema solo, preciso:** al centro una cosa con un nome (molecola, processo, parametro, norma, disciplinare). Mai panoramiche generiche.
- **Prima le fonti, poi il testo.** Ogni numero e ogni data hanno una fonte nel file; le stime si dicono stime; i dati che cambiano si datano e si segnano da ricontrollare. Ciò che non si verifica resta fuori dal parlato.
- **Struttura in 9 blocchi**, 450-550 parole, aggancio dalla prima parola, chiusura con una domanda a un mestiere.
- Salva in `[percorso]/NN-nome.md`, conta le parole e di' all'utente che cosa va ricontrollato prima di girare.
```

## 7. Idee di integrazione da valutare con l'utente

- **Un tema, più formati.** La ricerca di un copione (fonti verificate, numeri, paradosso) basta anche per un post LinkedIn nel tono Food Hub (laconico, data-driven, fonti, domanda finale), un'uscita della newsletter, un carosello. Se il repo ha già generatori per questi formati, il copione può diventare la loro fonte.
- **Archivio dei temi.** Una lista dei temi candidati con stato (proposto, in ricerca, scritto, girato, pubblicato). Ci sono già 4 spunti nella sezione 9 di `LINEE-GUIDA.md`, non ancora verificati.
- **Contenuto sponsorizzato.** `STILE.md`, sezione 6, descrive il modello GEOPOP-Mutti (reportage in filiera). Per Food Hub è un servizio dell'Area 1 da proporre ad aziende e startup, con un'avvertenza: nel campione i video #adv hanno la metà dei like in proporzione alle visualizzazioni.

## 8. Decisioni ancora aperte (dell'utente)

- **Colori e font Food Hub:** nel repo video sono ancora `TODO`. Il giallo di GEOPOP (`#F0F800`) non si copia. Se il repo contenuti ha già un brand book, usa quello come fonte.
- **Conduttore:** la formula si regge su uno o più volti fissi con la maglietta del brand. Da decidere chi.
- **Frase di chiusura fissa** (il "motto" a fine video, come "le scienze nella vita di tutti i giorni" per GEOPOP): da scegliere.

## 9. Note tecniche utili

- **Scaricare video di riferimento:** dal server cloud YouTube risponde con il controllo anti-bot; TikTok funziona con `yt-dlp --impersonate chrome` (serve `pip install curl_cffi`). Instagram risponde 429.
- **Trascrizione:** con `faster-whisper` serve `av` tra la 13 e la 15 (`pip install "av>=13,<16"`); con la 19 va in errore.
- **Ricerca fonti:** le pagine di ScienceDirect rispondono 403 a una lettura automatica; abstract, PubMed e siti istituzionali (eur-lex, food.ec.europa.eu, ecfr.gov, disciplinari dei consorzi) funzionano.
- **Scrittura in italiano:** nessun trattino lungo, incisi tra virgole o parentesi (skill `italiano`).
