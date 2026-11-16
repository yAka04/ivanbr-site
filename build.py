#!/usr/bin/env python3
"""
Gera o site estático em docs/ a partir de content.py e src/assets/.
Uso: python3 build.py
Sem dependências além do Python 3.8+.
"""
import json
import shutil
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import quote

from content import COMPANY, CUSTOM_DOMAIN, LANGS, MAKER_NAMES, PRODUCT_IMAGES, SITE_URL, TEXT

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "docs"
YEAR = date.today().year


def e(s):
    return escape(str(s), quote=True)


def wa_link(text):
    return f"https://wa.me/{COMPANY['whatsapp']}?text={quote(text)}"


# ---------------------------------------------------------------- partes

CHAT_ICON = (
    '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3h11A2.5 2.5 0 0 1 20 5.5v8a2.5 2.5 0 0 1-2.5 2.5H10l-4.2 3.6c-.5.4-1.3 0-1.3-.6V16A2.5 2.5 0 0 1 4 13.5z" '
    'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
)

VIA_MARK = (
    '<svg class="via" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
    '<circle cx="16" cy="16" r="11" fill="none" stroke="currentColor" stroke-width="6"/></svg>'
)


def drill_svg(t):
    """Ilustração técnica da microbroca: 4 regiões numeradas, linhas indicadoras
    ortogonais e dois detalhes ampliados (ponta e face da haste).
    Os números são referências de leitura, não uma sequência de processo."""
    Y = 196  # eixo da broca
    stripes = []
    x = 118
    while x < 560:
        stripes.append(f'<polygon points="{x},{Y-14} {x+11},{Y-14} {x+27},{Y+14} {x+16},{Y+14}"/>')
        x += 24
    # regiões (início, fim) e coluna da legenda
    regions = [(100, 122, 150), (122, 560, 450), (700, 760, 750), (1048, 1100, 1050)]
    nums = [op[0] for op in t["ops"]]
    marks = []
    for (a, b, col), n in zip(regions, nums):
        mid = (a + b) // 2
        side = 1 if col >= mid else -1
        marks.append(
            f'<path class="bracket" d="M{a},{Y+44} V{Y+50} H{b} V{Y+44}"/>'
            f'<path class="leader" d="M{mid},{Y+50} V{Y+60}"/>'
            f'<circle class="tag" cx="{mid}" cy="{Y+72}" r="12"/>'
            f'<text class="tag-num" x="{mid}" y="{Y+76}" text-anchor="middle">{n}</text>'
            f'<path class="leader" d="M{mid + side*12},{Y+72} H{col} V{Y+128}"/>'
        )
    # detalhe 01: ponta ampliada
    tip_stripes = "".join(
        f'<polygon points="{150+i*30},48 {164+i*30},48 {190+i*30},96 {176+i*30},96"/>' for i in range(4)
    )
    detail = t["ops_detail"]
    return f"""<svg class="drill-svg" viewBox="0 0 1200 330" role="img" aria-labelledby="drill-title">
  <title id="drill-title">{e(t['drill_alt'])}</title>
  <defs>
    <clipPath id="body-clip"><rect x="118" y="{Y-14}" width="442" height="28"/></clipPath>
    <clipPath id="tip-clip"><circle cx="165" cy="72" r="55"/></clipPath>
    <marker id="arr" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 1 L10 5 L0 9 z" fill="currentColor"/>
    </marker>
  </defs>
  <g class="insets">
    <text class="inset-label" x="165" y="10" text-anchor="middle">{e(detail)} {nums[0]}</text>
    <circle class="inset-bg" cx="165" cy="72" r="56"/>
    <g clip-path="url(#tip-clip)">
      <g class="metal"><polygon points="114,72 150,48 150,96"/><rect x="150" y="48" width="120" height="48"/></g>
      <g class="flutes">{tip_stripes}</g>
      <line class="axis" x1="100" y1="72" x2="230" y2="72"/>
    </g>
    <circle class="inset-ring" cx="165" cy="72" r="56"/>
    <circle class="inset-src" cx="111" cy="{Y}" r="18"/>
    <line class="inset-link" x1="118" y1="{Y-17}" x2="143" y2="123"/>

    <text class="inset-label" x="1040" y="10" text-anchor="middle">{e(detail)} {nums[3]}</text>
    <circle class="inset-bg" cx="1040" cy="72" r="56"/>
    <circle class="face-rim" cx="1040" cy="72" r="38"/>
    <circle class="mark" cx="1040" cy="72" r="32"/>
    <circle class="inset-ring" cx="1040" cy="72" r="56"/>
    <circle class="inset-src" cx="1074" cy="{Y}" r="22"/>
    <line class="inset-link" x1="1068" y1="{Y-21}" x2="1055" y2="126"/>
  </g>
  <line class="axis" x1="70" y1="{Y}" x2="1180" y2="{Y}"/>
  <g class="metal">
    <polygon points="100,{Y} 122,{Y-14} 122,{Y+14}"/>
    <rect x="122" y="{Y-14}" width="438" height="28"/>
    <polygon points="560,{Y-14} 640,{Y-32} 640,{Y+32} 560,{Y+14}"/>
    <rect x="640" y="{Y-32}" width="410" height="64"/>
  </g>
  <g class="flutes" clip-path="url(#body-clip)">{''.join(stripes)}</g>
  <g class="mark"><rect x="1048" y="{Y-32}" width="42" height="64"/><polygon points="1090,{Y-32} 1100,{Y-24} 1100,{Y+24} 1090,{Y+32}"/></g>
  <rect class="ring" x="700" y="{Y-42}" width="60" height="84" rx="5"/>
  <g class="dim">
    <line x1="1104" y1="{Y-32}" x2="1160" y2="{Y-32}"/><line x1="1104" y1="{Y+32}" x2="1160" y2="{Y+32}"/>
    <line class="dim-line" x1="1148" y1="{Y-30}" x2="1148" y2="{Y+30}" marker-start="url(#arr)" marker-end="url(#arr)"/>
    <text x="1148" y="{Y-48}" text-anchor="middle">{e(t['drill_dim'])}</text>
  </g>
  <g class="callout-marks">{''.join(marks)}</g>
</svg>"""

