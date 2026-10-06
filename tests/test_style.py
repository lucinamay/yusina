"""Run: python tests/test_style.py  (or pytest)."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import matplotlib as mpl

from yusina import tokens as t
from yusina._rcparams import build_rc
from yusina.generate import write_mplstyle

HEX = re.compile(r"^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$")


def test_scale_is_proportional():
    a, b = build_rc(1.0), build_rc(2.0)
    assert a["font.size"] == 10.0
    assert b["font.size"] == 20.0
    assert a["axes.titlesize"] == 13.5 and b["axes.titlesize"] == 27.0
    assert abs(a["xtick.labelsize"] - 7.2) < 1e-9
    assert abs(b["xtick.labelsize"] - 14.4) < 1e-9
    assert b["lines.linewidth"] == 2 * a["lines.linewidth"]
    # colours must not move with scale
    assert a["text.color"] == b["text.color"] == t.INK


def test_context_names_resolve():
    from yusina.style import set_style

    for name in t.CONTEXTS:
        set_style(name)
    set_style("poster")
    assert mpl.rcParams["font.size"] == 10.0 * t.CONTEXTS["poster"]
    assert abs(mpl.rcParams["axes.titlesize"] - 13.5 * t.CONTEXTS["poster"]) < 1e-9


def test_palette_is_valid_hex():
    for c in (t.INK, t.INK_FAINT, t.GRID, t.CANVAS, *t.CYCLE):
        assert HEX.match(c), c


def test_generated_file_loads():
    path = write_mplstyle(Path(__file__).parent / "_generated.mplstyle")
    try:
        with mpl.rc_context(fname=path):
            assert mpl.rcParams["font.size"] == 10.0
            assert mpl.rcParams["axes.grid"] is True
            assert mpl.rcParams["text.color"] == "#606060"       # quoted hex
            assert mpl.rcParams["axes.prop_cycle"].by_key()["color"][0] in (
                "#B9C311", "B9C311",
            )
    finally:
        path.unlink()


def test_every_mapped_key_is_real():
    unknown = set(build_rc()) - set(mpl.rcParams)
    # build_rc may carry keys for newer matplotlib; just report, don't fail hard
    assert not unknown, f"unknown rcParams: {sorted(unknown)}"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("all passed")
