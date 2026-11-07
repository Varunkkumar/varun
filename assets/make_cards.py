# Builds assets/cards/<id>-dark.svg and <id>-light.svg: 13 animated iso-glow project cards for the profile README.
# Same kernel and tokens as make_hero.py. CSS + SMIL only (GitHub strips scripts). run: python make_cards.py
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

def box(x, y, z, w, d, h, cls="face", d0=None):
    st = f' style="--d:{d0}s"' if d0 is not None else ""       # --d = animation-delay for blinking boxes
    return (f'<g class="{cls}"{st}>'
            f'<rect class="top" transform="{TOP(x, y, z + h)}" width="{w}" height="{d}"/>'
            f'<rect transform="{FRONT(x, y + d, z + h)}" width="{w}" height="{h}"/>'
            f'<rect class="side" transform="{SIDE(x + w, y + d, z + h)}" width="{d}" height="{h}"/></g>')
def onface(T, inner): return f'<g transform="{T}">{inner}</g>'
def path(pts): return "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in (P(*p) for p in pts))
def pulse(pts, d0=0, cls="pulse"):
    d = path(pts)
    return f'<path class="wire" d="{d}"/><path class="{cls}" style="--d:{d0}s" pathLength="100" d="{d}"/>'

XCSS = []
def barcss(rows, full):                          # rows of widths -> scaleX keyframes (CSS replaces SMIL <animate width>)
    out = ".bar { transform-box: fill-box; transform-origin: left center; transform: scaleX(.7); }\n"
    for i, v in enumerate(rows):
        vals = [float(a) / full for a in v.split(";")]
        n = len(vals) - 1
        out += f".b{i} {{ animation: bk{i} {2 + i}s linear infinite; }}\n@keyframes bk{i} {{ " + " ".join(
            f"{100 * j / n:g}% {{ transform: scaleX({x:.3f}); }}" for j, x in enumerate(vals)) + " }\n"
    return out
def lines(rows): return ''.join(f'<line class="detail" x1="{a}" y1="{b}" x2="{c}" y2="{d}"/>' for a, b, c, d in rows)

# ── models: each returns (svg parts, (x0, x1, y0, y1, z0, z1) bounds in model units) ──
def m_ef():
    s = [pulse([(0, 9, 1), (-20, 9, 1), (-36, 14, 1)]), pulse([(0, 59, 1), (-20, 59, 1), (-36, 54, 1)], 0.4),
         box(0, 0, 0, 110, 18, 12), box(0, 50, 0, 110, 18, 12), box(6, 3, 12, 98, 62, 4),
         box(30, 20, 16, 36, 28, 14), box(84, 32, 16, 4, 4, 42), box(79, 27, 58, 14, 14, 3, "face blink")]
    return s, (-36, 110, 0, 68, 0, 62)
def m_ros():
    s = []
    for i in range(10):
        a = 2 * math.pi * i / 10
        s.append(onface(TOP(0, 0, 0), f'<circle class="dotc" style="--d:{i * 0.2:.1f}s" cx="{50 + 80 * math.cos(a):.1f}" cy="{50 + 80 * math.sin(a):.1f}" r="4.5"/>'))
    s += [box(0, 0, 0, 100, 100, 16), box(35, 35, 16, 30, 30, 10)]
    return s, (-35, 135, -35, 135, 0, 26)
def m_gw():
    tyre = lambda x, y: f'<ellipse class="tyre" cx="{P(x, y, 10)[0]:.1f}" cy="{P(x, y, 10)[1]:.1f}" rx="8" ry="9"/>'
    s = [tyre(18, 0), tyre(82, 0), box(0, 0, 6, 100, 50, 16), box(22, 6, 22, 52, 38, 14), box(40, 20, 36, 8, 8, 4, "face blink"),
         tyre(18, 50), tyre(82, 50), pulse([(100, 25, 12), (115, 35, 1), (125, 52, 1), (135, 52, 6)]),
         box(130, 44, 0, 30, 6, 50),
         onface(FRONT(130, 50, 50), '<rect class="glass phone" x="3" y="3" width="24" height="40" rx="3"/>')]
    return s, (0, 160, 0, 56, 0, 50)
