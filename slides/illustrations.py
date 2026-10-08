"""Illustrazioni SVG leggere, senza testo, nei colori del logo Food Hub."""

M, O, G = "#D3134A", "#F4A269", "#48B17A"
MD, GD = "#A80F3B", "#2E7D53"
PEACH, CREAM, DARK = "#FCE8DA", "#FBF6F1", "#2A1E22"


def svg(body, label, vb=560):
    return (
        f'<svg viewBox="0 0 {vb} {vb}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">'
        f'<circle cx="{vb/2}" cy="{vb/2}" r="{vb/2 - 10}" fill="{PEACH}"/>{body}</svg>'
    )


def kiwi_slice(cx, cy, r):
    seeds = ""
    for i in range(14):
        ang = i * 360 / 14
        seeds += (
            f'<ellipse cx="{cx}" cy="{cy - r * 0.55}" rx="{r * 0.035:.1f}" ry="{r * 0.075:.1f}" '
            f'fill="{DARK}" transform="rotate({ang:.1f} {cx} {cy})"/>'
        )
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#8A6A45"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r * 0.9:.1f}" fill="#9CC75A"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r * 0.72:.1f}" fill="#B7D978"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r * 0.3:.1f}" fill="#F3EFD6"/>' + seeds
    )


def leaf(x, y, size, rot, color):
    return (
        f'<path d="M0 0 C {size*0.35} {-size*0.5}, {size*0.85} {-size*0.45}, {size} 0 '
        f'C {size*0.85} {size*0.45}, {size*0.35} {size*0.5}, 0 0 Z" fill="{color}" '
        f'transform="translate({x} {y}) rotate({rot})"/>'
    )


ILLUS = {}

ILLUS["kiwi"] = svg(
    f'<path d="M80 470 C 160 540, 300 545, 380 500" fill="none" stroke="{M}" stroke-width="6" '
    f'stroke-dasharray="4 18" stroke-linecap="round"/>'
    f'<circle cx="80" cy="470" r="16" fill="{M}"/><circle cx="230" cy="522" r="16" fill="{O}"/>'
    f'<circle cx="380" cy="500" r="16" fill="{G}"/>'
    + kiwi_slice(290, 255, 175)
    + leaf(430, 110, 90, -40, G) + leaf(430, 110, 70, -110, GD),
    "Mezzo kiwi con un percorso tratteggiato che collega tre punti della filiera",
)

ILLUS["crate"] = svg(
    '<ellipse cx="190" cy="270" rx="66" ry="54" fill="#8A6A45"/>'
    '<ellipse cx="290" cy="250" rx="66" ry="54" fill="#9C7A52"/>'
    '<ellipse cx="380" cy="278" rx="60" ry="50" fill="#8A6A45"/>'
    f'<rect x="100" y="290" width="360" height="160" rx="18" fill="{M}"/>'
    f'<rect x="100" y="340" width="360" height="12" fill="{MD}"/>'
    f'<rect x="100" y="392" width="360" height="12" fill="{MD}"/>'
    f'<path d="M320 80 h150 a24 24 0 0 1 24 24 v60 a24 24 0 0 1 -24 24 h-90 l-36 30 v-30 h-24 '
    f'a24 24 0 0 1 -24 -24 v-60 a24 24 0 0 1 24 -24 z" fill="{G}"/>'
    f'<circle cx="360" cy="134" r="9" fill="{CREAM}"/><circle cx="395" cy="134" r="9" fill="{CREAM}"/>'
    f'<circle cx="430" cy="134" r="9" fill="{CREAM}"/>',
    "Cassetta di kiwi con un fumetto di dialogo",
)


def bubble(x, y, color):
    return (
        f'<path d="M{x} {y} h120 a20 20 0 0 1 20 20 v56 a20 20 0 0 1 -20 20 h-46 l-24 26 v-26 h-50 '
        f'a20 20 0 0 1 -20 -20 v-56 a20 20 0 0 1 20 -20 z" fill="{color}"/>'
    )