def header(t, lang, root, anchor_base=""):
    nav = "".join(f'<li><a href="{anchor_base}#{a}">{e(label)}</a></li>' for a, label in t["nav"])
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{root}{lang['path']}" aria-label="{e(COMPANY['brand'])}">{VIA_MARK}<span class="brand-name">IVAN</span><span class="brand-sub">International Trade</span></a>
    <nav class="nav" aria-label="{e(t['menu'])}"><ul>{nav}</ul></nav>
    <div class="header-actions">
      <a class="btn btn-gold btn-small" href="{e(wa_link(t['wa_hello']))}" target="_blank" rel="noopener">{CHAT_ICON}<span>{e(t['wa_short'])}</span></a>
      {lang_menu(t, lang, root)}
    </div>
    <details class="mobile-menu">
      <summary aria-label="{e(t['menu'])}">{MENU_ICON}<span class="menu-text">{e(t['menu'])}</span></summary>
      <div class="mobile-panel">
        <ul class="mobile-nav">{nav}</ul>
        <p class="mobile-lang-title">{e(t['lang_label'])}</p>
        {lang_switch(t, lang, root)}
      </div>
    </details>
  </div>
</header>"""


MENU_ICON = (
    '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M4 7h16M4 12h16M4 17h16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
)

DOTS_ICON = (
    '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<circle cx="12" cy="5" r="2" fill="currentColor"/><circle cx="12" cy="12" r="2" fill="currentColor"/>'
    '<circle cx="12" cy="19" r="2" fill="currentColor"/></svg>'
)

CHECK_ICON = (
    '<svg class="check" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
    '<path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.2" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)


def lang_menu(t, lang, root):
    """Botão de três pontinhos que abre a lista de idiomas."""
    items = []
    for l in LANGS:
        cur = l["code"] == lang["code"]
        attr = ' aria-current="true"' if cur else ""
        items.append(
            f'<li><a class="lang-link" href="{root}{l["path"]}" hreflang="{l["hreflang"]}" lang="{l["html_lang"]}"{attr}>'
            f'<span>{e(l["name"])}</span>{CHECK_ICON if cur else ""}</a></li>'
        )
    return f"""<details class="lang-menu">
        <summary title="{e(t['lang_label'])}"><span class="lang-code" aria-hidden="true">{e(lang['label'])}</span>{DOTS_ICON}<span class="sr-only">{e(t['lang_label'])}: {e(lang['name'])}</span></summary>
        <div class="lang-panel">
          <p class="lang-panel-title">{e(t['lang_label'])}</p>
          <ul>{''.join(items)}</ul>
        </div>
      </details>"""


def lang_switch(t, lang, root):
    items = []
    for l in LANGS:
        cur = ' aria-current="true"' if l["code"] == lang["code"] else ""
        items.append(
            f'<li><a class="lang-link" href="{root}{l["path"]}" hreflang="{l["hreflang"]}" lang="{l["html_lang"]}" title="{e(l["name"])}"{cur}>{e(l["name"])}</a></li>'
        )
    return f'<ul class="langs" aria-label="{e(t["lang_label"])}">{"".join(items)}</ul>'


def series_code(pid):
    return {"max-500": "MAX-500", "a01": "A01", "a02": "A02", "a03": "A03", "max600": "MAX600"}[pid]


def _flutes(x0, x1, yc, h, step=18):
    """Corpo da broca com canais helicoidais, de x0 a x1, centrado em yc."""
    t, b = yc - h / 2, yc + h / 2
    out = [f'<rect class="m" x="{x0}" y="{t}" width="{x1-x0}" height="{h}"/>']
    x = x0 - h
    while x < x1:
        out.append(f'<polygon class="fl" points="{x},{t} {x+8},{t} {x+8+h*0.7},{b} {x+h*0.7},{b}"/>')
        x += step
    return out


def drill_icon(kind):
    """Ícone de broca para a faixa de contexto: nova, gasta ou recuperada."""
    tip = ('<polygon class="m" points="14,30 24,24 24,36"/>' if kind != "worn"
           else '<polygon class="m" points="20,26 24,24 24,36 20,34"/>')
    out = ['<svg class="cyc-icon" viewBox="0 0 200 60" aria-hidden="true" focusable="false">',
           '<line class="ax" x1="4" y1="30" x2="196" y2="30"/>', tip,
           '<rect class="m" x="24" y="24" width="86" height="12"/>']
    out += [f'<polygon class="fl" points="{x},24 {x+5},24 {x+13},36 {x+8},36"/>' for x in range(26, 104, 12)]
    out += ['<polygon class="m" points="110,24 130,18 130,42 110,36"/>',
            '<rect class="m" x="130" y="18" width="58" height="24"/>']
    if kind == "worn":
        out += [f'<circle class="dust" cx="{x}" cy="{y}" r="2"/>' for x, y in [(12, 20), (8, 38), (40, 16), (66, 44), (90, 15)]]
    if kind == "new":
        out.append('<rect class="ring" x="146" y="13" width="10" height="34" rx="2"/>')
        out.append('<rect class="mk-red" x="182" y="18" width="6" height="24"/>')
    if kind == "worn":
        out.append('<rect class="ring" x="146" y="13" width="10" height="34" rx="2"/>')
        out.append('<rect class="mk-red" x="182" y="18" width="6" height="24"/>')
    if kind == "rec":
        out.append('<rect class="ring" x="146" y="13" width="10" height="34" rx="2"/>')
        out.append('<rect class="mk-blue" x="182" y="18" width="6" height="24"/>')
    out.append("</svg>")
    return "".join(out)


def op_art(i, tol="±0,02"):
    """Ilustrações técnicas das quatro operações (vetoriais, sem texto traduzível)."""
    svg = ['<svg class="op-art" viewBox="0 0 320 200" aria-hidden="true" focusable="false">',
           f'<defs><clipPath id="fc{i}"><rect x="0" y="0" width="320" height="200"/></clipPath></defs>']
    if i == 0:  # MAX-500: ponta no rebolo + câmera AOI
        svg += [f'<g clip-path="url(#fc{i})">',
                '<line class="ax" x1="80" y1="112" x2="320" y2="112"/>']
        svg += _flutes(130, 330, 112, 30)
        svg += ['<polygon class="m" points="96,112 130,97 130,127"/>',
                '<circle class="wheel" cx="62" cy="70" r="42"/>',
                '<circle class="wheel-hub" cx="62" cy="70" r="10"/>',
                '<path class="motion" d="M30 34 A48 48 0 0 1 98 30" marker-end="url(#ar)"/>',
                '<rect class="cam" x="150" y="160" width="46" height="26" rx="4"/>',
                '<rect class="cam" x="138" y="166" width="14" height="14" rx="2"/>',
                '<path class="view" d="M138 170 L100 118 M138 178 L100 122"/>',
                '<text class="lbl" x="200" y="178">AOI</text>',
                '</g>']
    elif i == 1:  # A01: escova em cima, faca de ar pulsante embaixo, partículas saindo
        svg += ['<line class="ax" x1="0" y1="104" x2="320" y2="104"/>']
        svg += _flutes(0, 320, 104, 40, 22)
        svg += ['<rect class="tool" x="90" y="22" width="140" height="18" rx="3"/>']
        svg += [f'<line class="bristle" x1="{x}" y1="40" x2="{x + 4}" y2="82"/>' for x in range(98, 226, 8)]
        svg += ['<path class="tool" d="M150 186 H210 L198 160 H162 Z"/>',
                '<path class="air" d="M170 154 V134 M180 154 V128 M190 154 V134"/>']
        svg += [f'<circle class="dust" cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in
                [(246, 62, 3), (262, 48, 2.5), (276, 70, 2), (238, 40, 2), (290, 52, 2.5), (254, 150, 2.5), (272, 166, 2), (288, 146, 2)]]
    elif i == 2:  # MAX600: anel entrando na haste, colocação/remoção e tolerância
        svg += ['<line class="ax" x1="0" y1="100" x2="320" y2="100"/>']
        svg += _flutes(0, 40, 100, 16, 14)
        svg += ['<polygon class="m" points="40,92 78,78 78,122 40,108"/>',
                '<rect class="m" x="78" y="78" width="250" height="44"/>',
                '<rect class="ring" x="150" y="68" width="30" height="64" rx="4"/>',
                '<rect class="ghost" x="236" y="68" width="30" height="64" rx="4"/>',
                '<path class="move" d="M190 100 H226" marker-start="url(#ar)" marker-end="url(#ar)"/>',
                '<path class="dimx" d="M150 140 V170 M78 140 V170"/>',
                '<path class="dimx" d="M80 162 H148" marker-start="url(#ar)" marker-end="url(#ar)"/>',
                f'<text class="lbl" x="114" y="188" text-anchor="middle">{tol} mm</text>']
    else:  # A02/A03: face da haste — cor antiga removida, cor nova aplicada
        svg += ['<circle class="rim" cx="92" cy="96" r="54"/>',
                '<circle class="old" cx="92" cy="96" r="44"/>',
                '<path class="wash" d="M62 66 L122 126 M74 58 L130 114 M54 78 L110 134"/>',
                '<path class="move" d="M160 96 H196" marker-end="url(#ar)"/>',
                '<circle class="rim" cx="252" cy="96" r="54"/>',
                '<circle class="mark" cx="252" cy="96" r="44"/>',
                '<line class="ax" x1="20" y1="96" x2="300" y2="96"/>',
                '<line class="ax" x1="92" y1="30" x2="92" y2="162"/>',
                '<line class="ax" x1="252" y1="30" x2="252" y2="162"/>']
    svg.insert(1, '<defs><marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="currentColor"/></marker></defs>')
    svg.append('</svg>')
    return "".join(svg).replace('id="ar"', f'id="ar{i}"').replace("url(#ar)", f"url(#ar{i})")


def hero(t, root):
    route = "".join(f'<li><span class="route-via" aria-hidden="true"></span>{e(c)}</li>' for c in t["route"])
    links = "".join(f'<li><a href="{e(h)}"><strong>{e(c)}</strong><span>{e(x)}</span></a></li>' for h, c, x in t["hero_links"])
    return f"""<section class="hero" aria-labelledby="hero-title">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <ol class="route" aria-label="{e(t['route_label'])}">{route}</ol>
      <h1 id="hero-title">{'<br>'.join(e(x) for x in t['hero_title'].split('|'))}</h1>
      <p class="lead">{e(t['hero_lead'])}</p>
      <div class="ctas">
        <a class="btn btn-gold" href="{e(wa_link(t['wa_hello']))}" target="_blank" rel="noopener">{CHAT_ICON}<span>{e(t['cta_wa'])}</span></a>
        <a class="btn btn-ghost" href="#segments">{e(t['cta_portfolio'])}</a>
      </div>
    </div>
    <figure class="hero-visual">
      <div class="hero-board">{board_svg("pcba")}</div>
      <figcaption>
        <span class="hc-label">{e(t['hero_card_label'])}</span>
        <ul class="hc-list">{links}</ul>
      </figcaption>
    </figure>
  </div>