def m_vc():
    dx, dy = D(78, 0, 0)
    XCSS.append(f".rover {{ transform-box: view-box; animation: drive 6s linear infinite; }}\n@keyframes drive {{ 0%, 100% {{ transform: translate(0px, 0px); }} 40%, 60% {{ transform: translate({dx:.1f}px, {dy:.1f}px); }} 95% {{ transform: translate(0px, 0px); }} }}\n")
    s = [box(-10, -10, 0, 180, 80, 3), onface(TOP(0, 0, 3), '<line class="stopline" x1="115" y1="0" x2="115" y2="60"/>'),
         f'<g class="rover">{box(0, 14, 3, 40, 30, 10)}{box(10, 20, 13, 16, 18, 4, "face blink")}</g>', box(150, 0, 3, 8, 60, 26)]
    return s, (-10, 170, -10, 70, 0, 29)
def m_srm():
    XCSS.append(barcss(["8;28;14;30;8", "16;20;24;18;16", "24;25;24;26;24"], 30))
    bars = ''.join(f'<rect class="bar b{i}" x="6" y="{9 + i * 12}" width="30" height="6"/>' for i in range(3))
    s = [box(0, 0, 0, 50, 34, 80),
         onface(FRONT(0, 34, 80), f'<rect class="glass" x="3" y="3" width="44" height="42" rx="2"/>{bars}' + lines([(6 + i * 4, 54, 6 + i * 4, 74) for i in range(11)])),
         pulse([(50, 17, 6), (75, 20, 1), (90, 30, 1), (100, 32, 6)]), box(100, 22, 0, 32, 22, 14),
         onface(TOP(100, 22, 14), '<path class="detail" d="M0,0 L16,10 L32,0 M0,22 L12,9 M32,22 L20,9"/>')]
    return s, (0, 132, 0, 44, 0, 80)
def m_ah():
    chk = ''.join(f'<rect class="chk" x="8" y="{7 + i * 12}" width="8" height="8"/><rect class="chkf" style="--d:{i * 0.8}s" x="8" y="{7 + i * 12}" width="8" height="8"/>'
                  + f'<line class="detail" x1="22" y1="{11 + i * 12}" x2="{44 + 6 * i}" y2="{11 + i * 12}"/>' for i in range(3))
    s = [box(105, 0, 0, 36, 36, 26), onface(FRONT(105, 36, 26), lines([(4, 8, 32, 8), (4, 16, 32, 16)])),
         pulse([(70, 40, 2), (88, 34, 1), (105, 24, 6)]), pulse([(122, 36, 1), (122, 48, 1), (118, 60, 1)], 1.0),
         box(0, 20, 0, 70, 50, 4), box(0, 20, 4, 70, 4, 44),
         onface(FRONT(0, 24, 48), f'<rect class="glass" x="3" y="3" width="64" height="38" rx="2"/>{chk}'),
         box(105, 60, 0, 22, 5, 38), onface(FRONT(105, 65, 38), '<rect class="glass phone" x="2" y="2" width="18" height="30" rx="2"/>')]
    return s, (0, 141, 0, 70, 0, 48)
def m_map():
    g = lines([(x, 10, x, 100) for x in range(0, 161, 20)] + [(0, y, 160, y) for y in range(10, 101, 20)])
    s = [box(0, 0, 0, 160, 110, 4), onface(TOP(0, 0, 4), g), pulse([(23, 23, 5), (103, 23, 5), (103, 83, 5)]),
         box(20, 20, 4, 6, 6, 16, "face acc"), box(30, 30, 4, 30, 20, 10), box(60, 60, 4, 30, 30, 12),
         box(110, 30, 4, 30, 20, 14), box(30, 70, 4, 20, 20, 8), box(100, 80, 4, 6, 6, 16, "face acc")]
    return s, (0, 160, 0, 110, 0, 20)
