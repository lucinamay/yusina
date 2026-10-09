"""Render the ``yusina.palettes`` catalogue, one sheet per hue scheme ([pick] = maintainer favourite).

    python scripts/readymade.py          # writes catalogue_<scheme>.png
"""
import sys

sys.path.insert(0, "src")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import Rectangle

from yusina import palettes as P
from yusina import set_style


def luma(c):
    r, g, b = [(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in to_rgb(c)]
    return str(round((0.2126 * r + 0.7152 * g + 0.0722 * b) ** (1 / 2.2), 3))

def sheet(palettes, out, ncol=2):
    """Per palette: swatch · 2/3/4-series lines · first 4 in B/W · bars · scatter (alpha .5) · 4 lines at alpha .4."""
    set_style("notebook"); x = np.linspace(0, 10, 80); rng = np.random.default_rng(0)
    n = len(palettes); rows = -(-n // ncol); W = 8
    fig, axs = plt.subplots(rows, W * ncol, figsize=(16 * ncol, 1.9 * rows), squeeze=False, gridspec_kw={"width_ratios": [1.5, 1, 1, 1, 1, 1, 1, 1] * ncol})
    for k, (name, pal) in enumerate(palettes.items()):
        r, c0 = k % rows, W * (k // rows); sw, a2, a3, a4, bw, bar, sc, al = axs[r, c0:c0 + W]
        for i, c in enumerate(pal): sw.add_patch(Rectangle((i, 0.35), 1, 1, color=c)); sw.add_patch(Rectangle((i, 0), 1, 0.3, color=luma(c)))
        sw.set_xlim(0, max(len(pal), 8)); sw.set_ylim(0, 1.35); sw.axis("off"); sw.set_title(name, loc="left", fontsize=9)
        for m, ax in zip((2, 3, 4), (a2, a3, a4)):
            for i in range(m): ax.plot(x, np.sin(x / 2 + i * 0.9) + 0.3 * i, color=pal[i], lw=2)
        for i in range(min(4, len(pal))):
            bw.plot(x, np.sin(x / 2 + i * 0.9) + 0.3 * i, color=luma(pal[i]), lw=2)
            al.plot(x, np.sin(x / 2 + i * 0.9) + 0.3 * i, color=pal[i], lw=2, alpha=0.4)
            sc.scatter(rng.normal(i, 0.7, 40), rng.normal(i % 2, 0.7, 40), color=pal[i], s=14, alpha=0.5)
        bar.bar(range(len(pal)), 3 + rng.integers(0, 3, len(pal)), color=pal)
        for ax in (a2, a3, a4, bw, bar, sc, al): ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for ax in axs.flat[W * n:] if ncol == 1 else [a for k in range(n, rows * ncol) for a in axs[k % rows, W * (k // rows):W * (k // rows) + W]]: ax.axis('off')
    for ax, t in zip(axs[0, 1:W], ["2 series", "3 series", "4 series", "4 in B/W", "bars", "scatter α=.5", "lines α=.4"]): ax.set_title(t, fontsize=9)
    fig.suptitle("ready-made palettes — grey strip under swatch = luminance", fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.985)); fig.savefig(out, dpi=90); print("wrote", out)

if __name__ == "__main__":
    for sch, names in P.by_scheme().items():
        if not names: continue
        pals = {("[pick] " if P.PALETTES[n]["pick"] else "") + n + (f"  — {P.PALETTES[n]['note']}" if P.PALETTES[n]["note"] else ""): P.PALETTES[n]["colours"] for n in names}
        sheet(pals, f"catalogue_{sch}.png", ncol=1 if len(pals) <= 12 else 2)