</section>"""

def board_svg(kind):
    """Ilustrações originais: placa nua (PCB) e placa montada (PCBA)."""
    traces = [
        "M40 60 H120 L140 80 H220", "M40 100 H90 L110 120 H200 L220 140 H300",
        "M60 170 H150 L170 150 H250", "M240 60 V40 H320", "M300 90 V160 L280 180 H200",
        "M120 190 H300",
    ]
    vias = [(40, 60), (220, 80), (40, 100), (300, 140), (60, 170), (250, 150), (320, 40),
            (300, 90), (200, 180), (120, 190), (300, 190)]
    holes = [(30, 30), (330, 30), (30, 200), (330, 200)]
    out = ['<svg class="board" viewBox="0 0 360 230" aria-hidden="true" focusable="false">',
           '<rect x="4" y="4" width="352" height="222" rx="12" class="b-sub"/>',
           '<rect x="14" y="14" width="332" height="202" rx="8" class="b-silk"/>']
    out += [f'<path d="{d}" class="b-trace"/>' for d in traces]
    out += [f'<circle cx="{x}" cy="{y}" r="6" class="b-via"/>' for x, y in vias]
    out += [f'<circle cx="{x}" cy="{y}" r="7" class="b-hole"/>' for x, y in holes]
    if kind == "pcba":
        out += ['<rect x="128" y="58" width="78" height="78" rx="4" class="c-ic"/>',
                '<rect x="140" y="70" width="54" height="54" rx="2" class="c-ic-top"/>']
        for i in range(7):
            o = 136 + i * 10
            out += [f'<rect x="{o}" y="50" width="4" height="8" class="c-pin"/>',
                    f'<rect x="{o}" y="136" width="4" height="8" class="c-pin"/>',
                    f'<rect x="120" y="{o-70}" width="8" height="4" class="c-pin"/>',
                    f'<rect x="206" y="{o-70}" width="8" height="4" class="c-pin"/>']
        out += ['<rect x="236" y="96" width="34" height="14" rx="2" class="c-res"/>',
                '<rect x="236" y="120" width="34" height="14" rx="2" class="c-res"/>',
                '<circle cx="80" cy="140" r="16" class="c-cap"/><circle cx="80" cy="140" r="8" class="c-cap-top"/>',
                '<rect x="232" y="164" width="96" height="34" rx="3" class="c-conn"/>']
        out += [f'<rect x="{240 + i*14}" y="172" width="8" height="18" rx="1" class="c-conn-pin"/>' for i in range(6)]
        out += ['<rect x="44" y="40" width="44" height="24" rx="3" class="c-ic"/>']
    out.append("</svg>")
    return "".join(out)


ICONS = {
    # ícones de linha 24x24, desenhados para o site
    "process": '<path d="M7 3v6l-4 9a2 2 0 0 0 2 3h6"/><path d="M5 3h4"/><path d="M14 13h7v8h-7z"/><path d="M14 17h7"/><circle cx="17.5" cy="7" r="3"/>',
    "drill": '<path d="M9 3h6v5H9z"/><path d="M10 8h4l-1 9-1 4-1-4z"/><path d="M10.5 11l3 1M10.6 14l2.6 1"/>',
    "regrind": '<circle cx="8" cy="8" r="5"/><circle cx="8" cy="8" r="1.5"/><path d="M12 14l9 3-9 3z"/><path d="M4 2.5l1.5 1.5"/>',
    "pth": '<rect x="3" y="4" width="18" height="16" rx="1"/><path d="M3 9h18M3 15h18"/><path d="M10 4v16M14 4v16"/>',
    "print": '<path d="M4 15h16v5H4z"/><path d="M7 15V4h10v11"/><path d="M9 8h6M9 11h4"/>',
    "oven": '<rect x="2" y="7" width="20" height="10" rx="1"/><path d="M6 12h12"/><path d="M7 4c1 1 1 2 0 3M12 4c1 1 1 2 0 3M17 4c1 1 1 2 0 3"/>',
    "aoi": '<rect x="7" y="2" width="10" height="7" rx="1"/><path d="M12 9v2"/><path d="M8 21l4-10 4 10"/><path d="M3 21h18"/>',
    "eye": '<path d="M2 12s4-6 10-6 10 6 10 6-4 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "lab": '<path d="M9 3h6"/><path d="M10 3v6l-5 10a1.5 1.5 0 0 0 1.4 2h11.2a1.5 1.5 0 0 0 1.4-2L14 9V3"/><path d="M7 15h10"/>',
    "fixture": '<path d="M4 20V10h4v10M16 20V10h4v10"/><path d="M8 14h8"/><path d="M6 10V5M18 10V5"/><path d="M2 20h20"/>',
    "material": '<path d="M12 2l9 5-9 5-9-5z"/><path d="M3 12l9 5 9-5"/><path d="M3 17l9 5 9-5"/>',
    "line": '<rect x="2" y="13" width="20" height="4" rx="1"/><circle cx="6" cy="19.5" r="1.5"/><circle cx="18" cy="19.5" r="1.5"/><rect x="6" y="6" width="5" height="7"/><rect x="13" y="8" width="5" height="5"/>',
    "shield": '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
}


def icon(name):
    return (f'<svg class="pf-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" '
            f'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def recovery(t):
    ops = "".join(
        f'<li class="op-card"><div class="op-visual">{op_art(i, "±0,02" if t is TEXT["pt"] else "±0.02")}<span class="op-num" aria-hidden="true">{num}</span></div>'
        f'<div class="op-body"><h3 class="op-title"><span class="op-machine">{e(head)}</span> <span class="op-name">{e(machine)}</span></h3>'
        f'<p class="op-desc">{e(desc)}</p><p class="op-links">'
        + "".join(f'<a href="#{pid}">{e(label)}</a>' for label, pid in links)
        + '</p></div></li>'
        for i, (num, head, machine, desc, links) in enumerate(t["ops"])
    )
    cycle = "".join(
        f'<li>{drill_icon(kind)}<p class="cyc-title">{e(title)}</p><p class="cyc-text">{e(text)}</p></li>'
        for kind, (title, text) in zip(["new", "worn", "rec"], t["ops_cycle"])
    )
    return f"""<section id="recovery" class="section recovery" aria-labelledby="ops-title">
  <div class="wrap">
    <div class="ops">
      <div class="ops-head">
        <p class="ops-kicker">{e(t['ops_kicker'])}</p>
        <h2 id="ops-title">{e(t['ops_title'])}</h2>
        <p>{e(t['ops_lead'])}</p>
      </div>
      <ol class="cycle" aria-label="{e(t['ops_cycle_label'])}">{cycle}</ol>
      <ul class="ops-grid" aria-labelledby="ops-title">{ops}</ul>
    </div>
  </div>
