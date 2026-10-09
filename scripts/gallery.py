"""Standard plots that exercise every yusina style setting.

    python scripts/gallery.py [context|scale] [register] [out.png]
    python scripts/gallery.py talk
    python scripts/gallery.py 1.25 formal gallery_big.png

Applies set_style(), then draws one panel per plot family so a change in
tokens.py shows up somewhere: cycle, markers, legend, titles, axis labels,
spines, grid, bars (patch edge), boxplot (notch/fliers/means), errorbar,
histogram, image+colorbar, fill_between, twin axes, minor ticks, log formatter,
unicode minus.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import matplotlib.pyplot as plt
import numpy as np

from yusina import set_style
from yusina import tokens as t
from yusina.figures import _set_ax_boxplot_i_colour

GALLERY = Path(__file__).resolve().parent.parent / "gallery"

rng = np.random.default_rng(0)


def _arg_scale(a):
    if a in t.CONTEXTS:
        return a
    try:
        return float(a)
    except ValueError:
        sys.exit(f"unknown context {a!r}; use a float or one of {sorted(t.CONTEXTS)}")


def lines(ax):
    x = np.linspace(0, 10, 40)
    for i in range(4):
        ax.plot(x, np.sin(x + i) + i * 0.3, marker="o", label=f"series {i}")
    ax.set(title="lines + markers", xlabel="time (s)", ylabel="signal")
    ax.legend(title="key")


def scatter(ax):
    for i in range(4):
        ax.scatter(rng.normal(i, 1, 60), rng.normal(i, 1, 60), alpha=0.6, label=str(i))
    ax.set(title="scatter (alpha)", xlabel="dim 1", ylabel="dim 2")


def bars(ax):
    cats = list("ABCDE")
    ax.bar(cats, rng.integers(3, 10, 5))
    ax.bar(cats, rng.integers(1, 4, 5), bottom=rng.integers(3, 10, 5))
    ax.set(title="stacked bars (patch edge)", ylabel="count")


def boxes(ax):
    data = [rng.normal(i, 1 + 0.3 * i, 200) for i in range(5)]
    bp = ax.boxplot(data, notch=True, showmeans=True, tick_labels=list("vwxyz"))
    for i, c in enumerate(plt.rcParams["axes.prop_cycle"].by_key()["color"][: len(data)]):
        _set_ax_boxplot_i_colour(bp, i, c, inner_alpha=1.0)
    ax.set(title="boxplot: notch · fliers · means", ylabel="value")


def errorbars(ax):
    x = np.arange(8)
    y = rng.normal(5, 1, 8)
    ax.errorbar(x, y, yerr=rng.uniform(0.3, 1.2, 8), fmt="o-", capsize=t.ERRORBAR_CAPSIZE)
    ax.set(title="errorbar (capsize)", xlabel="index", ylabel="mean ± sd")


def hist(ax):
    ax.hist(rng.normal(0, 1, 2000), bins=30)
    ax.hist(rng.normal(1.5, 0.7, 2000), bins=30, alpha=0.6)
    ax.set(title="histogram", xlabel="x", ylabel="freq")


def image(ax):
    im = ax.imshow(rng.random((12, 12)))
    ax.figure.colorbar(im, ax=ax, fraction=0.046)
    ax.set(title=f"imshow + colorbar ({t.CMAP})")


def area(ax):
    x = np.linspace(0, 6, 200)
    base = np.zeros_like(x)
    for i in range(3):
        top = base + np.abs(np.sin(x + i)) + 0.2
        ax.fill_between(x, base, top, alpha=0.7, label=f"band {i}")
        base = top
    ax.set(title="fill_between", xlabel="x", ylabel="stacked")
    ax.legend()


def twin_log(ax):
    x = np.linspace(1, 100, 100)
    ax.plot(x, -x ** 1.5, label="left: −x^1.5 (unicode minus)")
    ax.set(title="twin axes · log · minor ticks", xlabel="x", ylabel="linear")
    ax.minorticks_on()
    r = ax.twinx()
    r.semilogy(x, x ** 2, color=t.CYCLE[3])
    r.set_ylabel("right: x^2 (log)")
    ax.legend(loc="lower left")


PANELS = [lines, scatter, bars, boxes, errorbars, hist, image, area, twin_log]


def build(scale, register=t.DEFAULT_REGISTER):
    set_style(scale, register)
    fig, axs = plt.subplots(3, 3, figsize=(15, 12))
    for fn, ax in zip(PANELS, axs.flat):
        fn(ax)
    fig.suptitle(f"yusina gallery — scale={scale!r} register={register}", fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    return fig


if __name__ == "__main__":
    args = sys.argv[1:]
    register = next((a for a in args if a in t.REGISTERS), t.DEFAULT_REGISTER)
    args = [a for a in args if a != register]
    scale = _arg_scale(args[0]) if args else "notebook"
    out = Path(args[1]) if len(args) > 1 else GALLERY / f"gallery_{register}.png"
    build(scale, register).savefig(out, dpi=150)
    print("wrote", out)
