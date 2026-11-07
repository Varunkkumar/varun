# Builds stack-dark.svg / stack-light.svg: a scrolling strip of skill chips for the profile README. CSS only, transparent background.
# run: python make_stack.py   (writes next to this file)
import os

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
A = "#2dd4bf"
NAMES = ["c", "c++", "python", "java", "bash", "esp32", "arduino", "ros 2", "linux", "react", "typescript", "react native",
         "mongodb", "docker", "aws", "gcp", "git", "blender"]
GAP, PAD, CH = 10, 28, 7.6

def page(dark):
    t = dict(detail="#22303b", ink="#d5e0e8") if dark else dict(detail="#c9c8c2", ink="#1d1e20")
    chips, x = [], 0.0
    for i, n in enumerate(NAMES):
        w = len(n) * CH + PAD
        chips.append(f'<rect class="{"chip hot" if i % 3 == 0 else "chip"}" x="{x:.1f}" y="20" width="{w:.1f}" height="30" rx="14"/>'
                     f'<text x="{x + w / 2:.1f}" y="35.5" text-anchor="middle" dominant-baseline="middle">{n}</text>')
        x += w + GAP
    row = "".join(chips); rw = x
    moved = row + f'<g transform="translate({rw:.1f} 0)">{row}</g>'          # second copy sits one row-width to the right
    names = ", ".join(NAMES)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 70" width="900" height="70" role="img" aria-label="Tech stack: {names}.">
<defs>
<linearGradient id="fade" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="900" y2="0"><stop offset="0" stop-color="#000"/><stop offset="{70 / 900:.4f}" stop-color="#fff"/><stop offset="{1 - 70 / 900:.4f}" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
<mask id="m" maskUnits="userSpaceOnUse" x="0" y="0" width="900" height="70"><rect width="900" height="70" fill="url(#fade)"/></mask>
</defs>
<style>
  .chip {{ fill: none; stroke: {t["detail"]}; stroke-width: 1; }}
  .hot {{ stroke: {A}; }}
  text {{ fill: {t["ink"]}; font: 12.5px {MONO}; }}
  .row {{ transform-box: view-box; animation: scroll 40s linear infinite; }}
  @keyframes scroll {{ from {{ transform: translate(0px, 0px); }} to {{ transform: translate(-{rw:.1f}px, 0px); }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<g mask="url(#m)"><g class="row">{moved}</g></g>
</svg>'''

here = os.path.dirname(os.path.abspath(__file__))
for name, dark in (("stack-dark.svg", True), ("stack-light.svg", False)):
    with open(os.path.join(here, name), "w", encoding="utf-8") as f:
        f.write(page(dark))
    print("wrote", name)