</section>"""


def segments(t, root):
    def items(lst):
        out = []
        lst = [x for x in lst if x[2]] + [x for x in lst if not x[2]]
        for ic, name, desc in lst:
            link = ('<a class="pf-link" href="#equipment">' + e(t["cta_products"]) + '</a>') if ic == "regrind" else (
                f'<a class="pf-link" href="{e(wa_link(t["wa_item"].format(item=name)))}" target="_blank" rel="noopener">{e(t["seg_consult"])}</a>')
            if ic == "regrind":
                thumbs = "".join(
                    f'<a href="#{e(p["id"])}" aria-label="{e(p["name"])} ({e(p["series"])})"><img src="{root}assets/img/{PRODUCT_IMAGES[p["id"]][0]}" alt="" loading="lazy" width="96" height="72"></a>'
                    for p in t["products"])
                desc_extra = f'<div class="pf-thumbs">{thumbs}</div>'
            else:
                desc_extra = ""
            out.append(f'<li class="pf-item' + (' pf-item--feat' if desc else '') + f'">{icon(ic)}<h4>{e(name)}</h4>' + (f'<p>{e(desc)}</p>' if desc else '') + desc_extra + f'{link}</li>')
        return "".join(out)
    return f"""<section id="segments" class="section segments" aria-labelledby="seg-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="seg-title">{e(t['seg_title'])}</h2>
      <p>{e(t['seg_lead'])}</p>
    </div>
    <article id="portfolio-pcb" class="pf-block pf-pcb" aria-labelledby="seg-pcb-title">
      <header class="pf-head">
        <div>
          <p class="seg-code" aria-hidden="true">{e(t['seg_pcb_code'])}</p>
          <h3 id="seg-pcb-title">{e(t['seg_pcb_title'])} <span class="sr-only">({e(t['seg_pcb_code'])})</span></h3>
          <p>{e(t['seg_pcb_text'])}</p>
        </div>
        <div class="pf-art">{board_svg("pcb")}</div>
      </header>
      <ul class="pf-grid">{items(t['seg_pcb_items'])}</ul>
    </article>
    <article id="portfolio-pcba" class="pf-block pf-pcba" aria-labelledby="seg-pcba-title">
      <header class="pf-head">
        <div>
          <p class="seg-code" aria-hidden="true">{e(t['seg_pcba_code'])}</p>
          <h3 id="seg-pcba-title">{e(t['seg_pcba_title'])} <span class="sr-only">({e(t['seg_pcba_code'])})</span></h3>
          <p>{e(t['seg_pcba_text'])}</p>
        </div>
        <div class="pf-art">{board_svg("pcba")}</div>
      </header>
      <ul class="pf-grid">{items(t['seg_pcba_items'])}</ul>
    </article>
  </div>
