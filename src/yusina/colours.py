colourDict = {
    "discrete": {
        "green": "#B9C311",  # green
        "teal": "#9BC2BA",  # teal
        "purple": "#CFC0D6",  # purple
        "orange": "#FFAD61",  # light orange
        "softred": "#EB6737",  # soft red
        "palegrey": "#D2CEC4",  # pale grey
        "yellow": "#FFEAA0",  # yellow
        "pink": "#FFC4CE",  # pink
        "blue": "#B4CAD8",  # light blue
        "red": "#C21100",  # red
    },
    "continuous": {
        "1": "#081d58",  #'#57BAC0',  # navy,
        "2": "#225ea8",  #'#77BC4D',  # royal blue,
        "3": "#41b6c4",  #'#F3C55F',  # teal,
        "4": "#7fcdbb",  #'#F48861',  # turquoise,
        "10": "#c7e9b4",  #'#797979',  # lemon green,
        "-1": "#c7e9b4",
    },
    "pathways": {
        "purple": "#A783B6",  # purple
        "orange": "#FF8B61",  # orange,
        "green": "#B9C311",  # green,
        "blue": "#6FB5C6",  # blue
        "pink": "#FFC4CE",  # pink
        "yellow": "#FFEAA0",  # yellow
    },
}



# 단청 바림(빛) ladders, 초빛 -> 2빛 -> 3빛 -> 먹: the 초빛 is the pigment mixed with 호분,
# then the pigment, then its deep step; values from korea_pigments.csv.
DANCHEONG_BARIM = {
    "red": ['#EBA18B', '#D64B2B', '#C0362C', '#562F27'],    # 분홍 장단 주홍 다자
    "green": ['#9EC79F', '#3F9E5A', '#566D52', '#211F1E'],  # 백록(삼록) 양록 하엽 먹
    "blue": ['#A9C1DC', '#5F93CF', '#26478F', '#211F1E'],   # 분삼청 삼청 군청 먹
}

# every continuous map yusina registers: name -> (stops light -> dark, collection or "")
CMAPS: dict[str, tuple[list[str], str]] = {
    # white, then the biosynthetic-distance steps: YlGnBu with its yellow end replaced by white
    "yusina": (["#FFFFFF"] + [colourDict["continuous"][k] for k in ("10", "4", "3", "2", "1")], ""),
    **{f"dancheong_{hue}": (steps, "Korea") for hue, steps in DANCHEONG_BARIM.items()},
    # 자수 바림: thread shading runs through several dyes (korea_pigments.csv), light -> deep,
    # changing hue on the way; stops interpolated in OKLab with palettes.through, nothing sampled from photographs
    "silk_petal": (['#ecdabb', '#efccc4', '#f1bdcc', '#f08da3', '#ea577b', '#b75d88', '#845b92'], "Korea"),  # 꽃잎: 소색 → 연홍 → 홍 → 자초
    "silk_leaf": (['#eef18d', '#c7da77', '#a1c361', '#7aad4c', '#689266', '#577875', '#495c7f'], "Korea"),  # 잎: 송화 → 괴화 → 쪽
    "silk_cloud": (['#ecdabb', '#efccc4', '#f1bdcc', '#b98baf', '#845b92', '#685c88', '#495c7f'], "Korea"),  # 구름: 소색 → 연홍 → 자초 → 쪽 (흉배의 구름 띠)
    "silk_feather": (['#ecdabb', '#c7dccd', '#9edcdd', '#729aad', '#495c7f', '#3a4454', '#2c2c2c'], "Korea"),  # 학 깃·하늘: 소색 → 옥색 → 쪽 → 현
    "delft": (['#F3EFE6', '#9EA2B2', '#68708E', '#4A5479', '#2F3862', '#1C244D', '#10153B'], "Netherlands"),  # tin-glaze white, then the cobalt washes of a Rijksmuseum plate, OKLab-interpolated
    "silk_osaek": (['#ea577b', '#f3ae73', '#cbc85f', '#7aad4c', '#577875', '#5e5c85', '#845b92'], "Korea"),  # 오색 띠 (흉배 물결·바위): 홍 → 치자 → 괴화 → 쪽 → 자초
}


def cmaps_by_collection() -> dict[str, list[str]]:
    """{collection: [cmap names]} for every map in ``CMAPS`` that has a collection."""
    out: dict[str, list[str]] = {}
    for name, (_, coll) in CMAPS.items():
        if coll:
            out.setdefault(coll, []).append(name)
    return out


def _register_cmap() -> None:
    import matplotlib as mpl
    from matplotlib.colors import LinearSegmentedColormap

    if "yusina" in mpl.colormaps:
        return
    for name, (stops, _) in CMAPS.items():
        cmap = LinearSegmentedColormap.from_list(name, stops)
        mpl.colormaps.register(cmap)
        mpl.colormaps.register(cmap.reversed())


_register_cmap()


def luminance(colour) -> float:
    """Relative (WCAG) luminance of *colour*; white = 1, black = 0."""
    import numpy as np
    from matplotlib.colors import to_rgb

    c = np.asarray(to_rgb(colour))
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return float(lin @ [0.2126, 0.7152, 0.0722])


def readable(colour, max_luminance: float = 0.3) -> str:
    """*colour* as text on the canvas: darkened with ``outline`` until its luminance is at
    most *max_luminance* (0.3 = 3:1 on white), so a label in its mark's colour stays legible."""
    from matplotlib.colors import to_hex

    colour = to_hex(colour)
    while luminance(colour) > max_luminance:
        colour = outline(colour)
    return colour


def outline(colour, strength: str = "soft", lightness: float | None = None, saturation: float | None = None) -> str:
    """Edge colour for a fill: same hue, darker and more saturated by ``tokens.EDGE[strength]``
    ("soft" for edges that should still read as the fill, "strong" for lines that must stand
    out on it); explicit *lightness* / *saturation* factors override. Hex string so
    ``generate`` quotes it in the .mplstyle."""
    import colorsys

    from matplotlib.colors import to_hex, to_rgb

    from yusina import tokens as t

    factors = t.EDGE[strength]
    lightness = factors["lightness"] if lightness is None else lightness
    saturation = factors["saturation"] if saturation is None else saturation
    h, l, s = colorsys.rgb_to_hls(*to_rgb(colour))
    return to_hex(colorsys.hls_to_rgb(h, l * lightness, min(1.0, s * saturation)))
