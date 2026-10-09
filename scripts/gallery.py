"""Standard plots that exercise every yusina style setting.

    python scripts/gallery.py [context|scale] [register] [family|all] [out.png]
    python scripts/gallery.py talk                 # 9-panel overview -> gallery/gallery_clean.png
    python scripts/gallery.py formal all           # one sheet per family -> gallery/<family>_formal.png
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

import io
import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap

from yusina import backends, figures, set_style
from yusina import tokens as t
from yusina.colours import outline
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
    ax.set(title="boxplot: notch, fliers, means", ylabel="value")


def errorbars(ax):
    x = np.arange(8)
    y = rng.normal(5, 1, 8)
    ax.errorbar(x, y, yerr=rng.uniform(0.3, 1.2, 8), fmt="o-", capsize=t.ERRORBAR_CAPSIZE)
    ax.set(title="errorbar (capsize)", xlabel="index", ylabel=r"mean $\pm$ sd")


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
    ax.set(title="fill between", xlabel="x", ylabel="stacked")
    ax.legend()


def twin_log(ax):
    x = np.linspace(1, 100, 100)
    ax.plot(x, -x ** 1.5, label=r"left: $-x^{1.5}$")
    ax.set(title="twin axes, log, minor ticks", xlabel="x", ylabel="linear")
    ax.minorticks_on()
    r = ax.twinx()
    r.semilogy(x, x ** 2, color=t.CYCLE[3])
    r.set_ylabel(r"right: $x^2$ (log)")
    ax.legend(loc="lower left")



def _cycle():
    return plt.rcParams["axes.prop_cycle"].by_key()["color"]


def _kde(sample, grid, bw=None):
    """Gaussian KDE on *grid* (numpy only; Scott's rule bandwidth)."""
    sample = np.asarray(sample)
    bw = bw or 1.06 * sample.std() * len(sample) ** -0.2
    return np.exp(-0.5 * ((grid[:, None] - sample[None, :]) / bw) ** 2).sum(1) / (len(sample) * bw * np.sqrt(2 * np.pi))


def _paste(ax, fig, dpi=110):
    """Rasterise *fig* and show it in *ax* (own-figure helpers and other backends)."""
    buf = io.BytesIO()
    fig.savefig(buf, dpi=dpi, format="png")
    plt.close(fig)
    buf.seek(0)
    ax.imshow(plt.imread(buf))
    ax.axis("off")


def _needs_chrome(ax, exc):
    """kaleido missing or without Chrome: report on stderr and in the panel, keep the sheet going."""
    print("plotly panel skipped:", str(exc).strip().splitlines()[0], file=sys.stderr)
    ax.text(0.5, 0.5, "plotly: image export unavailable\nuv sync (kaleido) + uv run plotly_get_chrome",
            ha="center", va="center", transform=ax.transAxes)
    ax.axis("off")


# ---------------------------------------------------------------- lines ----
def errorband(ax):
    x = np.linspace(0, 10, 50)
    for i, c in enumerate(_cycle()[:3]):
        y = np.sin(x + i) + 0.3 * i
        ax.plot(x, y, color=c, label=f"model {i}")
        ax.fill_between(x, y - 0.25, y + 0.25, color=c, alpha=0.2, lw=0)
    ax.legend()
    ax.set(title="line + CI band", xlabel="x", ylabel="y")


def step_lines(ax):
    for i, c in enumerate(_cycle()[:3]):
        times = np.sort(rng.exponential(3 + i, 25))
        surv = np.linspace(1, 0.2 + 0.1 * i, len(times))
        ax.step(times, surv, where="post", color=c, label=f"arm {i}")
        cens = times[::5]
        ax.plot(cens, np.interp(cens, times, surv), "|", color=c, ms=6)
    ax.legend()
    ax.set(title="step: survival curves + censor ticks", xlabel="time", ylabel="S(t)", ylim=(0, 1.05))


def stems(ax):
    x = np.arange(12)
    for i, c in enumerate(_cycle()[:2]):
        m = ax.stem(x + 0.3 * i, rng.random(12) + i * 0.1, linefmt="-", markerfmt="o", basefmt=" ", label=f"s{i}")
        m.markerline.set_color(c); m.stemlines.set_color(c)
    ax.axhline(0, color=t.INK, lw=0.5)
    ax.legend()
    ax.set(title="stem", xlabel="index", ylabel="weight")


def gradient_line(ax):
    x = np.linspace(0, 4 * np.pi, 200)
    y = np.sin(x) * np.exp(-x / 8)
    pts = np.array([x, y]).T.reshape(-1, 1, 2)
    lc = LineCollection(list(np.concatenate([pts[:-1], pts[1:]], axis=1)), cmap=t.CMAP, lw=2)
    lc.set_array(x)
    ax.add_collection(lc)
    ax.autoscale()
    ax.figure.colorbar(lc, ax=ax, label="t")
    ax.set(title="line coloured by a 3rd variable", xlabel="x", ylabel="y")


def direct_labels(ax):
    x = np.linspace(0, 10, 50)
    for i, c in enumerate(_cycle()[:4]):
        y = np.log1p(x) * (1 + 0.4 * i)
        ax.plot(x, y, color=c)
        ax.text(x[-1] + 0.2, y[-1], f"series {i}", color=c, va="center")
    ax.set(title="direct labels, no legend", xlabel="x", ylabel="y", xlim=(0, 12.5))


def roc(ax):
    for i, c in enumerate(_cycle()[:3]):
        pos, neg = rng.normal(1 + 0.6 * i, 1, 300), rng.normal(0, 1, 300)
        thr = np.sort(np.concatenate([pos, neg]))[::-1]
        tpr = [(pos >= s).mean() for s in thr]; fpr = [(neg >= s).mean() for s in thr]
        ax.plot(fpr, tpr, color=c, label=f"model {i}")
    ax.plot([0, 1], [0, 1], ls="--", color=t.INK, lw=0.8, label="chance")
    ax.legend(loc="lower right")
    ax.set(title="ROC", xlabel="FPR", ylabel="TPR", aspect="equal")


# -------------------------------------------------------------- scatter ----
def bubble(ax):
    n = 40
    sc = ax.scatter(rng.random(n), rng.random(n), s=rng.integers(10, 300, n), alpha=0.6, edgecolors="none")
    handles, labels = sc.legend_elements(prop="sizes", num=3, alpha=0.6)
    ax.legend(handles, labels, title="size")
    ax.set(title="bubble: size = 3rd variable", xlabel="x", ylabel="y")


def scatter_cbar(ax):
    n = 120
    x, y = rng.random(n), rng.random(n)
    sc = ax.scatter(x, y, c=x + y, cmap=t.CMAP, edgecolors="none")
    ax.figure.colorbar(sc, ax=ax, label="x + y")
    ax.set(title="scatter + colorbar", xlabel="x", ylabel="y")


def volcano(ax):
    n = 600
    lfc = rng.normal(0, 1.2, n); p = -np.log10(rng.random(n) ** 3)
    sig = p > 2
    up, down = sig & (lfc > 1), sig & (lfc < -1)
    c0, c1 = _cycle()[:2]
    ax.scatter(lfc[~(up | down)], p[~(up | down)], color="lightgrey", s=8, edgecolors="none")
    ax.scatter(lfc[up], p[up], color=c0, s=10, edgecolors="none", label="up")
    ax.scatter(lfc[down], p[down], color=c1, s=10, edgecolors="none", label="down")
    ax.axhline(2, ls="--", color=t.INK, lw=0.6); ax.axvline(1, ls="--", color=t.INK, lw=0.6); ax.axvline(-1, ls="--", color=t.INK, lw=0.6)
    ax.legend()
    ax.set(title="volcano", xlabel="log2 fold change", ylabel="-log10 p")


def hexbin(ax):
    x = rng.normal(size=4000); y = 0.6 * x + rng.normal(size=4000) * 0.8
    hb = ax.hexbin(x, y, gridsize=22, cmap=t.CMAP, mincnt=1, linewidths=0)
    ax.figure.colorbar(hb, ax=ax, label="count")
    ax.set(title="hexbin", xlabel="x", ylabel="y")


def hist2d(ax):
    x = rng.normal(size=4000); y = -0.5 * x + rng.normal(size=4000)
    _, _, _, im = ax.hist2d(x, y, bins=30, cmap=t.CMAP)
    ax.figure.colorbar(im, ax=ax, label="count")
    ax.set(title="2-D histogram", xlabel="x", ylabel="y")


# -------------------------------------------------------- distributions ----
def violins(ax):
    data = [rng.normal(i, 0.6 + 0.2 * i, 120) for i in range(4)]
    parts = ax.violinplot(data, showmedians=True, showextrema=False)
    for body, c in zip(parts["bodies"], _cycle()):
        body.set_facecolor(c); body.set_edgecolor(outline(c)); body.set_alpha(0.7)
    parts["cmedians"].set_color(t.INK)
    for i, (d, c) in enumerate(zip(data, _cycle())):
        ax.scatter(rng.normal(i + 1, 0.04, len(d)), d, s=4, color=outline(c), alpha=0.5, edgecolors="none")
    ax.set(title="violin + strip", xticks=range(1, 5), xticklabels=list("abcd"), ylabel="value")


def strip(ax):
    for i, c in enumerate(_cycle()[:5]):
        d = rng.normal(i * 0.5, 1, 60)
        ax.scatter(rng.normal(i, 0.08, len(d)), d, s=10, color=c, alpha=0.6, edgecolors="none")
        ax.plot([i - 0.25, i + 0.25], [d.mean()] * 2, color=outline(c), lw=2)
    ax.set(title="strip + mean", xticks=range(5), xticklabels=list("abcde"), ylabel="value")


def kde(ax):
    grid = np.linspace(-4, 8, 300)
    for i, c in enumerate(_cycle()[:3]):
        d = _kde(rng.normal(i * 1.5, 1 + 0.3 * i, 200), grid)
        ax.plot(grid, d, color=c, label=f"group {i}")
        ax.fill_between(grid, d, color=c, alpha=0.25, lw=0)
    ax.legend()
    ax.set(title="KDE", xlabel="value", ylabel="density")


def ridgeline(ax):
    grid = np.linspace(-4, 10, 300)
    for i, c in enumerate(_cycle()[:5]):
        d = _kde(rng.normal(i * 1.2, 1, 150), grid)
        d = d / d.max() * 1.4
        ax.fill_between(grid, i, i + d, color=c, alpha=0.8, lw=0, zorder=5 - i)
        ax.plot(grid, i + d, color=outline(c), lw=0.8, zorder=5 - i)
    ax.set(title="ridgeline", yticks=range(5), yticklabels=[f"day {i}" for i in range(5)], xlabel="value")


def hist_overlay(ax):
    for i, c in enumerate(_cycle()[:3]):
        ax.hist(rng.normal(i, 1, 400), bins=30, histtype="stepfilled", color=c, alpha=0.4, ec=outline(c), label=f"g{i}")
    ax.legend()
    ax.set(title="overlaid histograms", xlabel="value", ylabel="count")


def ecdf(ax):
    for i, c in enumerate(_cycle()[:3]):
        ax.ecdf(rng.gamma(2 + i, 1, 200), color=c, label=f"sample {i}")
    ax.legend(loc="lower right")
    ax.set(title="ECDF", xlabel="value", ylabel="F(x)")


def raster(ax):
    events = [np.sort(rng.uniform(0, 10, rng.integers(10, 40))) for _ in range(12)]
    colors = [c for c in _cycle()[:3] for _ in range(4)]
    ax.eventplot(events, colors=colors, lineoffsets=1, linelengths=0.8)
    ax.set(title="event raster", xlabel="time (s)", ylabel="trial")


# ----------------------------------------------------------- categorical ----
def grouped_bars(ax):
    cats, groups = list("wxyz"), 3
    w = 0.8 / groups
    for g, c in enumerate(_cycle()[:groups]):
        vals = rng.integers(3, 10, len(cats))
        ax.bar(np.arange(len(cats)) + (g - 1) * w, vals, w, yerr=rng.random(len(cats)), capsize=2, color=c, label=f"group {g}")
    ax.legend()
    ax.set(title="grouped bars + error caps", xticks=range(len(cats)), xticklabels=cats, ylabel="count")


def stacked(ax):
    x = np.arange(6); bottom = np.zeros(6)
    for i, c in enumerate(_cycle()[:5]):
        v = rng.integers(1, 6, 6)
        ax.bar(x, v, bottom=bottom, color=c, label=f"part {i}")
        bottom += v
    ax.legend(ncols=2)
    ax.set(title="stacked bars: planes touching", xlabel="sample", ylabel="count")


def barh(ax):
    vals = np.sort(rng.integers(5, 50, 8))
    labels = [f"item {i}" for i in range(8)]
    bars_ = ax.barh(labels, vals, color=_cycle()[0])
    ax.bar_label(bars_, padding=3)
    ax.set(title="horizontal bars + value labels", xlabel="value", xlim=(0, 58))


def lollipop(ax):
    vals = np.sort(rng.random(10))
    y = np.arange(10)
    ax.hlines(y, 0, vals, color=_cycle()[0], lw=1)
    ax.plot(vals, y, "o", color=_cycle()[0])
    ax.set(title="lollipop", yticks=y, yticklabels=[f"gene {i}" for i in y], xlabel="score")


def dumbbell(ax):
    y = np.arange(7); before = rng.random(7); after = before + rng.normal(0.2, 0.15, 7)
    c0, c1 = _cycle()[:2]
    ax.hlines(y, before, after, color=t.INK, lw=1, alpha=0.5)
    ax.plot(before, y, "o", color=c0, label="before"); ax.plot(after, y, "o", color=c1, label="after")
    ax.legend()
    ax.set(title="dumbbell", yticks=y, yticklabels=[f"site {i}" for i in y], xlabel="value")


def pie_donut(ax):
    vals = [35, 25, 20, 12, 8]
    ax.pie(vals, labels=[f"c{i}" for i in range(5)], colors=_cycle()[:5], wedgeprops={"width": 0.45, "lw": 0}, startangle=90)
    ax.set(title="donut: adjacent planes")


def waffle(ax):
    counts = [38, 27, 20, 15]
    cells = np.repeat(np.arange(4), counts).reshape(10, 10)
    ax.imshow(cells, cmap=ListedColormap(_cycle()[:4]), interpolation="nearest")
    ax.set_xticks(np.arange(-0.5, 10, 1), minor=True); ax.set_yticks(np.arange(-0.5, 10, 1), minor=True)
    ax.grid(which="minor", color="white", lw=1.5); ax.grid(which="major", visible=False)
    ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
    ax.set(title="waffle: 100 cells, 4 categories")


# -------------------------------------------------------------- matrices ----
def heatmap_annot(ax):
    data = rng.random((5, 6)).round(2)
    im, _ = figures.heatmap(data, [f"r{i}" for i in range(5)], [f"col {j}" for j in range(6)], ax=ax, cmap=t.CMAP, cbarlabel="value")
    figures.annotate_heatmap(im, valfmt="{x:.1f}", fontsize=7)
    ax.set(title="annotated heatmap")


def tri(ax):
    figures.triheatmap(rng.random((5, 6)) * 100, rng.random((5, 6)) * 100, col_labels=[f"c{j}" for j in range(6)], ax=ax, normalise=True)
    ax.set(title="triheatmap: two matrices per cell")


def corr(ax):
    names = [f"v{i}" for i in range(8)]
    m = np.array(np.corrcoef(rng.normal(size=(8, 50)) + np.arange(8)[:, None] * 0.1))
    m[np.triu_indices(8, 1)] = np.nan
    im = ax.imshow(m, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.figure.colorbar(im, ax=ax, label="r")
    ax.set(xticks=range(8), xticklabels=names, yticks=range(8), yticklabels=names, title="correlation, coloured tick labels")
    groups = ["a", "a", "a", "b", "b", "c", "c", "c"]
    figures._set_label_colors_from_categories(ax.get_xticklabels(), groups, dict(zip("abc", _cycle())))
    figures._set_label_colors_from_categories(ax.get_yticklabels(), groups, dict(zip("abc", _cycle())))
    ax.grid(False)


def contours(ax):
    x, y = np.meshgrid(np.linspace(-3, 3, 80), np.linspace(-3, 3, 80))
    z = np.exp(-(x**2 + y**2) / 2) - 0.6 * np.exp(-((x - 1.5)**2 + (y + 1)**2))
    cf = ax.contourf(x, y, z, levels=12, cmap=t.CMAP)
    ax.contour(x, y, z, levels=12, colors=t.INK, linewidths=0.4)
    ax.figure.colorbar(cf, ax=ax, label="z")
    ax.set(title="contourf + contour", xlabel="x", ylabel="y")


def quiver(ax):
    x, y = np.meshgrid(np.linspace(-2, 2, 14), np.linspace(-2, 2, 14))
    u, v = -y, x
    ax.quiver(x, y, u, v, np.hypot(u, v), cmap=t.CMAP, scale=40, width=0.004)
    ax.streamplot(x, y, u, v, color=t.INK, linewidth=0.4, density=0.6, arrowsize=0.6)
    ax.set(title="quiver + streamplot", xlabel="x", ylabel="y", aspect="equal")


# ----------------------------------------------------------- composition ----
def stacked_area(ax):
    x = np.arange(20)
    ys = [np.cumsum(rng.random(20)) + i for i in range(5)]
    ax.stackplot(x, ys, labels=[f"s{i}" for i in range(5)], colors=_cycle()[:5], alpha=0.9, lw=0)
    ax.legend(loc="upper left", ncols=2)
    ax.set(title="stacked area", xlabel="t", ylabel="total")


def stacked_share(ax):
    cats = rng.choice(list("abcdefgh"), 300, p=[0.3, 0.25, 0.15, 0.12, 0.08, 0.05, 0.03, 0.02])
    figures.stacked_bar(cats, threshold=0.05, ax=ax)
    ax.set(title="stacked bar share + Other")


def polar_radar(ax):
    labels = ["speed", "power", "range", "cost", "noise", "weight"]
    ang = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    for i, c in enumerate(_cycle()[:3]):
        v = rng.random(len(labels)) * 0.6 + 0.3
        ax.plot(np.r_[ang, ang[0]], np.r_[v, v[0]], color=c, label=f"profile {i}")
        ax.fill(np.r_[ang, ang[0]], np.r_[v, v[0]], color=c, alpha=0.15)
    ax.set_xticks(ang); ax.set_xticklabels(labels); ax.set_yticks([0.5, 1.0])
    ax.legend(loc="upper left", bbox_to_anchor=(1.15, 1.05))
    ax.set_title("radar")


def inset(ax):
    x = np.linspace(0, 10, 400); y = np.sin(x) + 0.05 * np.sin(40 * x)
    ax.plot(x, y, color=_cycle()[0])
    ins = ax.inset_axes((0.55, 0.55, 0.4, 0.4), xlim=(2, 2.6), ylim=(0.5, 1.0))
    ins.plot(x, y, color=_cycle()[0]); ins.set_xticks([]); ins.set_yticks([])
    ax.indicate_inset_zoom(ins, edgecolor=t.INK)
    ax.set(title="inset zoom", xlabel="x", ylabel="y")


def broken_log(ax):
    f = np.logspace(0, 4, 500)
    s = 1 / (1 + (f / 50) ** 2) + 0.3 / (1 + ((f - 2000) / 100) ** 2) + 0.01 * rng.random(500)
    ax.semilogx(f, s, color=_cycle()[0])
    for fx, label in ((50, "corner"), (2000, "peak")):
        ax.annotate(label, (fx, np.interp(fx, f, s)), xytext=(0, 18), textcoords="offset points", ha="center",
                    arrowprops={"arrowstyle": "-", "color": t.INK, "lw": 0.6})
    ax.minorticks_on()
    ax.set(title="semilogx spectrum + annotations", xlabel="frequency (Hz)", ylabel="power")


def table_panel(ax):
    rows = [["model A", "0.91", "0.88"], ["model B", "0.87", "0.90"], ["model C", "0.80", "0.79"]]
    tb = ax.table(cellText=rows, colLabels=["", "AUC", "F1"], loc="center", cellLoc="center")
    tb.auto_set_font_size(False); tb.set_fontsize(plt.rcParams["font.size"])
    tb.scale(1, 1.4)
    for (r, c), cell in tb.get_celld().items():
        cell.set_edgecolor(t.GRID); cell.set_linewidth(0.5)
        if r == 0:
            cell.set_text_props(weight=plt.rcParams["axes.titleweight"])
    ax.axis("off"); ax.set(title="table in the style")


# --------------------------------------------- figure-level helpers ----
def _df(n=120):
    import polars as pl
    return pl.DataFrame({"a": rng.normal(size=n), "b": rng.normal(size=n), "c": rng.random(n), "g": rng.choice(list("xyz"), n)})


def joint(ax):
    _paste(ax, figures.scatter_boxplots(_df(), "a", "b", color_by="g", title="scatter boxplots"))


def scatter3d(ax):
    figures.scatter_3d(_df(), "a", "b", "c", ax=ax)
    ax.set_title("scatter 3d")


def sankey(ax):
    import polars as pl
    df = pl.DataFrame({"src": rng.choice(list("ab"), 80), "mid": rng.choice(np.array(["x", "y", None], dtype=object), 80), "dst": rng.choice(list("pq"), 80)})
    backends.plotly_template(1.0, _REGISTER[0])
    fig = figures.sankey(df, ["src", "mid", "dst"], title="sankey")
    fig.update_layout(width=500, height=380)
    try:
        png = fig.to_image(format="png", scale=2)
    except RuntimeError as e:
        return _needs_chrome(ax, e)
    ax.imshow(plt.imread(io.BytesIO(png))); ax.axis("off")


# -------------------------------------------------------------- backends ----
def plotnine_panel(ax):
    import pandas as pd
    from plotnine import aes, facet_wrap, geom_line, geom_point, ggplot, labs
    x = np.linspace(0, 10, 40)
    df = pd.concat([pd.DataFrame({"x": x, "y": np.sin(x + i) + 0.3 * i, "g": f"s{i}", "panel": "AB"[i // 2]}) for i in range(4)])
    p = ggplot(df, aes("x", "y", color="g")) + geom_line() + geom_point() + facet_wrap("panel") + labs(title="plotnine") + backends.theme_yusina(1.0, _REGISTER[0])
    _paste(ax, p.draw())


def plotly_panel(ax):
    import plotly.graph_objects as go
    backends.plotly_template(1.0, _REGISTER[0])
    x = np.linspace(0, 10, 40)
    fig = go.Figure([go.Scatter(x=x, y=np.sin(x + i), name=f"s{i}") for i in range(3)] + [go.Bar(x=list("abc"), y=[1, 2, 3], name="bars", xaxis="x2", yaxis="y2")])
    fig.update_layout(title="plotly", width=500, height=380, xaxis={"domain": [0, 0.6]}, xaxis2={"domain": [0.7, 1]}, yaxis2={"anchor": "x2"})
    try:
        png = fig.to_image(format="png", scale=2)
    except RuntimeError as e:
        return _needs_chrome(ax, e)
    ax.imshow(plt.imread(io.BytesIO(png))); ax.axis("off")


_REGISTER = [t.DEFAULT_REGISTER]  # current register for panels that build their own look (plotnine, plotly)
PROJECTION = {polar_radar: "polar", scatter3d: "3d"}

FAMILIES = {
    "lines": [lines, errorband, step_lines, stems, gradient_line, direct_labels, roc, twin_log],
    "scatter": [scatter, bubble, scatter_cbar, volcano, hexbin, hist2d],
    "distributions": [boxes, violins, strip, hist, kde, ridgeline, hist_overlay, ecdf, raster, errorbars],
    "categorical": [bars, grouped_bars, stacked, barh, lollipop, dumbbell, pie_donut, waffle],
    "matrices": [image, heatmap_annot, tri, corr, contours, quiver],
    "composition": [area, stacked_area, stacked_share, polar_radar, inset, broken_log, table_panel],
    "helpers": [joint, scatter3d, sankey],
    "backends": [plotnine_panel, plotly_panel],
}
PANELS = [lines, scatter, bars, boxes, errorbars, hist, image, area, twin_log]  # overview sheet


def _grid(panels, ncols=4, w=4.3, h=3.5):
    rows = math.ceil(len(panels) / ncols)
    fig = plt.figure(figsize=(w * ncols, h * rows))
    for i, fn in enumerate(panels, 1):
        fn(fig.add_subplot(rows, ncols, i, projection=PROJECTION.get(fn)))
    return fig


def sheet_family(family: str, scale: float | str = "notebook", register: str = t.DEFAULT_REGISTER):
    """One sheet: every panel of *family* in one register."""
    set_style(scale, register); _REGISTER[0] = register
    fig = _grid(FAMILIES[family])
    fig.suptitle(f"yusina - {family} - register={register} scale={scale!r}", fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    return fig


def sheet_registers(panel, scale: float | str = "notebook"):
    """One row per register for a single panel: how the same plot changes with taste."""
    fig = plt.figure(figsize=(4.3 * len(t.REGISTERS), 3.5))
    for i, register in enumerate(t.REGISTERS, 1):
        set_style(scale, register); _REGISTER[0] = register
        ax = fig.add_subplot(1, len(t.REGISTERS), i, projection=PROJECTION.get(panel))
        panel(ax); ax.set_title(f"{register}: {ax.get_title()}")
    fig.tight_layout()
    return fig


def build(scale, register=t.DEFAULT_REGISTER):
    set_style(scale, register); _REGISTER[0] = register
    fig = _grid(PANELS, ncols=3, w=5, h=4)
    fig.suptitle(f"yusina gallery - scale={scale!r} register={register}", fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    return fig


if __name__ == "__main__":
    args = sys.argv[1:]
    register = next((a for a in args if a in t.REGISTERS), t.DEFAULT_REGISTER)
    family = next((a for a in args if a in FAMILIES or a == "all"), None)
    args = [a for a in args if a not in (register, family)]
    scale = _arg_scale(args[0]) if args else "notebook"
    if family:
        for fam in FAMILIES if family == "all" else [family]:
            out = GALLERY / f"{fam}_{register}.png"
            sheet_family(fam, scale, register).savefig(out, dpi=120); plt.close("all")
            print("wrote", out)
    else:
        out = Path(args[1]) if len(args) > 1 else GALLERY / f"gallery_{register}.png"
        build(scale, register).savefig(out, dpi=150)
        print("wrote", out)
