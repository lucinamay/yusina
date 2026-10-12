"""Shared pieces for the collection sheets: panel helpers, a grid builder, and the CLI.
Each collection has a ``_sheet.py`` shim that calls ``configure`` and re-exports this module."""

from __future__ import annotations

import sys
import textwrap
from functools import partial
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

from yusina import palettes as P
from yusina import set_style

INK = "#211F1E"
GALLERY = ASSETS = ROOT / "gallery" / "collections"
SERIF: list[str] = []
FALLBACK: str | None = None  # font appended to font.family for scripts the sans lacks (Hangul)
REFERENCES: tuple[str, ...] = ()
LANGS: tuple[str, ...] = ("en",)
FS = 1.3  # font scale for every explicit size below; the sheets are read on screen at 2000 px wide


def _fs(pt: float) -> float:
    return pt * FS


def configure(collection: str, langs=("en",), serif=(), fallback=None, references=()):
    """Set the per-collection paths, fonts, and reference sets; the first of *langs* is the default."""
    global GALLERY, ASSETS, SERIF, FALLBACK, REFERENCES, LANGS
    GALLERY = ROOT / "gallery" / "collections" / collection
    ASSETS = GALLERY / "assets"
    SERIF, FALLBACK, REFERENCES, LANGS = list(serif), fallback, tuple(references), tuple(langs)


def gallery() -> Path:
    """The configured output directory (read live; the name re-exported by a shim is the pre-configure value)."""
    return GALLERY


def blank(ax, title):
    ax.set_title(title, fontfamily=SERIF or None, fontweight="bold", fontsize=_fs(10.5))
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)


def _fit(ax, text, pt):
    """Re-wrap each paragraph to the axes width at *pt* points; paragraphs whose lines already fit keep their manual breaks."""
    fig = ax.figure; width_in = ax.get_position().width * fig.get_figwidth()
    chars = max(20, int(width_in * 72 / (pt * 0.52)))  # ~0.52 em average glyph width for Open Sans
    out = []
    for par in text.split("\n\n"):
        lines = par.split("\n")
        out.append(par if max(map(len, lines)) <= chars else textwrap.fill(" ".join(ln.strip() for ln in lines), chars))
    return "\n\n".join(out)


def caption(ax, text):
    ax.text(0, -0.05, _fit(ax, text, _fs(8.5)), transform=ax.transAxes, va="top", ha="left", fontsize=_fs(8.5), linespacing=1.5)


def artwork(ax, filename, title, credit, crop=None):
    """The source image (optionally cropped to fractions l,t,r,b) with its credit."""
    im = plt.imread(ASSETS / filename)
    if crop:
        h, w = im.shape[:2]; im = im[int(crop[1] * h):int(crop[3] * h), int(crop[0] * w):int(crop[2] * w)]
    blank(ax, title); ax.imshow(im); caption(ax, credit)


