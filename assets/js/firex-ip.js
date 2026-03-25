(function () {
    ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12'].forEach(m => {
        const d = document.createElement('div');
        d.className = 'ig-month-label';
        d.textContent = m;
        document.getElementById('ig-months-row').appendChild(d);
    });

    const firexData = [
        { label: 'Fase 1–2, Osservatorio & Selezione', start: 1, end: 2.8, color: 'green', dur: '2 mesi', dot: { label: 'Tu ti trovi qui', position: 2.8, color: 'orange', onLine: true } },
        { label: 'Fase 3, Call Esplorativa', start: 2, end: 4.8, color: 'green', dur: '3 mesi' },
        { label: 'Fase 4, Report', start: 4.8, end: 5.8, color: 'green', dur: '1 mese' },
        { label: 'Fase 5, Webinar informativo + Selezione per ChallengEat', start: 5.8, end: 7.5, color: 'green', dur: '~1.5 mesi', dot: { label: 'Firma accordo di co-sviluppo', position: 7.4, color: 'red' } },
    ];
    const challengeData = [
        { label: 'Fase 6, Edizioni ChallengEat', start: 7.5, end: 10.5, color: 'magenta', dur: '3 mesi' },
        { label: 'Fase 7, Portafoglio Progetti', start: 10.5, end: 12.8, color: 'green', dur: 'Continuo', continuous: true },
    ];

    function buildRow(item, delay) {
        const row = document.createElement('div');
        row.className = 'ig-row';
        const lbl = document.createElement('div');
        lbl.className = 'ig-row-label';
        lbl.textContent = item.label;
        const area = document.createElement('div');
        area.className = 'ig-bar-area';
        const bar = document.createElement('div');
        bar.className = `ig-bar ${item.color} ${item.continuous ? 'continuous' : ''}`;
        bar.style.left = ((item.start - 1) / 12 * 100) + '%';
        bar.style.width = ((item.end - item.start) / 12 * 100) + '%';
        const il = document.createElement('span');
        il.className = 'ig-bar-ilabel';
        il.textContent = item.label.split(',')[0].trim();
        bar.appendChild(il);
        area.appendChild(bar);

        if (item.dot) {
            const dotEl = document.createElement('div');
            let dotClasses = `ig-dot ${item.dot.color}`;
            if (item.dot.onLine) dotClasses += ' on-line';
            dotEl.className = dotClasses;
            dotEl.style.left = ((item.dot.position - 1) / 12 * 100) + '%';

            const dotLabel = document.createElement('div');
            let labelClasses = `ig-dot-label ${item.dot.color}`;
            if (item.dot.onLine) labelClasses += ' on-line';
            dotLabel.className = labelClasses;
            dotLabel.textContent = item.dot.label;
            dotLabel.style.left = ((item.dot.position - 1) / 12 * 100) + '%';

            area.appendChild(dotEl);
            area.appendChild(dotLabel);
            setTimeout(() => {
                dotEl.classList.add('animated');
                dotLabel.classList.add('visible');
            }, delay * 1000 + 400);
        }

        row.appendChild(lbl);
        row.appendChild(area);
        setTimeout(() => bar.classList.add('animated'), delay * 1000 + 150);
        return row;
    }

    const fc = document.getElementById('ig-rows-firex');
    firexData.forEach((d, i) => fc.appendChild(buildRow(d, 0.5 + i * 0.1)));
    const cc = document.getElementById('ig-rows-challengeat');
    challengeData.forEach((d, i) => cc.appendChild(buildRow(d, 1.1 + i * 0.12)));
})();
// Animate on scroll
const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });
document.querySelectorAll('.aos').forEach(el => observer.observe(el));

// Case study collapsible
function toggleCase(btn) {
    const detail = btn.nextElementSibling;
    const isOpen = detail.classList.contains('open');
    detail.classList.toggle('open');
    btn.classList.toggle('open');
    btn.textContent = isOpen ? 'Leggi il caso studio ↓' : 'Chiudi ↑';
}

// FAQ accordion
document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
        const item = btn.closest('.faq-item');
        const isOpen = item.classList.contains('open');
        document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
        if (!isOpen) item.classList.add('open');
    });
});