</section>"""

def products(t, root, lang_code="pt"):
    rows, index = [], []
    for i, p in enumerate(t["products"]):
        img, w, h = PRODUCT_IMAGES[p["id"]]
        code = series_code(p["id"])
        hl = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in p["highlights"])
        spec_rows = [(t["maker_label"], MAKER_NAMES[p["id"]])] + list(p["specs"])
        specs = "".join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in spec_rows)
        alt = f"{t['photo_alt']} {p['name']} ({p['series']})" if lang_code != "zh" else f"{t['photo_alt']}{p['name']}（{p['series']}）"
        quote_text = t["wa_quote"].format(product=f"{p['name']} ({p['series']})")
        models = "".join(f"<li>{e(m)}</li>" for m in p["models"])
        feats = "".join(f"<li>{e(f)}</li>" for f in p["features"])
        flip = " product--flip" if i % 2 else ""
        index.append(
            f'<li><a href="#{p["id"]}"><span class="ci-img"><img src="{root}assets/img/{img}" width="{w}" height="{h}" alt="" loading="lazy" decoding="async"></span>'
            f'<span class="ci-code">{e(code)}</span><span class="ci-name">{e(p["name"])}</span></a></li>')
        rows.append(f"""<article id="{p['id']}" class="product{flip}" aria-labelledby="{p['id']}-title">
      <div class="product-visual">
        <span class="pv-code" aria-hidden="true">{e(code)}</span>
        <img src="{root}assets/img/{img}" width="{w}" height="{h}" alt="{e(alt)}" loading="lazy" decoding="async">
      </div>
      <div class="product-body">
        <p class="series">{e(p['series'])}</p>
        <h3 id="{p['id']}-title">{e(p['name'])}</h3>
        <p class="product-text">{e(p['text'])}</p>
        <dl class="highlights">{hl}</dl>
        <div class="product-meta">
          <div>
            <h4>{e(t['models_label'])}</h4>
            <ul class="models">{models}</ul>
          </div>
          <div>
            <h4>{e(t['features_label'])}</h4>
            <ul class="features">{feats}</ul>
          </div>
        </div>
        <div class="product-actions">
          <details class="specs">
            <summary>{e(t['specs_toggle'])}</summary>
            <table><tbody>{specs}</tbody></table>
          </details>
          <a class="btn btn-ink quote-btn" data-product="{p['id']}" href="{e(wa_link(quote_text))}" target="_blank" rel="noopener">{CHAT_ICON}<span>{e(t['quote'])}</span></a>
        </div>
      </div>
    </article>""")
    return f"""<section id="equipment" class="section products" aria-labelledby="prod-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="prod-title">{e(t['prod_title'])}</h2>
      <p>{e(t['prod_lead'])}</p>
    </div>
    <nav class="catalog-index" aria-label="{e(t['catalog_label'])}"><ul>{''.join(index)}</ul></nav>
    {''.join(rows)}
  </div>
