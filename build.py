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
    """Desenho técnico da broca. Partes alinhadas com as 4 colunas das legendas (150/450/750/1050)."""
    stripes = []
    x = 118
    while x < 560:
        stripes.append(f'<polygon points="{x},82 {x+11},82 {x+27},110 {x+16},110"/>')
        x += 24
    leaders = [
        ((112, 96), (150, 206)),
        ((430, 96), (450, 206)),
        ((730, 96), (750, 206)),
        ((1068, 96), (1050, 206)),
    ]
    leader_svg = "".join(
        f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>' for a, b in leaders
    )
    dots = "".join(f'<circle cx="{a[0]}" cy="{a[1]}" r="3.5"/>' for a, _ in leaders)
    return f"""<svg class="drill-svg" viewBox="0 0 1200 210" role="img" aria-labelledby="drill-title">
  <title id="drill-title">{e(t['drill_alt'])}</title>
  <defs>
    <clipPath id="body-clip"><rect x="118" y="82" width="442" height="28"/></clipPath>
    <marker id="arr" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 1 L10 5 L0 9 z" fill="currentColor"/>
    </marker>
  </defs>
  <line class="axis" x1="70" y1="96" x2="1180" y2="96"/>
  <g class="metal">
    <polygon points="100,96 122,82 122,110"/>
    <rect x="122" y="82" width="438" height="28"/>
    <polygon points="560,82 640,64 640,128 560,110"/>
    <rect x="640" y="64" width="410" height="64"/>
  </g>
  <g class="flutes" clip-path="url(#body-clip)">{''.join(stripes)}</g>
  <g class="mark"><rect x="1048" y="64" width="42" height="64"/><polygon points="1090,64 1100,72 1100,120 1090,128"/></g>
  <rect class="ring" x="700" y="54" width="60" height="84" rx="5"/>
  <g class="dim">
    <line x1="1104" y1="64" x2="1160" y2="64"/><line x1="1104" y1="128" x2="1160" y2="128"/>
    <line class="dim-line" x1="1148" y1="66" x2="1148" y2="126" marker-start="url(#arr)" marker-end="url(#arr)"/>
    <text x="1148" y="48" text-anchor="middle">{e(t['drill_dim'])}</text>
  </g>
  <g class="leaders">{leader_svg}</g>
  <g class="dots">{dots}</g>
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


def hero(t):
    callouts = "".join(
        f'<li><strong>{e(part)}</strong><span>{e(desc)}</span><a href="#{pid}">{e(model)}</a></li>'
        for part, desc, model, pid in t["callouts"]
    )
    return f"""<section class="hero" aria-labelledby="hero-title">
  <div class="wrap">
    <h1 id="hero-title">{'<br>'.join(e(x) for x in t['hero_title'].split('|'))}</h1>
    <div class="hero-row">
      <p class="lead">{e(t['hero_lead'])}</p>
      <div class="ctas">
        <a class="btn btn-gold" href="{e(wa_link(t['wa_hello']))}" target="_blank" rel="noopener">{CHAT_ICON}<span>{e(t['cta_wa'])}</span></a>
        <a class="btn btn-ghost" href="#equipment">{e(t['cta_products'])}</a>
      </div>
    </div>
    <figure class="drill">
      <figcaption>{e(t['drill_caption'])}</figcaption>
      {drill_svg(t)}
      <ul class="callouts">{callouts}</ul>
    </figure>
  </div>
</section>"""


def segments(t):
    pcb = "".join(f"<li>{e(i)}</li>" for i in t["seg_pcb_items"])
    pcba = "".join(f"<li>{e(i)}</li>" for i in t["seg_pcba_items"])
    return f"""<section id="segments" class="section segments" aria-labelledby="seg-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="seg-title">{e(t['seg_title'])}</h2>
      <p>{e(t['seg_lead'])}</p>
    </div>
    <div class="seg-grid">
      <article class="seg seg-pcb" aria-labelledby="seg-pcb-title">
        <p class="seg-code" aria-hidden="true">{e(t['seg_pcb_code'])}</p>
        <h3 id="seg-pcb-title">{e(t['seg_pcb_title'])} <span class="sr-only">({e(t['seg_pcb_code'])})</span></h3>
        <p>{e(t['seg_pcb_text'])}</p>
        <ul class="ticks two-col">{pcb}</ul>
      </article>
      <article class="seg seg-pcba" aria-labelledby="seg-pcba-title">
        <p class="seg-code" aria-hidden="true">{e(t['seg_pcba_code'])}</p>
        <h3 id="seg-pcba-title">{e(t['seg_pcba_title'])} <span class="sr-only">({e(t['seg_pcba_code'])})</span></h3>
        <p>{e(t['seg_pcba_text'])}</p>
        <ul class="ticks">{pcba}</ul>
      </article>
    </div>
  </div>
