"""Gera o padrão de trilhas de placa (src/assets/img/pcb-traces.svg). Rodar uma vez."""
import random
from pathlib import Path
random.seed(7)
W = H = 720
G = 24
parts = []
used = set()
for _ in range(46):
    x = random.randrange(1, W // G) * G
    y = random.randrange(1, H // G) * G
    pts = [(x, y)]
    d = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    for _ in range(random.randint(2, 4)):
        L = random.randint(2, 7) * G
        x += d[0] * L; y += d[1] * L
        pts.append((x, y))
        # dobra a 45 graus
        if random.random() < 0.7:
            s = random.choice([-1, 1]) * G
            if d[0]:
                x += d[0] * G; y += s
            else:
                x += s; y += d[1] * G
            pts.append((x, y))
    path = "M" + " L".join(f"{px},{py}" for px, py in pts)
    parts.append(f'<path d="{path}"/>')
    for (px, py) in (pts[0], pts[-1]):
        parts.append(f'<circle cx="{px}" cy="{py}" r="5"/>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       f'<g fill="none" stroke="#D9AE3F" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{"".join(p for p in parts if p.startswith("<path"))}</g>'
       f'<g fill="#0E3D30" stroke="#D9AE3F" stroke-width="1.6">{"".join(p for p in parts if p.startswith("<circle"))}</g></svg>')
Path(__file__).resolve().parent.parent.joinpath("src/assets/img/pcb-traces.svg").write_text(svg)
print(len(svg))