ILLUS["routing"] = svg(
    bubble(70, 150, M) + bubble(210, 80, O) + bubble(350, 150, G)
    # foglia (prodotto) nel fumetto magenta
    + leaf(105, 198, 70, -20, CREAM)
    # documento (normativa) nel fumetto arancio
    + f'<rect x="250" y="102" width="62" height="74" rx="8" fill="{CREAM}"/>'
    + f'<rect x="262" y="118" width="38" height="7" rx="3" fill="{O}"/>'
    + f'<rect x="262" y="134" width="38" height="7" rx="3" fill="{O}"/>'
    + f'<rect x="262" y="150" width="26" height="7" rx="3" fill="{O}"/>'
    # rete di dati nel fumetto verde
    + f'<path d="M392 220 L430 182 L468 220 M430 182 V208" stroke="{CREAM}" stroke-width="6" fill="none"/>'
    + f'<circle cx="392" cy="220" r="12" fill="{CREAM}"/><circle cx="430" cy="182" r="12" fill="{CREAM}"/>'
    + f'<circle cx="468" cy="220" r="12" fill="{CREAM}"/>'
    # persona
    + f'<circle cx="280" cy="350" r="46" fill="{DARK}"/>'
    + f'<path d="M180 500 C 180 420, 380 420, 380 500 Z" fill="{DARK}"/>',
    "Una persona con tre fumetti: prodotto, normativa e dati",
)

ILLUS["magnifier"] = svg(
    kiwi_slice(240, 245, 120)
    + f'<circle cx="240" cy="245" r="150" fill="{CREAM}" fill-opacity="0.25" stroke="{DARK}" stroke-width="18"/>'
    + f'<line x1="350" y1="355" x2="462" y2="467" stroke="{M}" stroke-width="40" stroke-linecap="round"/>',
    "Lente d'ingrandimento su una fetta di kiwi",
)

ILLUS["brokenchain"] = svg(
    f'<rect x="60" y="230" width="200" height="100" rx="50" fill="none" stroke="{M}" stroke-width="28" transform="rotate(-25 160 280)"/>'
    f'<rect x="300" y="230" width="200" height="100" rx="50" fill="none" stroke="{O}" stroke-width="28" transform="rotate(-25 400 280)"/>'
    f'<line x1="268" y1="200" x2="282" y2="150" stroke="{DARK}" stroke-width="10" stroke-linecap="round"/>'
    f'<line x1="300" y1="210" x2="330" y2="170" stroke="{DARK}" stroke-width="10" stroke-linecap="round"/>'
    f'<line x1="262" y1="370" x2="250" y2="420" stroke="{DARK}" stroke-width="10" stroke-linecap="round"/>'
    f'<line x1="232" y1="360" x2="200" y2="400" stroke="{DARK}" stroke-width="10" stroke-linecap="round"/>'
    + leaf(380, 430, 70, -30, G),
    "Catena spezzata in due anelli",
)

ILLUS["shield"] = svg(
    f'<path d="M280 90 L430 145 V270 C430 370 360 440 280 475 C200 440 130 370 130 270 V145 Z" fill="{M}"/>'
    f'<path d="M210 280 L260 330 L360 220" fill="none" stroke="{CREAM}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>'
    f'<rect x="380" y="380" width="110" height="90" rx="16" fill="{O}"/>'
    f'<path d="M405 380 V350 a30 30 0 0 1 60 0 V380" fill="none" stroke="{O}" stroke-width="16"/>'
    f'<circle cx="435" cy="425" r="12" fill="{CREAM}"/>',
    "Scudo con spunta e un lucchetto",
)

ILLUS["target"] = svg(
    f'<circle cx="260" cy="300" r="190" fill="{M}"/><circle cx="260" cy="300" r="140" fill="{CREAM}"/>'
    f'<circle cx="260" cy="300" r="95" fill="{O}"/><circle cx="260" cy="300" r="50" fill="{CREAM}"/>'
    f'<circle cx="260" cy="300" r="20" fill="{M}"/>'
    f'<line x1="470" y1="90" x2="270" y2="290" stroke="{DARK}" stroke-width="12" stroke-linecap="round"/>'
    f'<path d="M470 90 l10 -50 l30 30 z M470 90 l50 -10 l-30 -30 z" fill="{G}"/>',
    "Bersaglio colpito al centro da una freccia",
)