def m_wl():
    XCSS.append(".water-g { transform-box: view-box; animation: rise 6s linear infinite; }\n@keyframes rise { 0%, 100% { transform: translate(0px, 0px); } 50% { transform: translate(0px, -26px); } }\n")
    water = onface(TOP(0, 0, 14), '<rect class="water" x="3" y="3" width="67" height="67"/>')
    s = [box(0, 0, 0, 70, 70, 4), box(0, 0, 4, 70, 3, 56), box(0, 3, 4, 3, 67, 56),
         f'<g class="water-g">{water}</g>',
         box(0, 67, 4, 3, 3, 56), box(67, 67, 4, 3, 3, 56), box(67, 0, 4, 3, 3, 56)]
    s += [box(95, 4 + i * 16, 0, 10, 10, 8, "face blink", i * 0.5) for i in range(4)]
    return s, (0, 105, 0, 70, 0, 60)
def m_vis():
    dx, dy = D(115, 0, 0)
    XCSS.append(f".item {{ transform-box: view-box; animation: slide 5s linear infinite; animation-delay: var(--d, 0s); }}\n@keyframes slide {{ from {{ transform: translate(0px, 0px); }} to {{ transform: translate({dx:.1f}px, {dy:.1f}px); }} }}\n")
    item = lambda w, h, t: f'<g class="item" style="--d:{t}s">{box(5, 41, 8, w, 10, h)}</g>'
    s = [box(65, 22, 0, 5, 5, 50), box(0, 30, 0, 150, 34, 8), onface(TOP(0, 30, 8), lines([(x, 0, x, 34) for x in range(6, 150, 8)])),
         item(10, 22, -0.1), item(14, 12, -2.6), box(65, 66, 0, 5, 5, 50), box(65, 22, 46, 5, 49, 5),
         box(62, 38, 36, 12, 14, 10, "face blink")]
    return s, (0, 150, 22, 71, 0, 51)
def m_llm():
    slots = ''.join(f'<rect class="detail" x="5" y="{6 + i * 12}" width="30" height="8"/>' for i in range(4))
    curve = "M6,8 C12,9 14,27 24,29 S40,36 62,37"
    s = [box(0, 0, 0, 40, 40, 80), onface(FRONT(0, 40, 80), slots), box(94, 25, 0, 10, 4, 6), box(64, 24, 6, 70, 6, 46),
         onface(FRONT(64, 30, 52), f'<rect class="glass" x="3" y="3" width="64" height="38" rx="2"/>'
                f'<path class="draw" pathLength="100" d="{curve}"/>')]
    return s, (0, 134, 0, 40, 0, 80)
def m_imu():
    cx, cy = P(50, 35, 5)
    board = (box(0, 0, 4, 100, 70, 4) + onface(TOP(0, 0, 8), lines([(10, 55, 90, 55), (10, 62, 60, 62), (43, 29, 60, 29)]))
             + box(15, 14, 8, 28, 28, 6) + box(60, 20, 8, 18, 18, 4) + box(80, 52, 8, 8, 8, 3, "face blink"))
    s = [box(45, 30, -14, 10, 10, 14),
         f'<g class="rock">{board}</g>']
    XCSS.append(".rock { transform-box: fill-box; transform-origin: center; animation: rock 4s linear infinite; }\n@keyframes rock { 0%, 100% { transform: rotate(-4deg); } 50% { transform: rotate(4deg); } }\n")
    return s, (0, 100, 0, 70, -14, 14)
def m_k8s():
    s = [box(50 * i, 0, 0, 40, 34, 22) for i in range(3)]
    s += [pulse([(20 + 50 * i, 60, 6), (20 + 50 * i, 47, 1), (20 + 50 * i, 34, 3)], i * 0.5) for i in range(3)]
    s += [box(50 * i + 6 + 20 * j, 8, 22, 8, 8, 4, "face blink", 0.3 * (i * 2 + j)) for i in range(3) for j in range(2)]
    s.append(box(0, 60, 0, 140, 22, 8))
    s.append(onface(FRONT(0, 82, 8), ''.join(f'<rect class="detail" x="{8 + i * 17}" y="2" width="9" height="3"/>' for i in range(8))))
    return s, (0, 140, 0, 82, 0, 26)
