"""Apply the yusina style to matplotlib."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl

from yusina import tokens as t
from yusina._rcparams import build_rc

MPLSTYLE = Path(__file__).parent / f"yusina-{t.DEFAULT_REGISTER}.mplstyle"  # for `plt.style.use(MPLSTYLE)`


def set_style(scale: float | str = 1.0, register: str = t.DEFAULT_REGISTER) -> None:
    """Apply the yusina style to the current matplotlib session.

    ``scale`` is a plotting *context*: it multiplies every point size, line
    width, marker size and pad in the sheet (not colours, weights or styles).
    Pass a float, or a name from ``tokens.CONTEXTS`` ("paper", "notebook",
    "talk", "poster").

    ``register`` is the taste axis (``tokens.REGISTERS``): "clean" (default),
    "formal", "latex", "biosynfoni".

        set_style()                    # notebook, clean
        set_style("paper", "formal")
        set_style(1.25)                # custom scale
    """
    if isinstance(scale, str):
        scale = t.CONTEXTS[scale]
    valid = set(mpl.rcParams)
    mpl.rcParams.update({k: v for k, v in build_rc(scale, register).items() if k in valid})
