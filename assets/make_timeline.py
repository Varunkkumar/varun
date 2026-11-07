# Builds timeline-dark.svg / timeline-light.svg: a self-drawing career line for the profile README. CSS only, transparent background.
# run: python make_timeline.py   (writes next to this file)
import os

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
A = "#2dd4bf"
STOPS = [("velammal", "ece"), ("first builds", "water level · voice car"), ("cmrl", "in-plant training"),
         ("chennai airport", "operations intern '23"), ("graduated", "b.e. ece"), ("scrapify ecotech", "now")]
X0, X1, Y, DRAW = 40, 860, 80, 55           # line extent, its y, and the % of the 9 s cycle spent drawing
XS = [90 + i * 144 for i in range(6)]       # stops evenly spaced, last one leaves room for its centred text

def page(dark):
    t = dict(face="#131b22", line="#5d7383", detail="#22303b", ink="#d5e0e8", ink2="#71828f") if dark else \
        dict(face="#ffffff", line="#2a2b2e", detail="#c9c8c2", ink="#1d1e20", ink2="#6b6d72")
    glow = ".prog, .now, .ring { filter: url(#glow); }" if dark else ""     # light theme: no glow
    css, body = "", []
    for i, ((a, b), x) in enumerate(zip(STOPS, XS)):
        p = max(0.5, (x - X0) / (X1 - X0) * DRAW)                           # when the line reaches this stop
        css += (f".s{i} {{ opacity: 1; transform-box: fill-box; transform-origin: center; animation: pop{i} 9s linear infinite both; }}\n"
                f"@keyframes pop{i} {{ 0%, {p - 0.1:.1f}% {{ opacity: 0; transform: scale(0); }} {p + 2:.1f}% {{ opacity: 1; transform: scale(1.35); }}"
                f" {p + 4:.1f}% {{ opacity: 1; transform: scale(1); }} 100% {{ opacity: 1; transform: scale(1); }} }}\n")
        last = i == len(STOPS) - 1
        ring = f'<circle class="ring" cx="{x}" cy="{Y}" r="6"/>' if last else ""
        body.append(f'<g class="s{i}">{ring}<circle class="{"now" if last else "dot"}" cx="{x}" cy="{Y}" r="{6 if last else 5}"/></g>')
        body.append(f'<g class="s{i}"><text class="t1" x="{x}" y="{Y + 26}" text-anchor="middle">{a}</text>'
                    f'<text class="t2" x="{x}" y="{Y + 42}" text-anchor="middle">{b}</text></g>')
    nl = "\n".join(body)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 190" width="900" height="190" role="img" aria-label="Timeline: velammal, first builds, cmrl, chennai airport, graduated, scrapify ecotech.">
<defs><filter id="glow" filterUnits="userSpaceOnUse" x="-50" y="-50" width="1000" height="300"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>
  * {{ vector-effect: non-scaling-stroke; }}
  .all {{ animation: life 9s linear infinite; }}
  @keyframes life {{ 0%, 94% {{ opacity: 1; }} 100% {{ opacity: 0; }} }}
  .base {{ fill: none; stroke: {t["line"]}; stroke-width: 1; stroke-dasharray: 100; animation: draw 9s linear infinite; }}
  @keyframes draw {{ 0% {{ stroke-dashoffset: 100; }} {DRAW}%, 100% {{ stroke-dashoffset: 0; }} }}
  .prog {{ fill: none; stroke: {A}; stroke-width: 2.4; stroke-linecap: round; stroke-dasharray: 5 95; stroke-dashoffset: 0; animation: go 9s linear infinite; }}
  @keyframes go {{ 0% {{ stroke-dashoffset: 0; opacity: 1; }} {DRAW}% {{ stroke-dashoffset: -95; opacity: 1; }} {DRAW + 3}%, 100% {{ stroke-dashoffset: -95; opacity: 0; }} }}
  .dot {{ fill: {t["face"]}; stroke: {t["line"]}; stroke-width: 1.2; }}
  .now {{ fill: {A}; stroke: {A}; }}
  .ring {{ fill: none; stroke: {A}; stroke-width: 1.5; transform-box: fill-box; transform-origin: center; animation: ring 2s ease-out infinite; }}
  @keyframes ring {{ from {{ transform: scale(1); opacity: .9; }} to {{ transform: scale(3.2); opacity: 0; }} }}
{css}  {glow}
  .t1 {{ fill: {t["ink"]}; font: 12px {MONO}; }}
  .t2 {{ fill: {t["ink2"]}; font: 10.5px {MONO}; }}
  .lab {{ fill: {t["ink2"]}; font: 10px {MONO}; letter-spacing: 1.5px; }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<text class="lab" x="40" y="30">THE ROAD SO FAR</text>
<g class="all">
<path class="base" pathLength="100" d="M{X0},{Y} L{X1},{Y}"/>
<path class="prog" pathLength="100" d="M{X0},{Y} L{X1},{Y}"/>
{nl}
</g>
</svg>'''

here = os.path.dirname(os.path.abspath(__file__))
for name, dark in (("timeline-dark.svg", True), ("timeline-light.svg", False)):
    with open(os.path.join(here, name), "w", encoding="utf-8") as f:
        f.write(page(dark))
    print("wrote", name)
