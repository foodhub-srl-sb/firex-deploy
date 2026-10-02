# Licenze di terze parti

Questo repository adatta alcuni contenuti di progetti open source. Le parti adattate riportano in testa la fonte.

## higgsfield-ai/skills

- Fonte: https://github.com/higgsfield-ai/skills (versione 0.13.0, settembre 2026)
- Usato in: `docs/ai/prompt.md` (schema a blocchi per le clip, blocco negativo per image-to-video, regole di continuità tra clip, storyboard prima del video, principi di scrittura dei prompt) e `docs/ai/modelli.md` (logica di scelta del modello, riscritta con gli id di OpenRouter).
- I testi sono stati tradotti, riscritti e adattati: nessun file è copiato integralmente e niente dipende dalla CLI o dalle API di Higgsfield.

```text
MIT License

Copyright (c) 2026 Higgsfield AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## RobustVideoMatting (modello)

- Fonte: https://github.com/PeterL1n/RobustVideoMatting, licenza **GPL-3.0**
- Usato da `scripts/rvm-matte.py`: il modello ONNX si scarica alla prima esecuzione in `~/.cache/rvm`. Nel repository non c'è codice né pesi di RVM; lo script è scritto da zero e chiama solo il modello.

## Altri componenti

- **GSAP** (`assets/vendor/gsap.min.js` nei progetti): licenza standard GreenSock, https://gsap.com/standard-license
- **Montserrat** (`assets/fonts/`): SIL Open Font License 1.1, https://fonts.google.com/specimen/Montserrat
