"""Apply the yusina style to matplotlib."""

from __future__ import annotations

import functools
from pathlib import Path
from typing import Any

import matplotlib as mpl
from matplotlib.axes import Axes

from yusina import tokens as t
from yusina._rcparams import build_rc

MPLSTYLE = Path(__file__).parent / "data" / f"yusina-{t.DEFAULT_REGISTER}.mplstyle"  # for `plt.style.use(MPLSTYLE)`


# plot method -> grid axis to switch off: lines that would cross bars, boxes,
# bins or fills; "both" for images. Swapped for horizontal orientations.
GRID_OFF = {"bar": "x", "hist": "x", "boxplot": "x", "violinplot": "x", "fill_between": "x",
            "stackplot": "x", "barh": "y", "fill_betweenx": "y", "imshow": "both", "matshow": "both"}
_ORIG: dict[str, Any] = {}


def _patch_grid_defaults(enable: bool) -> None:
    """Wrap the ``Axes`` methods in ``GRID_OFF`` so plain matplotlib calls get
    only the grid lines that do not cross their marks; ``enable=False`` restores
    the originals."""
    if not enable:
        for name, orig in _ORIG.items():
            setattr(Axes, name, orig)
        _ORIG.clear()
        return
    for name, axis in GRID_OFF.items():
        if name in _ORIG:
            continue
        orig = _ORIG[name] = getattr(Axes, name)

        @functools.wraps(orig)
        def wrapper(self, *args, _orig=orig, _axis=axis, **kwargs):
            out = _orig(self, *args, **kwargs)
            horizontal = kwargs.get("orientation") == "horizontal" or kwargs.get("vert") is False
            off = {"x": "y", "y": "x"}[_axis] if horizontal and _axis != "both" else _axis
            if off == "both":
                self.grid(False)
            else:
                getattr(self, f"{off}axis").grid(False)
            return out

        setattr(Axes, name, wrapper)


def set_style(scale: float | str = t.DEFAULT_CONTEXT, register: str = t.DEFAULT_REGISTER,
              grid_defaults: bool = True) -> None:
    """Apply the yusina style to the current matplotlib session.

    ``scale`` is a plotting *context*: it multiplies every point size, line
    width, marker size and pad in the sheet (not colours, weights or styles).
    Pass a float, or a name from ``tokens.CONTEXTS`` ("paper", "notebook",
    "talk", "poster").

    ``register`` is the taste axis (``tokens.REGISTERS``): "clean" (default),
    "formal", "latex", "biosynfoni".

        set_style()                    # paper, clean
        set_style("paper", "formal")
        set_style(1.25)                # custom scale

    ``grid_defaults`` patches the ``Axes`` plot methods in ``GRID_OFF`` so
    bars, histograms, boxplots and fills keep only the grid lines that do not
    cross them, and images get none (``imshow`` draws under the grid).
    ``grid_defaults=False`` restores matplotlib's own methods.
    """
    if isinstance(scale, str):
        scale = t.CONTEXTS[scale]
    valid = set(mpl.rcParams)
    mpl.rcParams.update({k: v for k, v in build_rc(scale, register).items() if k in valid})
    _patch_grid_defaults(grid_defaults)