def swatches(ax, colours, title, labels=None, text=None):
    """One swatch per colour, optional label under each, caption below."""
    blank(ax, title)
    n = len(colours)
    for i, c in enumerate(colours):
        ax.add_patch(Rectangle((i, 0.25), 1, 0.75, color=c))
        if labels:  # long names wrap under their swatch instead of running into the neighbour's
            ax.text(i + 0.5, 0.12, textwrap.fill(labels[i], max(8, 90 // n)), ha="center", va="center", fontsize=_fs(7 if n <= 7 else 6), linespacing=1.1)
    ax.set_xlim(0, n); ax.set_ylim(0, 1)
    if text:
        caption(ax, text)


def plots(ax, colours, title, text=None, seed=0):
    """Stacked bars (left) and lines (right) in *colours*, the usual plotting test."""
    blank(ax, title)
    rng = np.random.default_rng(seed); x = np.linspace(0, 10, 40)
    n = len(colours); bottom = np.zeros(5)
    for i, c in enumerate(colours):
        v = rng.integers(1, 4, 5); ax.bar(np.arange(5), v, bottom=bottom, color=c, width=0.75); bottom += v
        ax.plot(7 + x * 0.5, 0.9 * bottom.max() * (0.45 + 0.55 * i / n) + np.sin(x + i) * 0.6, color=c, lw=2)
    ax.set_xlim(-0.6, 12.3); ax.set_ylim(0, bottom.max() * 1.15)
    if text:
        caption(ax, text)


def heatmaps(ax, cmaps, title, text=None):
    """One small heatmap per colormap, name under each."""
    blank(ax, title)
    z = np.add.outer(np.linspace(0, 1, 24), np.linspace(0, 1, 24)) / 2
    n = len(cmaps); w = 1.0 / n
    for i, name in enumerate(cmaps):
        ins = ax.inset_axes((i * w + 0.01, 0.16, w - 0.02, 0.8)); ins.imshow(z, cmap=name); ins.set_xticks([]); ins.set_yticks([]); ins.grid(False)
        ax.text(i * w + w / 2, 0.06, name, ha="center", va="center", fontsize=_fs(6.5), family="monospace", transform=ax.transAxes)
    if text:
        caption(ax, text)


def gradients(ax, cmaps, title, text=None):
    """Horizontal gradient bar per colormap."""
    blank(ax, title)
    grad = np.linspace(0, 1, 256)[None, :]
    for i, name in enumerate(cmaps):
        ax.imshow(grad, cmap=name, aspect="auto", extent=(0, 1, i + 0.15, i + 0.85))
        ax.text(1.02, i + 0.5, name, va="center", fontsize=_fs(7.5), family="monospace")
    ax.set_xlim(0, 1.55); ax.set_ylim(0, len(cmaps))
    if text:
        caption(ax, text)


def text_panel(ax, title, body):
    blank(ax, title); ax.text(0, 1, _fit(ax, body, _fs(9)), transform=ax.transAxes, va="top", ha="left", fontsize=_fs(9), linespacing=1.6)


def build(panels, suptitle, ncols=3, row_heights=None, figsize=(19, 14)):
    """panels: callables fn(ax), or (fn, colspan) tuples; laid out row-major on an ncols grid."""
    set_style("notebook", "clean")
    if FALLBACK:
        plt.rcParams["font.family"] = [plt.rcParams["font.sans-serif"][0], FALLBACK]
    spans = [p[1] if isinstance(p, tuple) else 1 for p in panels]
    nrows = -(-sum(spans) // ncols)
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(nrows, ncols, height_ratios=row_heights or [1] * nrows, hspace=0.75, wspace=0.25, top=0.915, bottom=0.05, left=0.04, right=0.97)  # hspace leaves room for the captions under each panel
    r = c = 0
    for p, span in zip(panels, spans):
        fn = p[0] if isinstance(p, tuple) else p
        if c + span > ncols:
            r, c = r + 1, 0
        fn(fig.add_subplot(gs[r, c:c + span])); c += span
        if c >= ncols:
            r, c = r + 1, 0
    fig.suptitle(suptitle, fontfamily=SERIF or None, fontweight="bold", fontsize=_fs(18), y=0.99)
    return fig


def main(sheets, stem):
    """CLI: [<lang>|all]; sheets = {lang: (panels, suptitle, kwargs)}. The default language writes <stem>.png, others <stem>_<lang>.png."""
    args = sys.argv[1:]
    langs = list(LANGS) if "all" in args else [a for a in args if a in sheets] or [LANGS[0]]
    for lang in langs:
        panels, title, kw = sheets[lang]
        out = GALLERY / (f"{stem}.png" if lang == LANGS[0] else f"{stem}_{lang}.png")
        build(panels, title, **kw).savefig(out, dpi=130); plt.close("all"); print("wrote", out)


def standard_sheet(t, src, pal, extra=None, cmaps=None, crop=None, figsize=(19, 15)):
    """The common layout: artwork (2 cols) + "how" text; swatches + middle panel + plots; sources (3 cols).
    t: strings sup, art, credit, pal, pal_c, plots, how, how_b, prov, prov_b, and for the middle panel
    extra_t/extra_c (with *extra* = (colours, labels)) or cmaps_t/cmaps_c (with *cmaps* = names)."""
    cols = P.get(pal)
    middle = (partial(swatches, colours=extra[0], title=t["extra_t"], labels=extra[1], text=t["extra_c"]) if extra
              else partial(gradients, cmaps=cmaps, title=t["cmaps_t"], text=t["cmaps_c"]) if cmaps else None)
    panels = [(partial(artwork, filename=src, title=t["art"], credit=t["credit"], crop=crop), 2),
              partial(text_panel, title=t["how"], body=t["how_b"]),
              (partial(swatches, colours=cols, title=t["pal"], labels=names(cols), text=t["pal_c"]), 1 if middle else 2),
              *([middle] if middle else []),
              partial(plots, colours=cols, title=t["plots"]),
              (partial(text_panel, title=t["prov"], body=t["prov_b"]), 3)]
    return panels, t["sup"], {"ncols": 3, "row_heights": [1.3, 1.0, 0.45], "figsize": figsize}


def overview(rows, suptitle, dpi=110):
    """One row per palette: the object it was sampled from, its swatches, and plots.
    rows: (palette, asset filename, crop or None, credit). Writes <gallery>/overview.png."""
    panels = []
    for i, (pal, f, crop, credit) in enumerate(rows):
        cols = P.get(pal)
        panels += [partial(artwork, filename=f, title=pal, credit=credit, crop=crop),
                   partial(swatches, colours=cols, title=f"`{pal}` · {P.PALETTES[pal]['source']}", labels=names(cols)),
                   partial(plots, colours=cols, title="", seed=i)]
    out = GALLERY / "overview.png"
    build(panels, suptitle, ncols=3, figsize=(19, 4.2 * len(rows))).savefig(out, dpi=dpi); plt.close("all"); print("wrote", out)


def combine(stems, name):
    """Stack the rendered sheets *stems* (in order) into <gallery>/<name>[_<lang>].png, one per language, at a common width."""
    from PIL import Image

    for lang in LANGS:
        suffix = "" if lang == LANGS[0] else f"_{lang}"
        ims = [Image.open(GALLERY / f"{stem}{suffix}.png").convert("RGB") for stem in stems]
        w = max(im.width for im in ims)
        ims = [im if im.width == w else im.resize((w, round(im.height * w / im.width)), Image.Resampling.LANCZOS) for im in ims]
        gap = w // 40
        out = Image.new("RGB", (w, sum(im.height for im in ims) + gap * (len(ims) - 1)), "white"); y = 0
        for im in ims:
            out.paste(im, (0, y)); y += im.height + gap
        out.save(GALLERY / f"{name}{suffix}.png", optimize=True); print("wrote", GALLERY / f"{name}{suffix}.png")


def names(colours):
    """Name from the configured reference sets (later sets win) for each colour that is exactly a reference colour, else its hue."""
    ref = {}
    for name in REFERENCES:
        ref.update({v.lower(): k for k, v in P.reference(name).items()})
    return [ref.get(c.lower(), P.hue_name(c)) for c in colours]
