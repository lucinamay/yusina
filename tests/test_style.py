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


def test_registers_change_taste_not_size():
    for r in t.REGISTERS:
        rc = build_rc(1.0, r)
        assert rc["font.size"] == 10.0
        assert rc["font.sans-serif"] == t.REGISTERS[r]["sans"]
        assert "Arial" not in rc["font.sans-serif"]
    assert build_rc(1.0, "formal")["axes.grid"] is False
    assert "Montserrat" not in build_rc(1.0, "clean")["font.sans-serif"]


def test_palette_is_valid_hex():
    for c in (t.INK, t.INK_FAINT, t.GRID, t.CANVAS, *t.CYCLE):
        assert HEX.match(c), c


def test_generated_file_loads():
    path = write_mplstyle(path=Path(__file__).parent / "_generated.mplstyle")
    try:
        with mpl.rc_context(fname=path):
            assert mpl.rcParams["font.size"] == 10.0
            assert mpl.rcParams["axes.grid"] is True
            assert mpl.rcParams["text.color"] == "#606060"       # quoted hex
            first = t.REGISTERS[t.DEFAULT_REGISTER]["cycle"][0]
            assert mpl.rcParams["axes.prop_cycle"].by_key()["color"][0].lstrip("#") == first.lstrip("#")
    finally:
        path.unlink()


def test_every_mapped_key_is_real():
    unknown = set(build_rc()) - set(mpl.rcParams)
    # build_rc may carry keys for newer matplotlib; just report, don't fail hard
    assert not unknown, f"unknown rcParams: {sorted(unknown)}"


def test_palette_tags():
    from yusina import palettes as P

    assert P.hue_name("#FC8D62") == "orange" and P.hue_name("#B3B3B3") == "grey"
    assert P.google_like(P.get("Tol bright")) and not P.google_like(P.get("Carto Vivid"))
    assert P.blue_orange_start(P.get("Okabe-Ito"))
    assert P.distinct_n(P.get("seaborn colorblind")) == 3           # blue orange green, then orange again
    t = P.tags("Carto Vivid")
    assert abs(t["warm"] + t["cold"] - 1) < 1e-9 and t["contrast"] > 0
    assert "Carto Vivid" in P.find(mood="vivid", blue_orange_start=True)
    assert all(isinstance(v, (str, bool, int, float, list, dict)) for v in t.values())  # json-safe
    m = P.match("Egypt", "Carto Vivid")                                     # Carto Vivid leads orange, blue
    assert [P.base_hue(c) for c in m[:2]] == ["orange", "blue"] and sorted(m) == sorted(P.get("Egypt"))


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    print("all passed")