</section>"""

def about(t):
    paras = "".join(f"<p>{e(p)}</p>" for p in t["about_text"])
    facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in t["about_facts"])
    nodes = "".join(
        f'<li><span class="net-via" aria-hidden="true"></span><p class="net-city">{e(city)}</p>'
        f'<p class="net-entity">{e(entity)}</p><p class="net-role">{e(role)}</p></li>'
        for city, entity, role in t["net_nodes"]
    )
    tl = "".join(
        f'<li><span class="via-dot" aria-hidden="true"></span><p class="year">{e(y)}</p><p class="tl-text">{e(txt)}</p></li>'
        for y, txt in t["timeline"]
    )
    title = "<br>".join(e(x) for x in t["about_title"].split("|"))
    return f"""<section id="company" class="section about" aria-labelledby="about-title">
  <div class="wrap">
    <div class="about-grid">
      <div class="about-text">
        <h2 id="about-title">{title}</h2>
        {paras}
      </div>
      <dl class="facts">{facts}</dl>
    </div>
    <div class="net" role="group" aria-labelledby="net-title">
      <h3 id="net-title" class="net-title">{e(t['net_title'])}</h3>
      <ol class="net-nodes">{nodes}</ol>
    </div>
  </div>
</section>
<section id="history" class="section history" aria-labelledby="hist-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="hist-title">{e(t['hist_title'])}</h2>
      <p>{e(t['hist_lead'])}</p>
    </div>
    <ol class="timeline">{tl}</ol>
  </div>
