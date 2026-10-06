"""Apply the yusina style to matplotlib."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl

from yusina import tokens as t
from yusina._rcparams import build_rc

MPLSTYLE = Path(__file__).parent / "yusina.mplstyle"  # for `plt.style.use(MPLSTYLE)`


def set_style(scale: float | str = 1.0) -> None:
    """Apply the yusina style to the current matplotlib session.

    ``scale`` is a plotting *context*: it multiplies every point size, line
    width, marker size and pad in the sheet (not colours, weights or styles).
    Pass a float, or a name from ``tokens.CONTEXTS`` ("paper", "notebook",
    "talk", "poster").

        set_style()            # notebook baseline
        set_style("poster")
        set_style(1.25)        # custom
    """
    if isinstance(scale, str):
        scale = t.CONTEXTS[scale]
    valid = set(mpl.rcParams)
    mpl.rcParams.update({k: v for k, v in build_rc(scale).items() if k in valid})
