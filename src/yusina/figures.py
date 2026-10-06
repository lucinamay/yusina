"""Premade plots for scientific figures.

Curated, style-agnostic helpers pulled out of project figure scripts
(biosynfoni, ema-ai-paper). Every function draws on the active matplotlib
style (see ``yusina.set_style``); none hard-codes a colour or a size.
DataFrame arguments are polars.

Axes-drawing functions return the ``Axes`` (get the figure with ``ax.figure``);
functions that build their own multi-panel figure return the ``Figure``.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import polars as pl
from matplotlib.tri import Triangulation

from yusina import tokens as t


# ------------------------------------------------------------------ saving ----
def savefig(fig, filename, dpi: float = t.DPI_SAVE) -> None:
    """Save *fig* to *filename* (``.png`` assumed if no extension) and close it.

    When *filename* is a vector format, a sibling ``.png`` is written too.
    """
    path = Path(filename)
    if not path.suffix:
        path = path.with_suffix(".png")
    fig.savefig(path, dpi=dpi)
    if path.suffix.lower() != ".png":
        fig.savefig(path.with_suffix(".png"), dpi=dpi)
    plt.close(fig)


# --------------------------------------------------------------- colormaps ----
def custom_cmap(cmap, first_color: bool = False, last_color: bool = False):
    """Copy *cmap* (name or object) with its first and/or last entry made
    transparent -- useful to drop a "zero" bin out of an image."""
    if not isinstance(cmap, mpl.colors.Colormap):
        cmap = mpl.colormaps[cmap]
    colors = [cmap(i) for i in range(cmap.N)]
    if first_color:
        colors[0] = (0.95, 0.95, 0.95, 0.0)
    if last_color:
        colors[-1] = (1.0, 1.0, 0.95, 0.0)
    return mpl.colors.LinearSegmentedColormap.from_list(
        f"{cmap.name}_custom", colors, cmap.N
    )


def filtered_colormap(
    cmap, n_colors: int = 256, min_brightness: float = 0.15, max_brightness: float = 0.85
):
    """Copy *cmap* keeping only entries whose perceived luminance
    (``0.299R + 0.587G + 0.114B``) sits in ``[min_brightness, max_brightness]``,
    so the washed-out and near-black ends don't swallow categories."""
    name = cmap if isinstance(cmap, str) else getattr(cmap, "name", "cmap")
    rgb = plt.get_cmap(cmap, n_colors)(np.linspace(0, 1, n_colors))[:, :3]
    lum = rgb @ np.array([0.299, 0.587, 0.114])
    keep = rgb[(lum >= min_brightness) & (lum <= max_brightness)]
    return mpl.colors.ListedColormap(keep, name=f"{name}_filtered")


def two_gradient_cmap(low: str = "Greys", high: str = "Greens", name: str = "two_gradient"):
    """Stack the dark half of *low* under the light-to-dark span of *high* --
    a diverging-ish map that keeps zero neutral and one direction coloured."""
    n = 128
    lo = plt.get_cmap(low).resampled(n)(np.linspace(0.0, 0.4, n))
    hi = plt.get_cmap(high).resampled(n)(np.linspace(0.3, 1.0, n))
    return mpl.colors.ListedColormap(np.vstack([lo, hi]), name=name)


# ------------------------------------------------------------------- text ----
def cleanfmt(text):
    """Lowercase and de-underscore a string, or each string in a list; anything
    else is returned unchanged."""
    if isinstance(text, str):
        return text.replace("_", " ").lower()
    if isinstance(text, (list, tuple)):
        return [cleanfmt(x) for x in text]
    return text


def _resolve_colors(keys, palette=None) -> list:
    """Map an ordered iterable of category keys to colours.

    *palette*: ``Mapping`` (key -> colour, missing -> grey), a list/tuple
    (cycled), a colormap or its name (sampled evenly), or ``None`` (the active
    ``axes.prop_cycle``).
    """
    keys = list(keys)
    if isinstance(palette, Mapping):
        return [palette.get(k, "grey") for k in keys]
    if palette is None:
        cyc = plt.rcParams["axes.prop_cycle"].by_key().get("color", ["C0"])
        return [cyc[i % len(cyc)] for i in range(len(keys))]
    if isinstance(palette, (str, mpl.colors.Colormap)):
        cmap = plt.get_cmap(palette)
        return [cmap(x) for x in np.linspace(0, 1, max(len(keys), 1))]
    palette = list(palette)
    return [palette[i % len(palette)] for i in range(len(keys))]