ILLUS["saladbag"] = svg(
    f'<rect x="120" y="150" width="240" height="320" rx="30" fill="{CREAM}" stroke="#E2D4C8" stroke-width="6"/>'
    f'<rect x="120" y="150" width="240" height="44" rx="14" fill="{M}"/>'
    + leaf(150, 300, 120, -30, G) + leaf(200, 380, 130, -60, GD) + leaf(170, 430, 140, -15, G)
    + leaf(230, 260, 110, 20, "#7CC79A") + leaf(240, 330, 100, -80, G)
    + f'<rect x="150" y="410" width="180" height="40" rx="10" fill="{O}"/>'
    f'<rect x="410" y="120" width="56" height="270" rx="28" fill="{CREAM}" stroke="{DARK}" stroke-width="8"/>'
    f'<rect x="428" y="230" width="20" height="170" rx="10" fill="{M}"/>'
    f'<circle cx="438" cy="420" r="48" fill="{M}" stroke="{DARK}" stroke-width="8"/>'
    f'<line x1="470" y1="170" x2="490" y2="170" stroke="{DARK}" stroke-width="6"/>'
    f'<line x1="470" y1="210" x2="490" y2="210" stroke="{DARK}" stroke-width="6"/>'
    f'<line x1="470" y1="250" x2="490" y2="250" stroke="{DARK}" stroke-width="6"/>',
    "Busta di insalata pronta accanto a un termometro",
)

ILLUS["leafcut"] = svg(
    leaf(80, 290, 380, -10, G)
    + f'<path d="M90 288 C 200 270, 330 262, 455 225" fill="none" stroke="{GD}" stroke-width="8" stroke-linecap="round"/>'
    + f'<line x1="300" y1="90" x2="250" y2="480" stroke="{M}" stroke-width="8" stroke-dasharray="18 14" stroke-linecap="round"/>'
    + f'<circle cx="395" cy="430" r="34" fill="none" stroke="{O}" stroke-width="14"/>'
    + f'<circle cx="460" cy="380" r="34" fill="none" stroke="{O}" stroke-width="14"/>'
    + f'<path d="M375 400 L300 300 M432 370 L330 290" stroke="{DARK}" stroke-width="14" stroke-linecap="round"/>',
    "Foglia di insalata con una linea di taglio e delle forbici",
)

ILLUS["thermogaps"] = svg(
    f'<rect x="90" y="110" width="60" height="270" rx="30" fill="{CREAM}" stroke="{DARK}" stroke-width="8"/>'
    f'<rect x="110" y="200" width="20" height="200" rx="10" fill="{M}"/>'
    f'<circle cx="120" cy="410" r="52" fill="{M}" stroke="{DARK}" stroke-width="8"/>'
    f'<path d="M200 330 C 250 300, 280 260, 320 280 S 400 340, 470 250" fill="none" stroke="{O}" stroke-width="8" stroke-dasharray="2 20" stroke-linecap="round"/>'
    f'<circle cx="210" cy="325" r="18" fill="{G}"/>'
    f'<circle cx="320" cy="280" r="18" fill="{CREAM}" stroke="{M}" stroke-width="6" stroke-dasharray="8 7"/>'
    f'<circle cx="400" cy="320" r="18" fill="{CREAM}" stroke="{M}" stroke-width="6" stroke-dasharray="8 7"/>'
    f'<circle cx="470" cy="250" r="18" fill="{G}"/>',
    "Termometro e una linea con rilevazioni mancanti",
)

SECTION_DECO = (
    f'<svg viewBox="0 0 900 900" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">'
    f'<circle cx="450" cy="450" r="400" fill="{O}" fill-opacity="0.95"/>'
    f'<circle cx="450" cy="450" r="300" fill="none" stroke="{CREAM}" stroke-opacity="0.35" stroke-width="22"/>'
    + leaf(420, 40, 150, -60, G) + leaf(420, 40, 120, -130, "#3C9C69")
    + "</svg>"
)

CHECK = (
    f'<svg viewBox="0 0 44 44" aria-label="Dentro"><circle cx="22" cy="22" r="22" fill="{G}"/>'
    f'<path d="M12 23 L19 30 L32 15" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
)
CROSS = (
    f'<svg viewBox="0 0 44 44" aria-label="Fuori"><circle cx="22" cy="22" r="22" fill="{M}"/>'
    f'<path d="M14 14 L30 30 M30 14 L14 30" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/></svg>'
)


def get(name):
    return ILLUS[name]
