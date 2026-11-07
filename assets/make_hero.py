# Builds hero-dark.svg / hero-light.svg: an animated iso-glow plate for the profile README.
# GitHub strips scripts from README images, so everything moves with CSS + SMIL only.
# run: python make_hero.py   (writes next to this file)
import math, os

C, S = math.cos(math.pi / 6), math.sin(math.pi / 6)
P = lambda x, y, z: ((x - y) * C, (x + y) * S - z)
D = P
def plane(O, U, V):
    o, u, v = P(*O), D(*U), D(*V)
    return f"matrix({u[0]:.4f} {u[1]:.4f} {v[0]:.4f} {v[1]:.4f} {o[0]:.2f} {o[1]:.2f})"
TOP   = lambda x, y, z: plane((x, y, z), (1, 0, 0), (0, 1, 0))
FRONT = lambda x, y, z: plane((x, y, z), (1, 0, 0), (0, 0, -1))
SIDE  = lambda x, y, z: plane((x, y, z), (0, -1, 0), (0, 0, -1))

def box(x, y, z, w, d, h, cls="face"):
    return (f'<g class="{cls}">'
            f'<rect class="top" transform="{TOP(x, y, z + h)}" width="{w}" height="{d}"/>'
            f'<rect transform="{FRONT(x, y + d, z + h)}" width="{w}" height="{h}"/>'
            f'<rect class="side" transform="{SIDE(x + w, y + d, z + h)}" width="{d}" height="{h}"/></g>')
def onface(T, inner): return f'<g transform="{T}">{inner}</g>'
def path(pts): return "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in (P(*p) for p in pts))


def barcss(rows, full):                          # rows of widths -> scaleX keyframes (CSS replaces SMIL <animate width>)
    out = ".bar { transform-box: fill-box; transform-origin: left center; transform: scaleX(.7); }\n"
    for i, v in enumerate(rows):
        vals = [float(a) / full for a in v.split(";")]
        n = len(vals) - 1
        out += f".b{i} {{ animation: bk{i} {2 + i}s linear infinite; }}\n@keyframes bk{i} {{ " + " ".join(
            f"{100 * j / n:g}% {{ transform: scaleX({x:.3f}); }}" for j, x in enumerate(vals)) + " }\n"
    return out
Z = 8
svg = []   # painted back to front (smaller x+y first)
svg.append(box(0, 0, 0, 420, 150, Z))                                                 # ground plate
svg.append(onface(TOP(0, 0, Z), '<rect class="detail" x="8" y="8" width="404" height="134" rx="6"/>'))

# server rack with live bars (back row)
svg.append(box(250, 0, Z, 60, 34, 92))
ROWS = ["14;40;22;48;14", "26;30;34;28;26", "36;37;36;38;36"]
bars = ''.join(f'<rect class="bar b{i}" x="6" y="{8 + i * 10}" width="48" height="5"/>' for i in range(3))
svg.append(onface(FRONT(250, 34, Z + 92), f'<rect class="glass" x="3" y="3" width="54" height="36" rx="2"/>{bars}'
                  + ''.join(f'<line class="detail" x1="{6 + i * 4}" y1="50" x2="{6 + i * 4}" y2="84"/>' for i in range(13))))

# guardian wheels: car, beacon, wire to the phone
for x, y in [(36, 40), (110, 40)]:
    a, b = P(x, y, Z + 9); svg.append(f'<ellipse class="tyre" cx="{a:.1f}" cy="{b:.1f}" rx="8" ry="9"/>')
svg.append(box(20, 40, Z + 8, 110, 56, 18))
svg.append(box(48, 46, Z + 26, 56, 44, 16))
svg.append(onface(FRONT(48, 90, Z + 42), ''.join(f'<line class="detail" x1="{6 + i * 4}" y1="4" x2="{6 + i * 4}" y2="12"/>' for i in range(11))))
svg.append(box(70, 62, Z + 42, 10, 10, 5, "face beacon"))
for x, y in [(36, 96), (110, 96)]:
    a, b = P(x, y, Z + 9); svg.append(f'<ellipse class="tyre" cx="{a:.1f}" cy="{b:.1f}" rx="8" ry="9"/>')
wire = path([(130, 70, Z + 14), (142, 72, Z + 1), (150, 86, Z + 1), (160, 96, Z + 8)])
svg.append(f'<path class="wire" d="{wire}"/><path class="pulse" pathLength="100" d="{wire}"/>')
svg.append(box(150, 96, Z, 34, 6, 56))                                                # phone
svg.append(onface(FRONT(150, 102, Z + 56), '<rect class="glass phone" x="3" y="3" width="28" height="44" rx="3"/>'
                  '<text class="scr" x="17" y="22" text-anchor="middle">ALERT</text>'))

# voice car: drives up to the 20 cm line, waits, backs off
svg.append(onface(TOP(0, 0, Z), '<line class="stopline" x1="370" y1="20" x2="370" y2="90"/>'))
dx, dy = D(122, 0, 0)
svg.append(f'<g class="rover">{box(200, 52, Z + 4, 48, 34, 12)}{box(212, 58, Z + 16, 18, 20, 4, "face bt")}</g>')
svg.append(box(380, 20, Z, 10, 70, 34))                                               # wall