</section>"""

def customers(t, lang):
    groups = []
    for region, names in t["customers"]:
        is_country = region == t["cust_note_is_country"]
        items = []
        for name, extra in names:
            if extra and lang["code"] != "zh" and not is_country:
                items.append(f'<li>{e(name)} <span class="cn" lang="zh-CN">{e(extra)}</span></li>')
            elif extra:
                items.append(f'<li>{e(name)} <span class="cn">{e(extra)}</span></li>')
            else:
                items.append(f"<li>{e(name)}</li>")
        count = t["exp_count"].format(n=len(names))
        groups.append(
            f'<div class="exp-card"><div class="exp-head"><h3>{e(region)}</h3>'
            f'<span class="exp-count">{e(count)}</span></div>'
            f'<ul class="exp-names">{"".join(items)}</ul></div>')
    return f"""<section id="customers" class="section customers" aria-labelledby="cust-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="cust-title">{e(t['cust_title'])}</h2>
      <p>{e(t['cust_lead'])}</p>
    </div>
    <div class="exp-grid">{''.join(groups)}</div>
  </div>
</section>"""

def contact(t):
    f = t["form"]
    opts = "".join(f"<option>{e(o)}</option>" for o in f["options"])
    c = COMPANY
    return f"""<section id="contact" class="section contact" aria-labelledby="contact-title">
  <div class="wrap contact-grid">
    <div class="contact-info">
      <h2 id="contact-title">{e(t['cta_title'])}</h2>
      <p class="lead">{e(t['contact_lead'])}</p>
      <div class="contact-ctas">
        <a class="btn btn-gold btn-large" href="{e(wa_link(t['wa_hello']))}" target="_blank" rel="noopener">{CHAT_ICON}<span>{e(t['cta_wa'])}</span></a>
        <span class="contact-or">{e(t['cta_phone'])} <a href="tel:{c['phone_tel']}">{e(c['phone_display'])}</a></span>
      </div>
      <dl class="contact-list">
        <div><dt>{e(t['email_label'])}</dt><dd><a href="mailto:{e(c['email'])}">{e(c['email'])}</a></dd></div>
        <div><dt>{e(t['address_label'])}</dt><dd><address>{address_html(t)}</address>
          <a class="map-link" href="{e(c['maps'])}" target="_blank" rel="noopener">{e(t['map_link'])}</a></dd></div>
      </dl>
    </div>
    <form class="wa-form" id="wa-form" aria-labelledby="form-title" action="https://wa.me/{c['whatsapp']}" method="get" target="_blank"
          data-number="{c['whatsapp']}" data-tpl="{e(f['tpl'])}" data-tpl-company="{e(f['tpl_company'])}">
      <h3 id="form-title" class="form-title">{e(t['contact_title'])}</h3>
      <div class="field">
        <label for="f-name">{e(f['name'])}</label>
        <input id="f-name" name="name" type="text" autocomplete="name" required>
      </div>
      <div class="field">
        <label for="f-company">{e(f['company'])}</label>
        <input id="f-company" name="company" type="text" autocomplete="organization">
      </div>
      <div class="field">
        <label for="f-interest">{e(f['interest'])}</label>
        <select id="f-interest" name="interest" required>
          <option value="" disabled selected>{e(f['interest_placeholder'])}</option>
          {opts}
        </select>
      </div>
      <div class="field">
        <label for="f-message">{e(f['message'])}</label>
        <textarea id="f-message" name="message" rows="4"></textarea>
      </div>
      <input type="hidden" name="text" value="">
      <button class="btn btn-gold" type="submit">{CHAT_ICON}<span>{e(f['submit'])}</span></button>
      <p class="hint">{e(f['hint'])}</p>
    </form>
  </div>
</section>"""


def address_html(t):
    c = COMPANY
    return (f"{e(c['unit'])}, {e(c['street'])}<br>{e(c['condo'])}, {e(c['district'])}<br>"
            f"{e(c['city'])} – {e(c['state'])}, {e(c['zip'])}<br>{e(t['country'])}")


def footer(t, lang, root):
    c = COMPANY
    return f"""<footer class="site-footer">
  <div class="wrap footer-inner">
    <div>
      <p class="footer-brand">{VIA_MARK}<span>{e(c['brand'])}</span></p>
      <p>{e(c['legal'])}<br>CNPJ {e(c['cnpj'])}</p>
      <p class="small footer-group">{e(t['footer_group'])}</p>
    </div>
    <p>{address_html(t)}</p>
    <div>
      {lang_switch(t, lang, root)}
      <p class="small">© {YEAR} {e(c['brand'])}. {e(t['footer_rights'])}</p>
    </div>
  </div>