def m_ids():
    s = [pulse([(30, 9, 6), (60, 9, 6)]), pulse([(30, 21, 6), (60, 21, 6)], 0.3, "pulse atk"), box(0, 0, 0, 30, 30, 20), box(60, 0, 0, 16, 30, 34, "face blink"),
         pulse([(76, 9, 6), (98, 4, 1), (120, 2, 6)], 0.8), pulse([(76, 21, 6), (98, 42, 1), (120, 41, 5)], 1.2),
         box(120, -10, 0, 26, 22, 30), box(120, 30, 0, 32, 22, 10)]
    return s, (0, 154, -10, 52, 0, 34)

CARDS = [("ef", "EcoFloater", "autonomous boat", m_ef, 1), ("ros", "ROS 2 vacuum", "robotics", m_ros, 1),
         ("gw", "Guardian Wheels", "gsm · bluetooth · android", m_gw, 1), ("vc", "Voice car", "arduino · voice · bluetooth", m_vc, 1),
         ("srm", "Server monitor", "bash · linux · smtp", m_srm, 1), ("ah", "AchiveHub", "react · typescript · mongodb", m_ah, 1),
         ("map", "Route map", "leaflet · openrouteservice", m_map, 1), ("wl", "Water level", "sensors · leds", m_wl, 1),
         ("vis", "Edge vision", "edge ai · object detection", m_vis, 0), ("llm", "Fine-tuning rig", "llm · lora · fine-tuning", m_llm, 0),
         ("imu", "Sensor fusion", "stm32 · imu · filters", m_imu, 0), ("k8s", "Homelab cluster", "kubernetes · ci/cd", m_k8s, 0),
         ("ids", "Intrusion detection", "ml · networking", m_ids, 0)]

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
A = "#2dd4bf"
def card(n, cid, title, tag, model, live, dark):
    t = dict(panel="#0a0f14", face="#131b22", top="#18222b", side="#0f161c", line="#5d7383", detail="#22303b", ink="#d5e0e8", ink2="#71828f") if dark else \
        dict(panel="#eef2f3", face="#ffffff", top="#f9fbfb", side="#e6ecee", line="#2a2b2e", detail="#c9c8c2", ink="#1d1e20", ink2="#6b6d72")
    XCSS.clear()
    parts, (bx0, bx1, by0, by1, bz0, bz1) = model()
    pts = [P(x, y, z) for x in (bx0, bx1) for y in (by0, by1) for z in (bz0, bz1)]
    x0, x1, y0, y1 = min(p[0] for p in pts), max(p[0] for p in pts), min(p[1] for p in pts), max(p[1] for p in pts)
    BX, BY, BW, BH = 20, 34, 320, 152
    k = min(BW / (x1 - x0), BH / (y1 - y0))
    fit = f"translate({BX - x0 * k + (BW - (x1 - x0) * k) / 2:.1f} {BY - y0 * k + (BH - (y1 - y0) * k) / 2:.1f}) scale({k:.4f})"
    glow = ".pulse, .bar, .stopline, .blink rect, .dotc, .phone, .draw, .acc rect, .chkf, .water { filter: url(#glow); }" if dark else ""
    txt, w = ("live in 3d ▸", 84) if live else ("building", 62)
    chip = (f'<rect x="{346 - w}" y="9" width="{w}" height="19" rx="9.5" fill="none" stroke="{A}" stroke-width="1"'
            + ('' if live else ' stroke-dasharray="3 2"') + f'/><text class="chip" x="{346 - w / 2}" y="22" text-anchor="middle">{txt}</text>')
    body = "\n".join(parts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 240" width="360" height="240" role="img" aria-label="{title}: {tag}">
<defs><filter id="glow" filterUnits="userSpaceOnUse" x="-400" y="-400" width="1200" height="1000"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>
  * {{ vector-effect: non-scaling-stroke; }}
  .face rect, .tyre {{ fill: {t["face"]}; stroke: {t["line"]}; stroke-width: 1; }}
  .face rect.top {{ fill: {t["top"]}; }} .face rect.side {{ fill: {t["side"]}; }}
  .acc rect, .acc rect.top, .acc rect.side {{ fill: {A}; stroke: {A}; }}
  .detail {{ fill: none; stroke: {t["detail"]}; stroke-width: 1; }}
  .glass {{ fill: {t["side"]}; stroke: {t["detail"]}; stroke-width: 1; }}
  .wire {{ fill: none; stroke: {t["line"]}; stroke-width: 1.2; }}
  .pulse {{ fill: none; stroke: {A}; stroke-width: 2.4; stroke-linecap: round; stroke-dasharray: 14 86; animation: run 2.4s linear infinite; animation-delay: var(--d, 0s); }}
  .atk {{ stroke-dasharray: 8 92; stroke-width: 3; animation-duration: .9s; }}
  @keyframes run {{ from {{ stroke-dashoffset: 100; }} to {{ stroke-dashoffset: 0; }} }}
  .blink rect {{ animation: blink 1.4s steps(1) infinite; animation-delay: var(--d, 0s); }}
  @keyframes blink {{ 0%, 49% {{ fill: {A}; stroke: {A}; }} 50%, 100% {{ fill: {t["face"]}; }} }}
  .dotc {{ fill: {t["face"]}; stroke: {t["line"]}; stroke-width: 1; animation: dot 2s steps(1) infinite; animation-delay: var(--d, 0s); }}
  @keyframes dot {{ 0%, 20% {{ fill: {A}; stroke: {A}; }} 21%, 100% {{ fill: {t["face"]}; stroke: {t["line"]}; }} }}
  .phone {{ animation: lit 2.4s ease-in-out infinite; }}
  @keyframes lit {{ 0%, 55% {{ fill: {t["side"]}; }} 70%, 100% {{ fill: {A}; }} }}
  .stopline {{ fill: none; stroke: {A}; stroke-width: 1.2; stroke-dasharray: 4 3; }}
  .bar {{ fill: {A}; }}
  .chk {{ fill: none; stroke: {t["line"]}; stroke-width: 1; }}
  .chkf {{ fill: {A}; opacity: 1; animation: fillin 3.2s linear infinite both; animation-delay: var(--d, 0s); }}
  @keyframes fillin {{ 0%, 15% {{ opacity: 0; }} 25%, 80% {{ opacity: 1; }} 95%, 100% {{ opacity: 0; }} }}
  .water {{ fill: {A}; fill-opacity: .25; stroke: {A}; stroke-width: 1.2; }}
  .draw {{ fill: none; stroke: {A}; stroke-width: 1.6; stroke-dasharray: 100; animation: draw 4s ease-out infinite; }}
  @keyframes draw {{ 0% {{ stroke-dashoffset: 100; }} 70%, 90% {{ stroke-dashoffset: 0; }} 100% {{ stroke-dashoffset: -100; }} }}
  {glow}
{''.join(XCSS)}  .fig {{ fill: {t["ink2"]}; font: 10px {MONO}; letter-spacing: 1px; }}
  .chip {{ fill: {t["ink"]}; font: 10px {MONO}; }}
  .title {{ fill: {t["ink"]}; font: 600 16px {MONO}; }}
  .tag {{ fill: {t["ink2"]}; font: 11px {MONO}; }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<rect x=".5" y=".5" width="359" height="239" rx="12" fill="{t["panel"]}" stroke="{t["detail"]}"/>
<text class="fig" x="14" y="22">FIG {n:02d}</text>
{chip}
<g transform="{fit}">
{body}
</g>
<text class="title" x="14" y="206">{title}</text>
<text class="tag" x="14" y="224">{tag}</text>
</svg>'''

here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, "cards"); os.makedirs(out, exist_ok=True)
for n, (cid, title, tag, model, live) in enumerate(CARDS, 1):
    for dark in (True, False):
        name = f"{cid}-{'dark' if dark else 'light'}.svg"
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(card(n, cid, title, tag, model, live, dark))
        print("wrote", name)
