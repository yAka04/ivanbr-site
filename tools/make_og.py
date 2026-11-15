"""Gera as imagens de prévia (WhatsApp, LinkedIn etc.) em src/assets/og-<idioma>.jpg.

O texto fica numa coluna central de ~600 px: o WhatsApp mostra a miniatura
cortada em quadrado no centro, então nada importante pode ficar nas laterais.
Uso: python3 tools/make_og.py  (precisa de Playwright + Chromium).
"""
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from build import VIA_MARK, board_svg  # noqa: E402

TEXTS = {
    "pt": ("Equipamentos para a indústria de PCB e PCBA", "Suporte técnico local no Brasil", ["Hong Kong", "Shenzhen", "Valinhos"]),
    "en": ("Equipment for the PCB and PCBA industry", "Local technical support in Brazil", ["Hong Kong", "Shenzhen", "Valinhos"]),
    # "zh": ("PCB 与 PCBA 产业设备", "巴西本地技术支持", ["香港", "深圳", "巴西 Valinhos"]),  # versão em chinês desativada
}

CSS = (ROOT / "src/assets/css/site.css").read_text(encoding="utf-8")
FONTS = (ROOT / "src/assets/fonts").as_uri()
PATTERN = (ROOT / "src/assets/img/pcb-traces.svg").as_uri()


def page(lang):
    title, sub, route = TEXTS[lang]
    route_html = "".join(f"<li>{r}</li>" for r in route)
    cjk = lang == "zh"
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>
@font-face {{ font-family: Archivo; src: url({FONTS}/archivo-latin-wdth-normal.woff2) format("woff2"); font-weight: 100 900; font-stretch: 62% 125%; }}
@font-face {{ font-family: Archivo; src: url({FONTS}/archivo-latin-ext-wdth-normal.woff2) format("woff2"); font-weight: 100 900; font-stretch: 62% 125%; unicode-range: U+0100-024F, U+1E00-1EFF; }}
{CSS}
html, body {{ margin: 0; width: 1200px; height: 630px; overflow: hidden; }}
body {{ background: #0E3D30; font-family: Archivo, "Noto Sans CJK SC", "Noto Sans CJK TC", sans-serif; color: #F2F5F1; position: relative; }}
.bg {{ position: absolute; inset: 0; background: url({PATTERN}) repeat; background-size: 520px auto; opacity: .55; }}
.glow {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 45%, rgba(24,96,74,.95) 0%, rgba(14,61,48,0) 62%); }}
.side {{ position: absolute; top: 175px; width: 330px; }}
.side.l {{ left: -70px; transform: rotate(-8deg); }}
.side.r {{ right: -70px; transform: rotate(8deg); }}
.side .board {{ width: 100%; height: auto; display: block; filter: drop-shadow(0 30px 40px rgba(3,18,13,.5)); }}
.col {{ position: absolute; left: 300px; width: 600px; top: 0; bottom: 0; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }}
.brand {{ display: flex; align-items: center; gap: 12px; font-size: 30px; font-weight: 800; font-stretch: 112%; letter-spacing: .04em; }}
.brand svg {{ width: 34px; height: 34px; }}
.brand small {{ font-size: 17px; font-weight: 500; letter-spacing: 0; opacity: .75; border-left: 1px solid rgba(242,245,241,.35); padding-left: 12px; }}
h1 {{ margin: 34px 0 0; font-size: {64 if cjk else 54}px; line-height: 1.08; font-weight: {700 if cjk else 750}; font-stretch: {100 if cjk else 112}%; letter-spacing: {'.02em' if cjk else '-.01em'}; }}
p {{ margin: 22px 0 0; font-size: 28px; font-weight: 600; color: #D9AE3F; }}
ol {{ list-style: none; display: flex; gap: 0; margin: 30px 0 0; padding: 0; font-size: 19px; font-weight: 600; color: rgba(242,245,241,.8); }}
ol li {{ display: flex; align-items: center; }}
ol li + li::before {{ content: ""; width: 34px; height: 2px; background: #D9AE3F; margin: 0 12px; }}
</style></head><body>
<div class="bg"></div><div class="glow"></div>
<div class="side l">{board_svg("pcb")}</div>
<div class="side r">{board_svg("pcba")}</div>
<div class="col">
  <div class="brand">{VIA_MARK}<span>IVAN</span><small>International Trade</small></div>
  <h1>{title}</h1>
  <p>{sub}</p>
  <ol>{route_html}</ol>
</div>
</body></html>"""


async def main():
    from playwright.async_api import async_playwright
    tmp = ROOT / "tools" / "_og.html"
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        for lang in TEXTS:
            tmp.write_text(page(lang), encoding="utf-8")
            await pg.goto(tmp.as_uri(), wait_until="networkidle")
            await pg.evaluate("document.fonts.ready")
            out = ROOT / "src/assets" / f"og-{lang}.jpg"
            await pg.screenshot(path=str(out), type="jpeg", quality=88)
            print("ok", out)
        await b.close()
    tmp.unlink()


if __name__ == "__main__":
    asyncio.run(main())
