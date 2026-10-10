# 09 · Scrivi un copione per addetti ai lavori

Prima di girare serve un copione. Claude sceglie (o riceve) un tema preciso, cerca le fonti, verifica i numeri e scrive il copione seguendo [`copioni/LINEE-GUIDA.md`](../copioni/LINEE-GUIDA.md). Esempio finito: [`copioni/01-chimosina.md`](../copioni/01-chimosina.md).

## Come chiederlo

- **Dai un tema preciso**, con una cosa che ha un nome al centro: un enzima, un processo, un parametro, una norma, un disciplinare. Se hai solo un'area ("fermentazione"), chiedi a Claude tre temi candidati e scegline uno.
- **Indica il pubblico:** casari, tecnologi, R&D, startup, buyer, ricercatori.
- **Chiedi le fonti.** Ogni numero del copione deve averne una; ciò che non si verifica resta fuori dal parlato.

**Italiano**

```text
Scrivi un copione per un video verticale su [tema preciso], per [pubblico]. Segui copioni/LINEE-GUIDA.md e parti da copioni/_modello.md. Prima cerca e verifica le fonti, poi scrivi i 9 blocchi con il parlato e le indicazioni a schermo. Salvalo come copioni/NN-nome.md, conta le parole e dimmi che cosa va ricontrollato prima di girare.
```

```text
Non ho ancora un tema. Proponimi tre temi su [area] che passino il test del paradosso e abbiano un aggancio alla filiera italiana. Per ognuno: la cosa con un nome al centro, il paradosso in una frase e le fonti principali da verificare.
```

**English**

```text
Write a script for a vertical video about [specific topic], for [audience]. Follow copioni/LINEE-GUIDA.md and start from copioni/_modello.md. Research and verify sources first, then write the 9 blocks with voiceover and on-screen notes. Save it as copioni/NN-name.md, count the words and tell me what needs re-checking before we shoot.
```

**Consiglio:** dopo il copione, chiedi la versione breve (blocchi 1, 2 e 7) per un secondo video da 60-75 secondi.