# --------------------------------------------------------------- heatmaps ----
def heatmap(data, row_labels, col_labels, ax=None, cbar_kw=None, cbarlabel="", **kwargs):
    """Heatmap of a 2-D array with labelled rows and columns and a colorbar.

    Returns ``(AxesImage, Colorbar)``. Extra kwargs go to ``imshow``.
    Adapted from the matplotlib annotated-heatmap example.
    """
    data = np.asarray(data)
    if ax is None:
        ax = plt.gca()
    if cbar_kw is None:
        cbar_kw = {}

    im = ax.imshow(data, **kwargs)
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
    cbar.outline.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]), labels=cleanfmt(list(col_labels)))
    ax.set_yticks(np.arange(data.shape[0]), labels=cleanfmt(list(row_labels)))
    ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True, pad=0.5)
    plt.setp(
        ax.get_xticklabels(), rotation=90, ha="right", va="center", rotation_mode="anchor"
    )

    ax.spines[:].set_visible(False)
    ax.set_xticks(np.arange(data.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=1, alpha=1.0)
    ax.tick_params(which="minor", bottom=False, left=False)
    return im, cbar


def annotate_heatmap(
    im, data=None, valfmt="{x:.2f}", textcolors=("black", "white"), threshold=None, **textkw
):
    """Write each cell's value onto the heatmap *im*, switching text colour at
    *threshold* (default: middle of the colour range). Returns the list of
    ``Text``. Adapted from the matplotlib annotated-heatmap example."""
    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()
    data = np.asarray(data)

    threshold = im.norm(threshold) if threshold is not None else im.norm(data.max()) / 2.0
    kw = dict(horizontalalignment="center", verticalalignment="center")
    kw.update(textkw)
    if isinstance(valfmt, str):
        valfmt = mpl.ticker.StrMethodFormatter(valfmt)

    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            texts.append(im.axes.text(j, i, valfmt(data[i, j], None), **kw))
    return texts


def _triangulation_for_triheatmap(m: int, n: int):
    """Four ``Triangulation``s (N, E, S, W) splitting each cell of an m x n grid
    into quadrants -- the geometry behind :func:`triheatmap`."""
    xv, yv = np.meshgrid(np.arange(-0.5, m), np.arange(-0.5, n))
    xc, yc = np.meshgrid(np.arange(0, m), np.arange(0, n))
    x = np.concatenate([xv.ravel(), xc.ravel()])
    y = np.concatenate([yv.ravel(), yc.ravel()])
    cstart = (m + 1) * (n + 1)
    north = [(i + j * (m + 1), i + 1 + j * (m + 1), cstart + i + j * m)
             for j in range(n) for i in range(m)]
    east = [(i + 1 + j * (m + 1), i + 1 + (j + 1) * (m + 1), cstart + i + j * m)
            for j in range(n) for i in range(m)]
    south = [(i + 1 + (j + 1) * (m + 1), i + (j + 1) * (m + 1), cstart + i + j * m)
             for j in range(n) for i in range(m)]
    west = [(i + (j + 1) * (m + 1), i + j * (m + 1), cstart + i + j * m)
            for j in range(n) for i in range(m)]
    return [Triangulation(x, y, tri) for tri in (north, east, south, west)]


def triheatmap(
    upper,
    lower,
    col_labels=(),
    ax=None,
    cbar_kw=None,
    cbarlabel="",
    colours=("Greens", "Purples"),
    normalise=False,
):
    """Compare two same-shaped matrices in one grid: each cell is split on its
    diagonals, top/bottom triangles show *upper*, left/right show *lower*.

    Returns ``(list_of_images, Colorbar)``. With ``normalise=True`` both maps
    use a fixed 0-100 range.
    """
    upper, lower = np.asarray(upper), np.asarray(lower)
    if ax is None:
        ax = plt.gca()
    if cbar_kw is None:
        cbar_kw = {}

    values = [upper, lower, lower, upper]
    tris = _triangulation_for_triheatmap(upper.shape[1], upper.shape[0])
    cmaps = [colours[0], colours[1], colours[1], colours[0]]
    if normalise:
        norms = [plt.Normalize(0, 100) for _ in range(4)]
        imgs = [ax.tripcolor(tr, np.ravel(v), cmap=c, norm=n)
                for tr, v, c, n in zip(tris, values, cmaps, norms)]
    else:
        imgs = [ax.tripcolor(tr, np.ravel(v), cmap=c)
                for tr, v, c in zip(tris, values, cmaps)]

    cbar = ax.figure.colorbar(imgs[1], ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
    cbar.ax.set_yticks([])
    cbar.outline.set_visible(False)

    ax.set_xticks(np.arange(upper.shape[1]), labels=cleanfmt(list(col_labels)))
    ax.set_yticks([])
    ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True, pad=0.5)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", rotation_mode="anchor")

    ax.spines[:].set_visible(False)
    ax.invert_yaxis()
    ax.margins(x=0, y=0)
    ax.set_xticks(np.arange(upper.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(upper.shape[0] + 1) - 0.5, minor=True)
    ax.set_aspect("equal", "box")
    ax.grid(which="minor", color="w", linestyle="-", linewidth=1, alpha=1.0)
    ax.tick_params(which="minor", bottom=False, left=False)
    return imgs, cbar


# --------------------------------------------------------------- bar plots ----
def stacked_bar(categories, threshold: float = 0.0, ax=None, palette=None,
                other_label: str = "Other"):
    """One vertical stacked bar showing the category mix of *categories*
    (any iterable: list, polars/pandas Series, ndarray).

    Categories whose share is below *threshold* are pooled into *other_label*.
    Each segment is labelled with its share; segments over 3% also show their
    absolute count inside the bar. Returns the ``Axes``.
    """
    counts = Counter(categories)
    total = sum(counts.values())
    if not total:
        raise ValueError("stacked_bar: no categories to plot")

    small = sum(c for c in counts.values() if c / total < threshold)
    items = sorted(
        ((k, c) for k, c in counts.items() if c / total >= threshold),
        key=lambda kv: kv[1],
    )
    if small:
        items.insert(0, (other_label, small))

    keys = [k for k, _ in items]
    colors = _resolve_colors(keys, palette)
    if other_label in keys:
        colors[keys.index(other_label)] = "lightgrey"

    if ax is None:
        _, ax = plt.subplots(figsize=(3, 6))

    bottom = 0.0
    for (key, count), color in zip(items, colors):
        share = count / total
        ax.bar(0, share, bottom=bottom, width=0.6, color=color, edgecolor="white")
        mid = bottom + share / 2
        ax.text(0.4, mid, f"{cleanfmt(str(key)).capitalize()} ({share * 100:.1f}%)",
                va="center", ha="left")
        if share > 0.03:
            ax.text(0, mid, str(count), va="center", ha="center",
                    color="white", weight="bold")
        bottom += share

    ax.set(xlim=(-0.5, 2), ylim=(0, 1), xticks=[], yticks=[])
    ax.set_frame_on(False)
    return ax


def annotate_stacked_bars(ax, min_height: float = 1.0, valfmt: str = "{:.0f}",
                          color="#FFFFFFEE", **textkw):
    """Label every bar patch in *ax* with its height, centred in the segment --
    the counts-inside-a-stacked-histogram trick. Segments up to *min_height*
    are skipped."""
    for patch in ax.patches:
        height = patch.get_height()
        if height <= min_height:
            continue
        ax.annotate(
            valfmt.format(height),
            (patch.get_x() + patch.get_width() / 2, patch.get_y() + height / 2),
            ha="center", va="center", color=color, **textkw,
        )


# ----------------------------------------------------------------- scatter ----
def scatter(df: pl.DataFrame, x: str, y: str, color_by: str | None = None,
            palette=None, ax=None, title: str | None = None, legend: bool = True,
            **kwargs):
    """Scatter *y* vs *x* from a polars DataFrame, optionally split by *color_by*.

    Rows with a null *x*, *y* (or *color_by*) are dropped. Extra kwargs go to
    ``Axes.scatter``. Returns the ``Axes``.
    """
    kwargs.setdefault("alpha", 0.6)
    kwargs.setdefault("edgecolors", "none")
    cols = [x, y] + ([color_by] if color_by else [])
    df = df.drop_nulls(cols)
    if ax is None:
        _, ax = plt.subplots()

    if color_by is None:
        ax.scatter(df.get_column(x).to_numpy(), df.get_column(y).to_numpy(), **kwargs)
    else:
        cats = df.get_column(color_by).unique(maintain_order=True).to_list()
        for cat, color in zip(cats, _resolve_colors(cats, palette)):
            sub = df.filter(pl.col(color_by) == cat)
            ax.scatter(sub.get_column(x).to_numpy(), sub.get_column(y).to_numpy(),
                       color=color, label=str(cat), zorder=3, **kwargs)
        if legend:
            ax.legend(frameon=False, prop={"size": 6})

    ax.set_xlabel(cleanfmt(x))
    ax.set_ylabel(cleanfmt(y))
    if title:
        ax.set_title(cleanfmt(title))
    ax.grid(True, alpha=0.3, linewidth=0.5)
    return ax


def _set_ax_boxplot_i_colour(bp: dict, i: int, colour, inner_alpha: float = 0.6) -> dict:
    """Recolour the i-th box (and its whiskers, caps, median, fliers) of a
    ``patch_artist`` boxplot dict to *colour*."""
    translucent = mpl.colors.to_rgba(colour, inner_alpha)
    bp["boxes"][i].set_facecolor(translucent)
    bp["boxes"][i].set_edgecolor(colour)
    bp["medians"][i].set_color(colour)
    bp["whiskers"][i * 2].set_color(colour)
    bp["whiskers"][i * 2 + 1].set_color(colour)
    bp["caps"][i * 2].set_color(colour)
    bp["caps"][i * 2 + 1].set_color(colour)
    if bp["fliers"]:
        bp["fliers"][i].set_markeredgecolor(translucent)
    return bp


def scatter_boxplots(df: pl.DataFrame, x: str, y: str, color_by: str | None = None,
                     palette=None, title: str | None = None):
    """Scatter of *y* vs *x* with a marginal boxplot on each axis (a "joint"
    plot). Split by *color_by* if given; each group keeps one colour across the
    scatter and both marginals. Returns the ``Figure``."""
    cols = [x, y] + ([color_by] if color_by else [])
    df = df.drop_nulls(cols)

    fig = plt.figure()
    gs = fig.add_gridspec(2, 2, width_ratios=(4, 1), height_ratios=(1, 4),
                          wspace=0.05, hspace=0.05)
    ax = fig.add_subplot(gs[1, 0])
    top = fig.add_subplot(gs[0, 0], sharex=ax)
    right = fig.add_subplot(gs[1, 1], sharey=ax)
    top.tick_params(length=0, labelbottom=False, labelsize=5)
    right.tick_params(length=0, labelleft=False, labelsize=5, labelrotation=-30)
    ax.tick_params(length=0)

    if color_by is None:
        groups = [("", df)]
    else:
        cats = df.get_column(color_by).unique(maintain_order=True).to_list()
        groups = [(c, df.filter(pl.col(color_by) == c)) for c in cats]
    colors = _resolve_colors([label for label, _ in groups], palette)

    xs = [g.get_column(x).to_numpy() for _, g in groups]
    ys = [g.get_column(y).to_numpy() for _, g in groups]
    labels = [str(label) for label, _ in groups]
    xbox = top.boxplot(xs, vert=False, patch_artist=True, tick_labels=labels)
    ybox = right.boxplot(ys, vert=True, patch_artist=True, tick_labels=labels)

    for i, label in enumerate(labels):
        ax.scatter(xs[i], ys[i], color=colors[i], label=label, alpha=0.6,
                   edgecolors="none", zorder=3)
        _set_ax_boxplot_i_colour(xbox, i, colors[i])
        _set_ax_boxplot_i_colour(ybox, i, colors[i])

    if color_by is not None:
        ax.legend(frameon=False, prop={"size": 6})
    ax.set_xlabel(cleanfmt(x), labelpad=10)
    ax.set_ylabel(cleanfmt(y), labelpad=10)
    ax.grid(True, alpha=0.3, linewidth=0.5)
    if title:
        top.set_title(cleanfmt(title), pad=20)
    gs.tight_layout(fig)
    return fig


def scatter_3d(df: pl.DataFrame, x: str, y: str, z: str, marker: str = "o", ax=None):
    """3-D scatter of three polars DataFrame columns. Returns the 3-D ``Axes``."""
    if ax is None:
        ax = plt.figure().add_subplot(projection="3d")
    df = df.drop_nulls([x, y, z])
    ax.scatter(df.get_column(x).to_numpy(), df.get_column(y).to_numpy(),
               df.get_column(z).to_numpy(), marker=marker)
    ax.set_xlabel(cleanfmt(x))
    ax.set_ylabel(cleanfmt(y))
    ax.set_zlabel(cleanfmt(z))
    return ax


# ------------------------------------------------------------------ sankey ----
def _rgba(color, alpha: float) -> str:
    """matplotlib colour -> ``"rgba(r,g,b,a)"`` string for plotly."""
    r, g, b = mpl.colors.to_rgb(color)
    return f"rgba({int(r * 255)},{int(g * 255)},{int(b * 255)},{alpha})"


def sankey(df: pl.DataFrame, columns, palette=None, link_alpha: float = 0.3,
           column_labels=None, pad: int = 20, thickness: int = 20, title=None):
    """Multi-column flow (Sankey) diagram from a polars DataFrame.

    Each row of *df* is one unit of flow; *columns* is the ordered list of
    categorical columns it passes through. Links connect adjacent columns,
    their width being the row count for that value pair. Nulls become
    ``"None"``. Nodes are per-column, so the same value in two columns is two
    nodes (no accidental back-flow).

    *palette* is passed to :func:`_resolve_colors` once per column (so a dict
    keyed by category value works). Links take their source node's colour at
    *link_alpha*. *column_labels* overrides the header text (dict col -> text,
    or a list matching *columns*).

    Returns a ``plotly.graph_objects.Figure`` (needs ``plotly``).
    """
    import plotly.graph_objects as go

    columns = list(columns)
    if len(columns) < 2:
        raise ValueError("sankey: need at least two columns")

    df = df.with_columns(
        pl.col(c).cast(pl.String).fill_null("None") for c in columns
    )

    node_keys, labels = [], []
    for col in columns:
        for val in df.get_column(col).unique(maintain_order=True).to_list():
            node_keys.append((col, val))
            labels.append(val)
    index = {key: i for i, key in enumerate(node_keys)}

    node_colors = {}
    for col in columns:
        vals = [v for c, v in node_keys if c == col]
        for val, color in zip(vals, _resolve_colors(vals, palette)):
            node_colors[(col, val)] = mpl.colors.to_hex(color)
    node_color_list = [node_colors[key] for key in node_keys]

    src, tgt, value, link_color = [], [], [], []
    for a, b in zip(columns, columns[1:]):
        grouped = df.group_by(a, b).len().sort("len", descending=True)
        for row_a, row_b, n in grouped.iter_rows():
            s = index[(a, row_a)]
            src.append(s)
            tgt.append(index[(b, row_b)])
            value.append(n)
            link_color.append(_rgba(node_color_list[s], link_alpha))

    fig = go.Figure(
        go.Sankey(
            node=dict(pad=pad, thickness=thickness, label=labels,
                      color=node_color_list, line=dict(width=0)),
            link=dict(source=src, target=tgt, value=value, color=link_color),
        )
    )

    if isinstance(column_labels, Mapping):
        headers = [column_labels.get(c, c) for c in columns]
    elif column_labels is not None:
        headers = list(column_labels)
    else:
        headers = [cleanfmt(c) for c in columns]
    for i, text in enumerate(headers):
        fig.add_annotation(
            x=i / (len(columns) - 1), y=1.06, text=f"<b>{text}</b>",
            showarrow=False, xref="paper", yref="paper",
            xanchor=("left" if i == 0 else "right" if i == len(columns) - 1 else "center"),
        )
    if title:
        fig.update_layout(title_text=title)
    return fig


# ------------------------------------------------------- coloured tick labels ----
def _set_label_colors(ticklabels, colors) -> None:
    """Give each tick label a rounded coloured background box."""
    for label, color in zip(ticklabels, colors):
        plt.setp(
            label,
            backgroundcolor=color,
            bbox=dict(facecolor=color, alpha=0.5,
                      boxstyle="round, rounding_size=0.7", edgecolor="none"),
        )


def _cat_to_colour(categories, col_dict: dict) -> list:
    """Look each category (or the first element, if it is a list) up in
    *col_dict*, falling back to grey."""
    colors = []
    for category in categories:
        if isinstance(category, list):
            category = category[0] if category else ""
        colors.append(col_dict.get(category, "grey"))
    return colors


def _set_label_colors_from_categories(ticklabels, categories, col_dict: dict) -> None:
    """:func:`_set_label_colors` with the colours resolved from *categories*
    through *col_dict*."""
    _set_label_colors(ticklabels, _cat_to_colour(categories, col_dict))