</section>"""


def products(t, root, lang_code="pt"):
    rows = []
    for i, p in enumerate(t["products"]):
        img, w, h = PRODUCT_IMAGES[p["id"]]
        hl = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in p["highlights"])
        spec_rows = [(t["maker_label"], MAKER_NAMES[p["id"]])] + list(p["specs"])
        specs = "".join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in spec_rows)
        alt = f"{t['photo_alt']} {p['name']} ({p['series']})" if lang_code != "zh" else f"{t['photo_alt']}{p['name']}（{p['series']}）"
        quote_text = t["wa_quote"].format(product=f"{p['name']} ({p['series']})")
        models = "".join(f"<li>{e(m)}</li>" for m in p["models"])
        feats = "".join(f"<li>{e(f)}</li>" for f in p["features"])
        loading = "eager" if i == 0 else "lazy"
        rows.append(f"""<article id="{p['id']}" class="product" aria-labelledby="{p['id']}-title">
      <div class="product-media">
        <img src="{root}assets/img/{img}" width="{w}" height="{h}" alt="{e(alt)}" loading="{loading}" decoding="async">
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
    {''.join(rows)}
  </div>
</section>"""


def about(t):
    paras = "".join(f"<p>{e(p)}</p>" for p in t["about_text"])
    facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in t["about_facts"])
    tl = "".join(
        f'<li><span class="via-dot" aria-hidden="true"></span><p class="year">{e(y)}</p><p class="tl-text">{e(txt)}</p></li>'
        for y, txt in t["timeline"]
    )
    return f"""<section id="company" class="section about" aria-labelledby="about-title">
  <div class="wrap">
    <div class="about-grid">
      <div class="about-text">
        <h2 id="about-title">{'<br>'.join(e(x) for x in t['about_title'].split('|'))}</h2>
        {paras}
      </div>
      <dl class="facts">{facts}</dl>
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
        groups.append(f'<div class="cust-group"><h3>{e(region)}</h3><ul>{"".join(items)}</ul></div>')
    return f"""<section id="customers" class="section customers" aria-labelledby="cust-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="cust-title">{e(t['cust_title'])}</h2>
      <p>{e(t['cust_lead'])}</p>
    </div>
    <div class="cust-grid">{''.join(groups)}</div>
  </div>
</section>"""


def contact(t):
    f = t["form"]
    opts = "".join(f"<option>{e(o)}</option>" for o in f["options"])
    c = COMPANY
    return f"""<section id="contact" class="section contact" aria-labelledby="contact-title">
  <div class="wrap contact-grid">
    <div class="contact-info">
      <h2 id="contact-title">{e(t['contact_title'])}</h2>
      <p class="lead">{e(t['contact_lead'])}</p>
      <dl class="contact-list">
        <div><dt>{e(t['phone_label'])}</dt><dd><a href="tel:{c['phone_tel']}">{e(c['phone_display'])}</a></dd></div>
        <div><dt>{e(t['address_label'])}</dt><dd><address>{address_html(t)}</address>
          <a class="map-link" href="{e(c['maps'])}" target="_blank" rel="noopener">{e(t['map_link'])}</a></dd></div>
      </dl>
    </div>
    <form class="wa-form" id="wa-form" action="https://wa.me/{c['whatsapp']}" method="get" target="_blank"
          data-number="{c['whatsapp']}" data-tpl="{e(f['tpl'])}" data-tpl-company="{e(f['tpl_company'])}">
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
        og_img = f"{SITE_URL}/assets/og.jpg"
    else:
        # Sem endereço definitivo: links relativos, sem canonical.
        alts = "".join(
            f'<link rel="alternate" hreflang="{l["hreflang"]}" href="{(root + l["path"]) or "./"}">' for l in LANGS
        )
        canon = ""
        og_img = f"{root}assets/og.jpg"
    ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": c["legal"],
        "alternateName": c["brand"],
        "legalName": c["legal"],
        "taxID": c["cnpj"],
        "description": t["footer_group"],
        "telephone": c["phone_tel"],
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
{hero(t)}
{segments(t)}
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
    (OUT / "pt").mkdir(exist_ok=True)
    (OUT / "pt" / "index.html").write_text(
        '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
        '<title>IVAN International Trade</title><meta name="robots" content="noindex">'
        '<meta http-equiv="refresh" content="0; url=../">'
        '<script>location.replace("../" + location.hash);</script>'
        '</head><body><a href="../">IVAN International Trade</a></body></html>\n',
        encoding="utf-8")
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
