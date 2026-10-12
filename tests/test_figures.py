"""Run: python tests/test_figures.py  (or pytest).

Smoke-tests every public plot helper: it draws without raising and returns the
right artifact type. Also checks the two bits of real logic --
``_resolve_colors`` dispatch and ``stacked_bar``'s "Other" pooling.
"""

import sys
from pathlib import Path
from typing import cast

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import polars as pl
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.transforms import TransformedPath

from yusina import figures as f
from yusina import set_style

DF = pl.DataFrame(
    {
        "a": [1.0, 2.0, 3.0, None, 5.0, 6.0],
        "b": [6.0, 5.0, 4.0, 3.0, 2.0, 1.0],
        "c": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
        "g": ["x", "x", "y", "y", "z", "z"],
    }
)


def test_resolve_colors_dispatch():
    keys = ["a", "b", "c"]
    assert f._resolve_colors(keys, {"a": "red"}) == ["red", "grey", "grey"]
    assert f._resolve_colors(keys, ["red", "blue"]) == ["red", "blue", "red"]
    assert len(f._resolve_colors(keys, "viridis")) == 3
    assert len(f._resolve_colors(keys, None)) == 3


def test_stacked_bar_pools_other():
    cats = ["a"] * 90 + ["b"] * 7 + ["c"] * 3
    ax = f.stacked_bar(cats, threshold=0.05)
    # a and b clear 5%; c (3%) folds into Other -> 3 segments
    rects = [p for p in ax.patches if isinstance(p, Rectangle)]
    assert len(rects) == 3
    heights = sorted(round(p.get_height(), 3) for p in rects)
    assert heights == [0.03, 0.07, 0.90]
    plt.close("all")


def test_stacked_bar_accepts_polars_series():
    ax = f.stacked_bar(DF.get_column("g"))
    assert len(ax.patches) == 3
    plt.close("all")


def test_scatter_grouped_and_plain():
    ax = f.scatter(DF, "a", "b", color_by="g", palette={"x": "red"})
    assert len(ax.collections) == 3  # one PathCollection per group, nulls dropped
    plt.close("all")
    ax = f.scatter(DF, "a", "b")
    assert len(ax.collections) == 1
    plt.close("all")


def test_scatter_boxplots_returns_figure():
    fig = f.scatter_boxplots(DF, "a", "b", color_by="g")
    assert isinstance(fig, Figure)
    plt.close("all")


def test_scatter_3d():
    ax = f.scatter_3d(DF, "a", "b", "c")
    assert ax.name == "3d"
    plt.close("all")


def test_heatmap_and_annotate():
    data = np.arange(12).reshape(3, 4)
    im, _cbar = f.heatmap(data, list("rst"), list("wxyz"))
    texts = f.annotate_heatmap(im)
    assert len(texts) == 12
    plt.close("all")


def test_triheatmap():
    up, lo = np.random.rand(3, 4) * 100, np.random.rand(3, 4) * 100
    imgs, _cbar = f.triheatmap(up, lo, col_labels=list("wxyz"), normalise=True)
    assert len(imgs) == 4
    plt.close("all")


def test_inset_callouts_table():
    set_style(under=0)  # erase under the inset and the legend
    _, ax = plt.subplots()
    ax.semilogx([1, 10, 100], [0, 1, 0])
    f.inset_zoom(ax, (1, 10), (0, 1), bounds=(0.5, 0.5, 0.4, 0.4))
    canvas = cast(FigureCanvasAgg, ax.figure.canvas)
    canvas.draw()
    img = np.asarray(canvas.buffer_rgba())
    x, y = ax.transData.transform((10 ** 1.25, 0.75))  # on the parent line, under the inset
    assert (img[img.shape[0] - int(y), int(x)] == img[0, 0]).all()  # erased to background
    assert len(f.callouts(ax, {"up": (10, 1), "down": (100, 0)})) == 2
    ax.legend(["curve"], loc="lower left"); canvas.draw()  # the legend box joins the holes at draw time
    clip = cast(TransformedPath, ax.lines[0].get_clip_path()).get_fully_transformed_path()  # outer box + inset hole + legend hole
    assert len(np.asarray(clip.vertices)) == 15  # outer box + inset hole + legend hole, 5 vertices each
    plt.close("all")


