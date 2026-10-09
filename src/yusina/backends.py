"""yusina style for libraries other than matplotlib.

Every adapter reads ``yusina.tokens`` so one edit there restyles all backends.
Optional imports happen inside each function: install the extra you use
(``pip install yusina[plotly]`` / ``[plotnine]`` / ``[shade]`` / ``[protein]``).
"""

from __future__ import annotations

import matplotlib as mpl
import polars as pl

from yusina import tokens as t
from yusina._rcparams import build_rc
from yusina.colours import colourDict
from yusina.figures import _rgba

_WEIGHT = {"regular": "normal"}  # matplotlib -> CSS/plotnine weight names
_plotnine_defaults: dict[str, type] = {}  # strong refs: plotnine's Registry is a WeakValueDictionary


# ----------------------------------------------------------------- palettes ----
def ordinal_palette(n: int | None = None) -> dict[str, str]:
    """biosynfoni's continuous-discrete scale: ordinal steps ("1".."4") on YlGnBu
    samples, control/"-1" at the pale end. Returns the mapping every adapter
    below consumes (mpl ListedColormap, plotly discrete colorscale, plotnine
    scale_colour_manual, viewer colour commands). ``n`` keeps the first n
    ordinal steps; the control entry is always included."""
    steps = {k: v for k, v in colourDict["continuous"].items() if k != "-1"}
    if n is not None:
        steps = dict(list(steps.items())[:n])
    return {**steps, "-1": colourDict["continuous"]["-1"]}


# -------------------------------------------------------------------- plotly ----
def plotly_template(scale: float | str = 1.0, register: str = t.DEFAULT_REGISTER):
    """Build ``go.layout.Template`` from tokens (register font stack and cycle,
    transparent paper/plot background, grid alpha, INK axes), register it as
    ``pio.templates["yusina"]`` and make it the default template.
    ``generate.write_plotly_template`` dumps it to JSON."""
    import plotly.graph_objects as go
    import plotly.io as pio

    if isinstance(scale, str):
        scale = t.CONTEXTS[scale]
    reg = t.REGISTERS[register]
    pt = t.FONT_PT * scale
    axis = {
        "showgrid": reg["grid_alpha"] > 0, "gridcolor": _rgba(t.GRID, reg["grid_alpha"]),
        "gridwidth": t.LINEWIDTH["grid"] * scale, "zeroline": False,
        "showline": reg["spine_lw"] > 0, "linecolor": t.INK, "linewidth": reg["spine_lw"] * scale or 1,
        "ticks": "outside", "tickcolor": t.INK, "ticklen": t.TICK_LEN["major"] * scale,
        "tickwidth": t.LINEWIDTH["tick_major"] * scale, "tickfont": {"size": t.FONT_SCALE["tick_label"] * pt},
        "title": {"font": {"size": t.FONT_SCALE["axes_label"] * pt}},
    }
    layout = go.Layout(
        font={"family": ", ".join(reg["sans"]), "size": pt, "color": t.INK},
        colorway=list(reg["cycle"]),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=axis, yaxis=axis,
        title={"font": {"size": t.FONT_SCALE["axes_title"] * pt,
                             "weight": _WEIGHT.get(reg["title_weight"], reg["title_weight"])}},
        legend={"bgcolor": "rgba(0,0,0,0)", "borderwidth": 0, "font": {"size": t.FONT_SCALE["legend"] * pt}},
    )
    template = go.layout.Template(layout=layout)
    pio.templates["yusina"] = template
    pio.templates.default = "yusina"  # call once, done, like set_style
    return template


# ------------------------------------------------------------------ plotnine ----
def theme_yusina(scale: float | str = 1.0, register: str = t.DEFAULT_REGISTER):
    """plotnine look: the register rcParams as a ``theme_matplotlib`` base plus
    fixes for what plotnine overrides (strip background, legend key, panel
    border, grid, spines). Returns a ``theme`` to add to a ggplot. Also makes
    the register cycle plotnine's default discrete colour/fill scale, globally,
    like ``set_style`` does for matplotlib; plotnine ignores ``axes.prop_cycle``."""
    from plotnine import (
        element_blank,
        element_line,
        element_text,
        scale_color_manual,
        scale_fill_manual,
        theme,
        theme_matplotlib,
    )
    from plotnine._utils.registry import Registry

    if isinstance(scale, str):
        scale = t.CONTEXTS[scale]
    reg = t.REGISTERS[register]
    valid = set(mpl.rcParams)
    rc = {k: v for k, v in build_rc(scale, register).items() if k in valid}
    grid = (element_line(color=t.GRID, alpha=reg["grid_alpha"], size=t.LINEWIDTH["grid"] * scale)
            if reg["grid_alpha"] > 0 else element_blank())
    spine = (element_line(color=t.INK, size=reg["spine_lw"] * scale)
             if reg["spine_lw"] > 0 else element_blank())
    look = theme_matplotlib(rc=rc) + theme(
        panel_background=element_blank(), panel_border=element_blank(), plot_background=element_blank(),
        panel_grid_major=grid, panel_grid_minor=element_blank(), axis_line=spine,
        strip_background=element_blank(), strip_text=element_text(weight=reg["title_weight"]),
        legend_background=element_blank(), legend_key=element_blank(),
    )
    cycle = list(reg["cycle"])

    def default(base):  # ``make_scale`` looks defaults up by name in Registry
        class scale_yusina_discrete(base):
            def __init__(self, values=cycle, **kwargs):
                super().__init__(values=values, **kwargs)
        return scale_yusina_discrete

    colour, fill = default(scale_color_manual), default(scale_fill_manual)
    _plotnine_defaults.update(scale_color_discrete=colour, scale_colour_discrete=colour, scale_fill_discrete=fill)
    Registry.update(_plotnine_defaults)
    return look


# ------------------------------------------------ datashader / holoviews ----
def shade_points(lf: pl.LazyFrame, x: str, y: str, agg: str | None = None,
                 width: int = 800, height: int = 600, cmap=None):
    """Rasterise >1e5 points. datashader 0.19 accepts pandas/dask/cuDF only, not
    polars; this streams ``lf`` in batches (``collect_batches``) through one
    ``ds.Canvas`` and sums the aggregates, so the full frame never materialises.
    Returns the shaded image (xarray) or, with holoviews installed, an
    interactive ``hv.Image`` that re-shades on zoom."""
    raise NotImplementedError


def shade_heatmap(lf: pl.LazyFrame, row: str, col: str, value: str,
                  agg: str = "mean", cmap=None):
    """Same streaming path for dense matrices (e.g. pairwise distances):
    aggregate per batch, return an ``hv.Image`` / ``hv.HeatMap``."""
    raise NotImplementedError


# ---------------------------------------------------------- protein viewers ----
def viewer_colours(viewer: str = "pymol") -> str:
    """Emit the CYCLE / ordinal palette as colour commands for one viewer
    (``pymol`` ``set_color``, ``chimerax`` ``color name``, ``py3dmol`` hex list),
    so chains/ligands match the paper's figures. Which viewer do you use?"""
    raise NotImplementedError
