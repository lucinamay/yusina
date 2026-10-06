"""Run: python tests/test_figures.py  (or pytest).

Smoke-tests every public plot helper: it draws without raising and returns the
right artifact type. Also checks the two bits of real logic --
``_resolve_colors`` dispatch and ``stacked_bar``'s "Other" pooling.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import polars as pl

from yusina import figures as f

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
    assert len(ax.patches) == 3
    heights = sorted(round(p.get_height(), 3) for p in ax.patches)
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
    assert isinstance(fig, plt.Figure)
    plt.close("all")


def test_scatter_3d():
    ax = f.scatter_3d(DF, "a", "b", "c")
    assert ax.name == "3d"
    plt.close("all")


def test_heatmap_and_annotate():
    data = np.arange(12).reshape(3, 4)
    im, cbar = f.heatmap(data, list("rst"), list("wxyz"))
    texts = f.annotate_heatmap(im)
    assert len(texts) == 12
    plt.close("all")


def test_triheatmap():
    up, lo = np.random.rand(3, 4) * 100, np.random.rand(3, 4) * 100
    imgs, cbar = f.triheatmap(up, lo, col_labels=list("wxyz"), normalise=True)
    assert len(imgs) == 4
    plt.close("all")


def test_colormap_helpers():
    assert f.custom_cmap("Greys", first_color=True).N == plt.get_cmap("Greys").N
    assert f.filtered_colormap("GnBu").N < 256
    assert f.two_gradient_cmap().N == 256
    plt.close("all")


def test_annotate_stacked_bars():
    fig, ax = plt.subplots()
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
    node = fig.data[0].node
    link = fig.data[0].link
    # per-column nodes: src{a,b} + mid{x,y,None} + dst{p,q} = 7
    assert len(node.label) == 7
    assert list(node.label).count("x") == 1  # 'x' in mid only, once
    # distinct pairs: src->mid {a-x,a-y,b-x,b-None} + mid->dst {x-p,y-p,x-q,None-q}
    assert len(link.source) == 8
    assert sum(link.value) == 5 + 5  # every row counted once per adjacent pair
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
