"""Render every value in tokens.py as a representative specimen.

    python scripts/moodboard.py [out.png]

Library-independent: reads tokens.py directly and draws each token the way it
is actually used (INK as text/spine/tick, INK_FAINT as a swatch, GRID behind
data, CANVAS as show-through, CYCLE as lines + bars, sizes as real specimens,
widths as real strokes). It does NOT apply the yusina style, so what you see
is the source record, not a generated sheet.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle

from yusina import tokens as t

GALLERY = Path(__file__).resolve().parent.parent / "gallery"

REG = t.REGISTERS[t.DEFAULT_REGISTER]

# use the token font for specimens, nothing else
plt.rcParams.update({"font.family": t.FONT_FAMILY, "font.sans-serif": t.SANS})

MONO = {"family": "monospace"}


def _blank(ax, title):
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(title, loc="left", fontsize=11, fontweight="bold", color=t.INK, pad=6)
    ax.set_xlim(0, 1)


def panel_core_colours(ax):
    _blank(ax, "core colours  ·  role")
    rows = [
        (t.INK, "INK", "text · spines · ticks · default line & marker"),
        (t.INK_FAINT, "INK_FAINT", "unused by rc; boxplots stroke outline(fill)"),
        (t.GRID, "GRID", f"grid lines (drawn at alpha {REG['grid_alpha']})"),
        (t.CANVAS, "CANVAS", "axes + figure + saved-file background (transparent)"),
    ]
    x0, w = 0.02, 0.11
    ax.set_ylim(0, len(rows))
    for i, (col, name, role) in enumerate(reversed(rows)):
        y = i + 0.5
        if name == "GRID":  # faint lines on white -- how it actually reads
            ax.add_patch(Rectangle((x0, y - 0.34), w, 0.68, facecolor="white",
                                   edgecolor=t.INK, lw=0.6))
            for gx in np.linspace(x0 + 0.012, x0 + w - 0.012, 6):
                ax.plot([gx, gx], [y - 0.32, y + 0.32], color=col, lw=0.6,
                        alpha=REG["grid_alpha"])
            for gy in np.linspace(y - 0.22, y + 0.22, 3):
                ax.plot([x0 + 0.005, x0 + w - 0.005], [gy, gy], color=col, lw=0.6,
                        alpha=REG["grid_alpha"])
        elif name == "CANVAS":  # show-through: checkerboard
            for cx in range(10):
                for cy in range(6):
                    ax.add_patch(Rectangle((x0 + cx * w / 10, y - 0.34 + cy * 0.68 / 6),
                                           w / 10, 0.68 / 6,
                                           color="0.82" if (cx + cy) % 2 else "1.0"))
            ax.add_patch(Rectangle((x0, y - 0.34), w, 0.68, facecolor="none",
                                   edgecolor=t.INK, lw=0.6))
        else:
            ax.add_patch(Rectangle((x0, y - 0.34), w, 0.68, facecolor=col,
                                   edgecolor=t.INK, lw=0.6))
        ax.text(x0 + w + 0.03, y + 0.19, name, va="center", fontsize=10,
                fontweight="bold", color=t.INK)
        ax.text(x0 + w + 0.03, y - 0.19, col, va="center", fontsize=8, color=t.INK,
                **MONO)
        ax.text(0.42, y, role, va="center", fontsize=9, color=t.INK)


def panel_cycle(ax_sw, ax_demo):
    _blank(ax_sw, f"CYCLE  ·  {len(t.CYCLE)} categorical colours (lines & patches)")
    ax_sw.set_ylim(0, 1)
    w = 1.0 / len(t.CYCLE)
    for i, col in enumerate(t.CYCLE):
        ax_sw.add_patch(Rectangle((i * w, 0.35), w * 0.92, 0.6, facecolor=col,
                                  edgecolor=t.INK, lw=0.6))
        ax_sw.text(i * w + w * 0.46, 0.2, str(i), ha="center", fontsize=8, color=t.INK)
        ax_sw.text(i * w + w * 0.46, 0.06, col, ha="center", fontsize=6, color=t.INK,
                   **MONO)

    ax_demo.set_title("used as lines / bars", loc="left", fontsize=9, color=t.INK)
    x = np.linspace(0, 6, 100)
    for i, col in enumerate(t.CYCLE):
        ax_demo.plot(x, np.sin(x + i * 0.5) + i * 0.15, color=col, lw=1.4)
    ax_demo.set_xticks([])
    ax_demo.set_yticks([])
    for s in ax_demo.spines.values():
        s.set_color(t.INK)
        s.set_linewidth(0.5)


def panel_colormap(ax):
    _blank(ax, f"CMAP  ·  {t.CMAP}  (images / heatmaps)")
    grad = np.linspace(0, 1, 256)[None, :]
    ax.imshow(grad, aspect="auto", cmap=t.CMAP, extent=(0, 1, 0, 1))
    ax.text(0.02, 0.5, "low", va="center", fontsize=8, color=t.INK)
    ax.text(0.98, 0.5, "high", va="center", ha="right", fontsize=8, color="white")


def panel_typography(ax):
    _blank(ax, f"typography  ·  {', '.join(t.SANS)}")
    pt = t.FONT_PT
    rows = [("body / tick base", pt, t.WEIGHT)]
    rows += [(name, pt * mult, REG["title_weight"] if "title" in name else t.WEIGHT)
             for name, mult in t.FONT_SCALE.items()]
    ax.set_ylim(0, len(rows))
    for i, (name, size, weight) in enumerate(reversed(rows)):
        y = i + 0.5
        ax.text(0.02, y, "Aa Bb Qq 0123 — biosynthesis", va="center", fontsize=size,
                fontweight=weight, color=t.INK)
        ax.text(0.72, y, f"{name}", va="center", fontsize=9, color=t.INK)
        ax.text(0.98, y, f"{size:g} pt · {weight}", va="center", ha="right", fontsize=8,
                color=t.INK, **MONO)


def panel_linewidths(ax):
    _blank(ax, "LINEWIDTH  ·  strokes at true width (pt)")
    items = list(t.LINEWIDTH.items())
    ax.set_ylim(0, len(items))
    for i, (name, lw) in enumerate(reversed(items)):
        y = i + 0.5
        ax.plot([0.02, 0.5], [y, y], color=t.INK, lw=max(lw, 0.1),
                solid_capstyle="round")
        note = " (invisible: spines off)" if lw == 0 else ""
        ax.text(0.55, y, f"{name}   {lw:g} pt{note}", va="center", fontsize=9,
                color=t.INK)


def panel_geometry(ax):
    _blank(ax, "geometry & output")
    lines = [
        ("tick length", f"major {t.TICK_LEN['major']:g} pt · minor {t.TICK_LEN['minor']:g} pt"),
        ("marker size", f"{t.MARKER_PT:g} pt · small (fliers/means) {t.MARKER_PT_SMALL:g} pt"),
        ("errorbar cap", f"{t.ERRORBAR_CAPSIZE:g} pt"),
        ("pads", " · ".join(f"{k} {v:g}" for k, v in t.PAD.items())),
        ("grid alpha", f"{REG['grid_alpha']}"),
        ("figsize", f"{t.FIGSIZE[0]:g} x {t.FIGSIZE[1]:g} in"),
        ("dpi", f"screen {t.DPI_SCREEN} · save {t.DPI_SAVE}"),
        ("contexts", " · ".join(f"{k}={v:g}" for k, v in t.CONTEXTS.items())),
    ]
    ax.set_ylim(0, len(lines))
    for i, (k, v) in enumerate(reversed(lines)):
        y = i + 0.5
        ax.text(0.02, y, k, va="center", fontsize=9, fontweight="bold", color=t.INK)
        ax.text(0.30, y, v, va="center", fontsize=9, color=t.INK, **MONO)


def build():
    fig = plt.figure(figsize=(9, 13))
    fig.patch.set_facecolor("white")
    gs = GridSpec(6, 2, figure=fig, height_ratios=[2.0, 1.2, 0.5, 2.2, 2.4, 2.6],
                  hspace=0.9, wspace=0.12, top=0.93, bottom=0.02, left=0.06, right=0.97)
    fig.suptitle("yusina — token moodboard", fontsize=15, fontweight="bold",
                 color=t.INK, x=0.06, ha="left", y=0.985)

    panel_core_colours(fig.add_subplot(gs[0, :]))
    panel_cycle(fig.add_subplot(gs[1, :]), fig.add_subplot(gs[2, :]))
    panel_colormap(fig.add_subplot(gs[3, 0]))
    panel_linewidths(fig.add_subplot(gs[3, 1]))
    panel_typography(fig.add_subplot(gs[4, :]))
    panel_geometry(fig.add_subplot(gs[5, :]))
    return fig


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else GALLERY / "moodboard.png"
    fig = build()
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    print("wrote", out)