def test_legend_under():
    """A thick black line under the legend box is drawn at a quarter alpha, not erased, not hidden; same under an inset."""
    set_style()
    _, ax = plt.subplots()
    ax.plot([0, 1], [0.5, 0.5], lw=20, color="#000000"); ax.set(xlim=(0, 1), ylim=(0, 1)); ax.grid(False)
    leg = ax.legend(["x"], loc="center", handlelength=0, handletextpad=0, borderpad=3)  # wide empty padding, no handle
    canvas = cast(FigureCanvasAgg, ax.figure.canvas); canvas.draw()
    img = np.asarray(canvas.buffer_rgba()); x0, y0, x1, y1 = leg.get_window_extent().extents
    at = (img.shape[0] - int((y0 + y1) / 2), int(x0) + 6)  # inside the box, in the padding
    assert 60 <= img[at][3] <= 66 and (img[at][:3] == 0).all()  # black at a quarter alpha on the transparent canvas
    set_style(under=0); canvas.draw(); img = np.asarray(canvas.buffer_rgba())
    assert (img[at] == img[0, 0]).all()  # erased to background
    set_style()
    _, ax = plt.subplots()  # the same under an inset: the parent line fades, the inset's own content stays full
    ax.plot([0, 1], [0.62, 0.62], lw=20, color="#000000"); ax.set(xlim=(0, 1), ylim=(0, 1)); ax.grid(False)
    ins = f.inset_zoom(ax, (0, 1), (0.4, 0.6), bounds=(0.3, 0.3, 0.4, 0.4)); ins.plot([0, 1], [0.5, 0.5], lw=20, color="#FF0000"); ins.grid(False)
    canvas = cast(FigureCanvasAgg, ax.figure.canvas); canvas.draw(); img = np.asarray(canvas.buffer_rgba())
    cx, cy = ax.transAxes.transform((0.5, 0.5)); px, py = ax.transAxes.transform((0.5, 0.62))
    assert (img[img.shape[0] - int(cy), int(cx)][:3] == [255, 0, 0]).all()  # inset line on top, full
    assert (img[img.shape[0] - int(py), int(px)] == [0, 0, 0, 64]).all()  # parent line under the inset at a quarter alpha
    tb = f.table(ax, DF.head(2), index="a")
    assert tb[0, 0].visible_edges == "TB" and tb[2, 0].visible_edges == "B"
    assert tb[1, 0].get_text().get_fontweight() == "bold"
    plt.close("all")


def test_ridgeline_reset():
    """In the overlap, reset=True leaves only the front ridge's alpha; without it the fills add up."""
    grid = np.linspace(-3, 3, 200); curves = [np.exp(-(grid**2)), np.exp(-((grid - 0.3) ** 2))]
    alphas = []
    set_style()  # transparent canvas: the alpha channel carries the composite
    for reset in (True, False):
        _, ax = plt.subplots(); ax.grid(False)
        f.ridgeline(ax, grid, curves, colours=["#000000", "#000000"], alpha=0.5, reset=reset)
        canvas = cast(FigureCanvasAgg, ax.figure.canvas); canvas.draw(); img = np.asarray(canvas.buffer_rgba())
        x, y = ax.transData.transform((0.15, 1.2))  # inside both ridges: above row 1's base, below row 0's top
        alphas.append(int(img[img.shape[0] - int(y), int(x)][3])); plt.close("all")
    assert alphas[0] == 128 and alphas[1] in (191, 192)  # 0.5 alone vs 1 - 0.5 * 0.5 stacked


def test_group_ticks():
    _, ax = plt.subplots()
    ax.set(xticks=[0, 1], xticklabels=["a", "b"])
    labels = f.group_ticks(ax, "x", ["#2C5F8A", "#FFD700"])
    assert labels[0].get_color() == "#2c5f8a" and labels[1].get_color() != "#ffd700" and labels[0].get_fontweight() == "bold"
    ax.bar([0, 1], [1, 2], color=["#2C5F8A", "#8E3B2E"])  # inferred from the marks at each tick
    assert [lab.get_color() for lab in f.group_ticks(ax)] == ["#2c5f8a", "#8e3b2e"]
    ax.scatter([5, 5, 5], [1, 2, 3], color="#1A4C32"); ax.set(xticks=[0, 1, 5], xticklabels=["a", "b", "c"])
    assert f.group_ticks(ax)[2].get_color() == "#1a4c32"
    plt.close("all")


def test_colormap_helpers():
    assert f.custom_cmap("Greys", first_color=True).N == plt.get_cmap("Greys").N
    assert f.filtered_colormap("GnBu").N < 256
    assert f.two_gradient_cmap().N == 256
    plt.close("all")


def test_annotate_stacked_bars():
    _fig, ax = plt.subplots()
    ax.bar(0, 5, bottom=0)
    ax.bar(0, 3, bottom=5)
    f.annotate_stacked_bars(ax, min_height=1)
    assert len([t for t in ax.texts]) == 2
    plt.close("all")


def test_sankey():
    sk = pl.DataFrame(
        {
            "src": ["a", "a", "b", "b", "b"],
            "mid": ["x", "y", "x", "x", None],
            "dst": ["p", "p", "q", "q", "q"],
        }
    )
    fig = f.sankey(sk, ["src", "mid", "dst"], palette={"a": "red"})
    trace = fig.data[0]
    assert isinstance(trace, go.Sankey)
    node, link = trace.to_plotly_json()["node"], trace.to_plotly_json()["link"]
    # per-column nodes: src{a,b} + mid{x,y,None} + dst{p,q} = 7
    assert len(node["label"]) == 7
    assert list(node["label"]).count("x") == 1  # 'x' in mid only, once
    # distinct pairs: src->mid {a-x,a-y,b-x,b-None} + mid->dst {x-p,y-p,x-q,None-q}
    assert len(link["source"]) == 8
    assert sum(link["value"]) == 5 + 5  # every row counted once per adjacent pair
    assert f._rgba("red", 0.3) == "rgba(255,0,0,0.3)"


def test_cleanfmt():
    assert f.cleanfmt("Step_Num") == "step num"
    assert f.cleanfmt(["A_B", 3]) == ["a b", 3]


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("all passed")