</footer>"""


def head(t, lang, root):
    c = COMPANY
    abs_ok = bool(SITE_URL)
    if abs_ok:
        page_url = f"{SITE_URL}/{lang['path']}"
        alts = "".join(
            f'<link rel="alternate" hreflang="{l["hreflang"]}" href="{SITE_URL}/{l["path"]}">' for l in LANGS
        ) + f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">'
        canon = f'<link rel="canonical" href="{page_url}">\n<meta property="og:url" content="{page_url}">'
        og_img = f"{SITE_URL}/assets/og-{lang['code']}.jpg"
    else:
        # Sem endereço definitivo: links relativos, sem canonical.
        alts = "".join(
            f'<link rel="alternate" hreflang="{l["hreflang"]}" href="{(root + l["path"]) or "./"}">' for l in LANGS
        )
        canon = ""
        og_img = f"{root}assets/og-{lang['code']}.jpg"
    ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": c["legal"],
        "alternateName": c["brand"],
        "legalName": c["legal"],
        "taxID": c["cnpj"],
        "description": t["footer_group"],
        "telephone": c["phone_tel"],
        "email": c["email"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": f"{c['street']}, {c['unit']}, {c['condo']}",
            "addressLocality": c["city"],
            "addressRegion": c["state"],
            "postalCode": c["zip"],
            "addressCountry": "BR",
        },
        "areaServed": ["BR", "South America"],
    }
    if abs_ok:
        ld["url"] = SITE_URL + "/"
        ld["logo"] = SITE_URL + "/assets/apple-touch-icon.png"
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['title'])}</title>
<meta name="description" content="{e(t['description'])}">
{canon}
{alts}
<meta name="theme-color" content="#0E3D30">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(c['brand'])}">
<meta property="og:title" content="{e(t['title'])}">
<meta property="og:description" content="{e(t['description'])}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{lang['html_lang'].replace('-', '_')}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{root}assets/fonts/archivo-latin-wdth-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/css/site.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>"""


def page(lang):
    t = TEXT[lang["code"]]
    root = "../" if lang["path"] else ""
    return f"""<!DOCTYPE html>
<html lang="{lang['html_lang']}">
<head>
{head(t, lang, root)}
</head>
<body>
<a class="skip" href="#main">{e(t['skip'])}</a>
{header(t, lang, root)}
<main id="main">
{hero(t, root)}
{segments(t, root)}
{recovery(t)}
{products(t, root, lang["code"])}
{about(t)}
{customers(t, lang)}
{contact(t)}
</main>
{footer(t, lang, root)}
<script src="{root}assets/js/site.js" defer></script>
</body>
</html>
"""


def page_404():
    t = TEXT["pt"]
    lang = LANGS[0]
    # O 404 é servido em qualquer caminho. O script descobre a raiz do site
    # (/ no domínio próprio, /repositorio/ no github.io) e corrige os links.
    body = header(t, lang, "./", anchor_base="./")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t['notfound_title'])} | {e(COMPANY['brand'])}</title>
<meta name="robots" content="noindex">
<script>
  (function () {{
    var seg = location.pathname.split("/")[1];
    var base = /\\.github\\.io$/.test(location.hostname) && seg ? "/" + seg + "/" : "/";
    document.write('<base href="' + base + '">');
  }})();
</script>
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body class="notfound">
{body}
<main id="main" class="hero">
  <div class="wrap">
    <h1>{e(t['notfound_title'])}</h1>
    <p class="lead">{e(t['notfound_text'])}</p>
    <p><a class="btn btn-gold" href="./">{e(t['notfound_link'])}</a></p>
  </div>
</main>
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""


def write_redirect(folder, target, html_lang):
    (OUT / folder).mkdir(exist_ok=True)
    (OUT / folder / "index.html").write_text(
        f'<!DOCTYPE html><html lang="{html_lang}"><head><meta charset="utf-8">'
        '<title>IVAN International Trade</title><meta name="robots" content="noindex">'
        f'<meta http-equiv="refresh" content="0; url={target}">'
        f'<script>location.replace("{target}" + location.hash);</script>'
        f'</head><body><a href="{target}">IVAN International Trade</a></body></html>\n',
        encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC / "assets", OUT / "assets")
    for lang in LANGS:
        d = OUT / lang["path"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page(lang), encoding="utf-8")
    (OUT / "404.html").write_text(page_404(), encoding="utf-8")
    # /pt/ leva para a versão em português (que fica na raiz), mantendo a seção (#...).
    write_redirect("pt", "../", "pt-BR")
    # A versão em chinês foi desativada: quem abrir um link antigo de /zh/ vai para a versão em português.
    if not any(l["code"] == "zh" for l in LANGS):
        write_redirect("zh", "../", "pt-BR")
    if CUSTOM_DOMAIN:
        (OUT / "CNAME").write_text(CUSTOM_DOMAIN + "\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    if not SITE_URL:
        (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
        print("Site gerado em", OUT, "(sem SITE_URL: sem sitemap e sem canonical)")
        return
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    urls = []
    for l in LANGS:
        alts = "".join(
            f'<xhtml:link rel="alternate" hreflang="{a["hreflang"]}" href="{SITE_URL}/{a["path"]}"/>' for a in LANGS
        )
        urls.append(f"<url><loc>{SITE_URL}/{l['path']}</loc>{alts}</url>")
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
        + "".join(urls) + "</urlset>\n",
        encoding="utf-8",
    )
    print("Site gerado em", OUT)


if __name__ == "__main__":
    main()
