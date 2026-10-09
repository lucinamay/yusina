"""yusina style for libraries other than matplotlib. Framework only; bodies follow approval.

Every adapter reads ``yusina.tokens`` so one edit there restyles all backends.
Optional imports happen inside each function: install the extra you use
(``pip install yusina[plotly]`` / ``[plotnine]`` / ``[shade]`` / ``[protein]``).
"""

from __future__ import annotations

import polars as pl


# ----------------------------------------------------------------- palettes ----
def ordinal_palette(n: int | None = None) -> dict[str, str]:
    """biosynfoni's continuous-discrete scale: ordinal steps ("1".."4") on YlGnBu
    samples, control/"-1" at the pale end. Returns the mapping every adapter
    below consumes (mpl ListedColormap, plotly discrete colorscale, plotnine
    scale_colour_manual, viewer colour commands)."""
    raise NotImplementedError


# -------------------------------------------------------------------- plotly ----
def plotly_template(scale: float | str = 1.0):
    """Build ``go.layout.Template`` from tokens (font, colorway=CYCLE, transparent
    paper/plot background, grid alpha, INK axes) and register it as
    ``pio.templates["yusina"]``. ``generate.write_plotly_template`` dumps it to JSON."""
    raise NotImplementedError


# ------------------------------------------------------------------ plotnine ----
def theme_yusina(scale: float | str = 1.0):
    """plotnine theme. plotnine draws through matplotlib, so ``set_style`` already
    sets fonts/colours; this only fixes what plotnine overrides (strip background,
    legend key, panel border) and returns a ``theme`` to add to a ggplot."""
    raise NotImplementedError


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