# ecofloater: twin pontoons, deck, electronics, gnss mast, wake from the thrusters (front row)
wake = path([(292, 103, Z + 1), (268, 103, Z + 1), (236, 108, Z + 1)]) + " " + path([(292, 141, Z + 1), (268, 141, Z + 1), (236, 136, Z + 1)])
svg.append(f'<path class="wire" d="{wake}"/><path class="pulse" pathLength="100" d="{wake}"/>')
svg.append(box(296, 94, Z, 112, 18, 12))                                              # pontoons
svg.append(box(296, 132, Z, 112, 18, 12))
svg.append(box(302, 97, Z + 12, 100, 50, 4))                                          # deck
svg.append(box(318, 106, Z + 16, 38, 30, 12))                                         # electronics box
svg.append(box(323, 111, Z + 28, 12, 9, 2, "face bt"))                                # esp32 #1 blinking
svg.append(box(372, 120, Z + 16, 4, 4, 30))                                           # gnss mast
svg.append(box(366, 114, Z + 46, 15, 15, 4, "face beacon"))
svg.append(onface(FRONT(296, 150, Z + 12), '<text class="label" x="56" y="9" text-anchor="middle">ECOFLOATER</text>'))

# fit the scene into the left part of the card
pts = [P(x, y, z) for x in (0, 420) for y in (0, 150) for z in (0, 100)]
x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
BX, BY, BW, BH = 20, 44, 530, 276
k = min(BW / (x1 - x0), BH / (y1 - y0))
fit = f"translate({BX - x0 * k + (BW - (x1 - x0) * k) / 2:.1f} {BY - y0 * k:.1f}) scale({k:.4f})"
body = "\n".join(svg)

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
def page(dark):
    t = dict(panel="#0a0f14", face="#131b22", top="#18222b", side="#0f161c", line="#5d7383", detail="#22303b",
             ink="#d5e0e8", ink2="#71828f") if dark else \
        dict(panel="#eef2f3", face="#ffffff", top="#f9fbfb", side="#e6ecee", line="#2a2b2e", detail="#c9c8c2",
             ink="#1d1e20", ink2="#6b6d72")
    A = "#2dd4bf"   # "tide", same accent as the 3d lab
    glow = ".pulse, .bar, .stopline, .beacon rect, .bt rect, .phone { filter: url(#glow); }" if dark else ""   # light theme: no glow
    roverkf = (f".rover {{ transform-box: view-box; animation: drive 6s linear infinite; }}\n@keyframes drive {{ 0%, 100% {{ transform: translate(0px, 0px); }} 40%, 60% {{ transform: translate({dx:.1f}px, {dy:.1f}px); }} 95% {{ transform: translate(0px, 0px); }} }}\n")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 330" role="img" aria-label="Isometric plate of Varun's projects: a car with an alarm beacon, a voice-controlled rover, a server rack and a sealed crate marked patent pending.">
<defs><filter id="glow" filterUnits="userSpaceOnUse" x="-100" y="-100" width="1200" height="600"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>
  * {{ vector-effect: non-scaling-stroke; }}
  .bg {{ fill: {t["panel"]}; }}
  .face rect, .tyre {{ fill: {t["face"]}; stroke: {t["line"]}; stroke-width: 1; }}
  .face rect.top {{ fill: {t["top"]}; }} .face rect.side {{ fill: {t["side"]}; }}
  .detail {{ fill: none; stroke: {t["detail"]}; stroke-width: 1; }}
  .glass {{ fill: {t["side"]}; stroke: {t["detail"]}; stroke-width: 1; }}
  .wire {{ fill: none; stroke: {t["line"]}; stroke-width: 1.2; }}
  .pulse {{ fill: none; stroke: {A}; stroke-width: 2.4; stroke-linecap: round; stroke-dasharray: 14 86; animation: run 2.4s linear infinite; }}
  @keyframes run {{ from {{ stroke-dashoffset: 100; }} to {{ stroke-dashoffset: 0; }} }}
  .beacon rect {{ animation: blink 1.2s steps(1) infinite; }}
  .bt rect {{ animation: blink 1.5s steps(1) infinite; }}
  .phone {{ animation: lit 2.4s ease-in-out infinite; }}
  .lid rect {{ animation: seam 3s ease-in-out infinite; }}
  @keyframes blink {{ 0%, 49% {{ fill: {A}; stroke: {A}; }} 50%, 100% {{ fill: {t["face"]}; }} }}
  @keyframes lit {{ 0%, 55% {{ fill: {t["side"]}; }} 70%, 100% {{ fill: {A}; }} }}
  @keyframes seam {{ 0%, 100% {{ stroke: {t["line"]}; }} 50% {{ stroke: {A}; }} }}
  .stopline {{ fill: none; stroke: {A}; stroke-width: 1.2; stroke-dasharray: 4 3; }}
  .bar {{ fill: {A}; }}
{barcss(ROWS, 48)}{roverkf}
  {glow}
  .scr {{ fill: {t["panel"]}; font: 700 7px {MONO}; }}
  .label {{ fill: {t["ink2"]}; font: 700 8px {MONO}; letter-spacing: .8px; }}
  .name {{ fill: {t["ink"]}; font: 600 34px {MONO}; letter-spacing: -0.5px; }}
  .sub {{ fill: {t["ink2"]}; font: 14px {MONO}; }}
  .acc {{ fill: {A}; }}
  .fig {{ fill: {t["ink2"]}; font: 11px {MONO}; letter-spacing: 1px; }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<rect class="bg" width="900" height="330" rx="14"/>
<text class="fig" x="28" y="34">FIG 01 · ECOFLOATER AND FRIENDS</text>
<g transform="{fit}">
{body}
</g>
<text class="name" x="572" y="150">varun k kumar</text>
<text class="sub" x="572" y="178">ece grad · robots at scrapify ecotech</text>
<text class="sub" x="572" y="204"><tspan class="acc">▸</tspan> click for the 3d lab</text>
</svg>'''

here = os.path.dirname(os.path.abspath(__file__))
for name, dark in (("hero-dark.svg", True), ("hero-light.svg", False)):
    with open(os.path.join(here, name), "w", encoding="utf-8") as f:
        f.write(page(dark))
    print("wrote", name)
