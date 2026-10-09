"""Render the ``yusina.palettes`` catalogue, one sheet per hue scheme ([pick] = maintainer favourite).

    python scripts/readymade.py          # writes gallery/catalogue_<scheme>.png
"""
import sys
from pathlib import Path

sys.path.insert(0, "src")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import Rectangle

from yusina import palettes as P
from yusina import set_style

GALLERY = Path(__file__).resolve().parent.parent / "gallery"


def luma(c):
    r, g, b = [(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in to_rgb(c)]
    return str(round((0.2126 * r + 0.7152 * g + 0.0722 * b) ** (1 / 2.2), 3))

def sheet(palettes, out):
    """Per palette: swatch · 2/3/4-series lines · first 4 in B/W · bars · scatter (alpha .5) · 4 lines at alpha .4
    · stacked bars · stacked area (planes)."""
    set_style("notebook"); x = np.linspace(0, 10, 80); rng = np.random.default_rng(0)
    n = len(palettes); W = 10
    fig, axs = plt.subplots(n, W, figsize=(19, 1.9 * n), squeeze=False, gridspec_kw={"width_ratios": [1.5] + [1] * 9})
    for k, (name, pal) in enumerate(palettes.items()):
        sw, a2, a3, a4, bw, bar, sc, al, st, ar = axs[k]
        for i, c in enumerate(pal): sw.add_patch(Rectangle((i, 0.35), 1, 1, color=c)); sw.add_patch(Rectangle((i, 0), 1, 0.3, color=luma(c)))
        sw.set_xlim(0, max(len(pal), 8)); sw.set_ylim(0, 1.35); sw.axis("off"); sw.set_title(name, loc="left", fontsize=9)
        for m, ax in zip((2, 3, 4), (a2, a3, a4)):
            for i in range(m): ax.plot(x, np.sin(x / 2 + i * 0.9) + 0.3 * i, color=pal[i], lw=2)
        for i in range(min(4, len(pal))):
            bw.plot(x, np.sin(x / 2 + i * 0.9) + 0.3 * i, color=luma(pal[i]), lw=2)
            al.plot(x, np.sin(x / 2 + i * 0.9) + 0.3 * i, color=pal[i], lw=2, alpha=0.4)
            sc.scatter(rng.normal(i, 0.7, 40), rng.normal(i % 2, 0.7, 40), color=pal[i], s=14, alpha=0.5)
        bar.bar(range(len(pal)), 3 + rng.integers(0, 3, len(pal)), color=pal)
        bottom = np.zeros(5)
        for i in range(min(4, len(pal))):
            v = 1 + rng.integers(0, 3, 5); st.bar(range(5), v, bottom=bottom, color=pal[i], width=0.8); bottom += v
        ar.stackplot(x, [np.sin(x / 3 + i) + 1.5 for i in range(min(4, len(pal)))], colors=pal[:4], lw=0)
        for ax in (a2, a3, a4, bw, bar, sc, al, st, ar): ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for ax, t in zip(axs[0, 1:W], ["2 series", "3 series", "4 series", "4 in B/W", "bars", "scatter α=.5", "lines α=.4", "stacked bars", "stacked area"]): ax.set_title(t, fontsize=9)
    fig.suptitle("ready-made palettes — grey strip under swatch = luminance", fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.985)); fig.savefig(out, dpi=90); print("wrote", out)

if __name__ == "__main__":
    for sch, names in P.by_scheme().items():
        if not names: continue
        pals = {("[pick] " if P.PALETTES[n]["pick"] else "") + n + (f"  — {P.PALETTES[n]['note']}" if P.PALETTES[n]["note"] else ""): P.PALETTES[n]["colours"] for n in names}
        sheet(pals, GALLERY / f"catalogue_{sch}.png")
